from __future__ import division

import os
import collections
from time import sleep
from builtins import dict
from datetime import datetime, timedelta

import yaml
import requests
from retry import retry

from testrail.helper import TestRailError, TooManyRequestsError, ServiceUnavailableError

nested_dict = lambda: collections.defaultdict(nested_dict)


class UpdateCache(object):
    """ Decorator class for updating API cache
    """
    def __init__(self, cache):
        self.cache = cache

    def __call__(self, f):
        def wrapped_f(*args, **kwargs):
            api_resp = f(*args, **kwargs)
            if isinstance(api_resp, dict) and not api_resp:
                # Empty dict, indicating something at args[-1] was deleted.
                self._delete_from_cache(args[-1])
            else:
                # Something must have been added or updated
                self._update_cache(api_resp)

            return api_resp
        return wrapped_f

    def _delete_from_cache(self, delete_id):
        ''' Check every dict inside of self.cache for an object with a matching
            ID
        '''
        for project in self.cache.values():
            obj_list = project['value']
            for index, obj in enumerate(obj_list):
                if obj['id'] == delete_id:
                    obj_list.pop(index)
                    return
        else:
            # If we hit this, it means we looked at every object in every cache
            # and didn't find a match. Set the cache to refresh on the next call
            for project in self.cache.values():
                project['ts'] = None

            return

    def _update_cache(self, update_obj):
        ''' Update the cache using update_obj.

            If a matching object is found in the cache, replace it with update_obj.
            If no matching object is found, append it to the cache
        '''
        # Make update_obj a list if it isn't already
        update_list = update_obj if isinstance(update_obj, list) else [update_obj, ]

        for update_obj in update_list:
            if 'project_id' in update_obj:
                # Most response objects have a project_id
                obj_key = update_obj['project_id']
            elif 'test_id' in update_obj:
                # Results have no project_id and are cached based on test_id
                obj_key = update_obj['test_id']
            else:
                raise TestRailError("Unknown object type; can't update cache")

            if not self.cache[obj_key]['ts']:
                # The cache will clear on the next read, so no reason to add/update
                continue

            obj_list = self.cache[obj_key]['value']
            for index, obj in enumerate(obj_list):
                if obj['id'] == update_obj['id']:
                    obj_list[index] = update_obj
                    break
            else:
                # If we get this far, it means we searched all objects without
                # finding a match. Add the object
                obj_list.append(update_obj)
                obj_list.sort(key=lambda x: x['id'])


class API(object):
    _config = None
    _ts = datetime.now() - timedelta(days=1)
    _shared_state = {'_case_types': nested_dict(),
                     '_cases': nested_dict(),
                     '_configs': nested_dict(),
                     '_milestones': nested_dict(),
                     '_plans': nested_dict(),
                     '_priorities': nested_dict(),
                     '_projects': nested_dict(),
                     '_results': nested_dict(),
                     '_runs': nested_dict(),
                     '_sections': nested_dict(),
                     '_statuses': nested_dict(),
                     '_suites': nested_dict(),
                     '_tests': nested_dict(),
                     '_users': nested_dict(),
                     '_timeout': 30,
                     '_project_id': None}

    def __init__(self, email=None, key=None, url=None):
        self.__dict__ = self._shared_state
        if email is not None and key is not None and url is not None:
            config = dict(email=email, key=key, url=url)
            self._config = config
        elif self._config is not None:
            config = self._config
        else:
            config = self._conf()

        self._auth = (config['email'], config['key'])
        self._url = config['url']
        self.headers = {'Content-Type': 'application/json'}
        self.verify_ssl = config.get('verify_ssl', True)

    def _conf(self):
        TR_EMAIL = 'TESTRAIL_USER_EMAIL'
        TR_KEY = 'TESTRAIL_USER_KEY'
        TR_URL = 'TESTRAIL_URL'

        conf_path = '%s/.testrail.conf' % os.path.expanduser('~')

        if os.path.isfile(conf_path):
            with open(conf_path, 'r') as f:
                config = yaml.load(f, Loader=yaml.BaseLoader)
        else:
            config = {
                'testrail': {
                    'user_email': None, 'user_key': None, 'url': None
                }
            }

        _email = os.environ.get(TR_EMAIL) or config['testrail'].get('user_email')
        _key = os.environ.get(TR_KEY) or config['testrail'].get('user_key')
        _url = os.environ.get(TR_URL) or config['testrail'].get('url')

        if _email is None:
            raise TestRailError('A user email must be set in environment ' +
                                'variable %s or in ' % TR_EMAIL +
                                '~/.testrail.conf')
        if _key is None:
            raise TestRailError('A password or API key must be set in ' +
                                'environment variable %s or ' % TR_KEY +
                                'in ~/.testrail.conf')
        if _url is None:
            raise TestRailError('A URL must be set in environment variable ' +
                                '%s or in ~/.testrail.conf' % TR_URL)

        if os.environ.get('TESTRAIL_VERIFY_SSL') is not None:
            verify_ssl = os.environ.get('TESTRAIL_VERIFY_SSL').lower() == 'true'
        elif config['testrail'].get('verify_ssl') is not None:
            verify_ssl = config['testrail'].get('verify_ssl').lower() == 'true'
        else:
            verify_ssl = True

        return {'email': _email, 'key': _key, 'url': _url, 'verify_ssl': verify_ssl}

    def _paginate_request(self, end_point, params, field):
        params["offset"] = 0
        params["limit"] = 250
        values = []
        while True:
            items = self._get(end_point, params=params)
            if items["size"] == 0:
                return values
            values.extend(items[field])
            params["offset"] += params["limit"]

    @staticmethod
    def _raise_on_429_or_503_status(resp):
        """ 429 is TestRail's status for too many API requests
            Use the 'Retry-After' key in the response header to sleep for the
            specified amount of time, then raise an exception to trigger the
            retry
        """
        if resp.status_code == 429:
            wait_amount = int(resp.headers['Retry-After'])
            sleep(wait_amount)
            raise TooManyRequestsError("Too many API requests")
        if resp.status_code == 503:
            raise ServiceUnavailableError("Service Temporarily Unavailable")
        else:
            return

    def _refresh(self, ts):
        if not ts:
            return True

        td = (datetime.now() - ts)
        since_last =  (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

        return since_last > self._timeout

    @classmethod
    def flush_cache(cls):
        """ Set all cache objects to refresh the next time they are accessed
        """
        def clear_ts(cache):
            if 'ts' in cache:
                cache['ts'] = None
            for val in cache.values():
                if isinstance(val, dict):
                    clear_ts(val)


        for cache in cls._shared_state.values():
            if not isinstance(cache, dict):
                continue
            else:
                clear_ts(cache)

    def set_project_id(self, project_id):
        self._project_id = project_id

    # User Requests
    def users(self):
        if self._refresh(self._users['ts']):
            # get new value, if request is good update value with new ts.
            self._users['value'] = self._get('get_users')
            self._users['ts'] = datetime.now()
        return self._users['value']

    def user_with_id(self, user_id):
        try:
            return list(filter(lambda x: x['id'] == user_id, self.users()))[0]
        except IndexError:
            raise TestRailError("User ID '%s' was not found" % user_id)

    def user_with_email(self, user_email):
        try:
            return list(filter(lambda x: x['email'] == user_email, self.users()))[0]
        except IndexError:
            raise TestRailError("User email '%s' was not found" % user_email)

    # Project Requests
    def projects(self):
        if self._refresh(self._projects['ts']):
            # get new value, if request is good update value with new ts.
            self._projects['value'] = self._paginate_request("get_projects", {}, "projects")
            self._projects['ts'] = datetime.now()
        return self._projects['value']

    def project_with_id(self, project_id):
        try:
            return list(filter(lambda x: x['id'] == project_id, self.projects()))[0]
        except IndexError:
            raise TestRailError("Project ID '%s' was not found" % project_id)

    # Suite Requests
    def suites(self, project_id=None):
        project_id = project_id or self._project_id
        if self._refresh(self._suites[project_id]['ts']):
            # get new value, if request is good update value with new ts.
            _suites = self._get('get_suites/%s' % project_id)
            self._suites[project_id]['value'] = _suites
            self._suites[project_id]['ts'] = datetime.now()
        return self._suites[project_id]['value']

    def suite_with_id(self, suite_id):
        try:
            return list(filter(lambda x: x['id'] == suite_id, self.suites()))[0]
        except IndexError:
            raise TestRailError("Suite ID '%s' was not found" % suite_id)

    @UpdateCache(_shared_state['_suites'])
    def add_suite(self, suite):
        fields = ['name', 'description']
        fields.extend(self._custom_field_discover(suite))

        project_id = suite.get('project_id')
        payload = self._payload_gen(fields, suite)
        return self._post('add_suite/%s' % project_id, payload)

    # Case Requests
    def cases(self, project_id=None, suite_id=-1):
        project_id = project_id or self._project_id
        if self._refresh(self._cases[project_id][suite_id]['ts']):
            # get new value, if request is good update value with new ts.
            endpoint = 'get_cases/%s' % project_id
            params = {'suite_id': suite_id} if suite_id != -1 else {}
            self._cases[project_id][suite_id]["value"] = self._paginate_request(endpoint, params, "cases")
            self._cases[project_id][suite_id]['ts'] = datetime.now()
        return self._cases[project_id][suite_id]['value']

    def case_with_id(self, case_id, suite_id=None):
        try:
            return list(filter(lambda x: x['id'] == case_id, self.cases(suite_id=suite_id)))[0]
        except IndexError:
            raise TestRailError("Case ID '%s' was not found" % case_id)

    def add_case(self, case):
        fields = ['title', 'template_id', 'type_id', 'priority_id', 'estimate',
                  'milestone_id', 'refs']
        section_id = case.get('section_id')
        payload = self._payload_gen(fields, case)
        #TODO get update cache working for now reset cache
        self.flush_cache()
        return self._post('add_case/%s' % section_id, payload)

    def update_case(self, case):
        fields = ['title', 'template_id', 'type_id', 'priority_id', 'estimate',
                  'milestone_id', 'refs']
        fields.extend(self._custom_field_discover(case))

        data = self._payload_gen(fields, case)
        #TODO get update cache working for now reset cache
        self.flush_cache()
        return self._post('update_case/%s' % case.get('id'), data)


    def case_types(self):
        if self._refresh(self._case_types['ts']):
            # get new value, if request is good update value with new ts.
            _case_types = self._get('get_case_types')
            self._case_types['value'] = _case_types
            self._case_types['ts'] = datetime.now()
        return self._case_types['value']

    def case_type_with_id(self, case_type_id):
        try:
            return list(filter(
                lambda x: x['id'] == case_type_id, self.case_types()))[0]
        except IndexError:
            return TestRailError(
                "Case Type ID '%s' was not found" % case_type_id)

    # Milestone Requests
    def milestones(self, project_id):
        if self._refresh(self._milestones[project_id]['ts']):
            # get new value, if request is good update value with new ts.
            endpoint = 'get_milestones/%s' % project_id
            self._milestones[project_id]['value'] = self._paginate_request(endpoint, {}, "milestones")
            self._milestones[project_id]['ts'] = datetime.now()
        return self._milestones[project_id]['value']

    def milestone_with_id(self, milestone_id, project_id=None):
        if project_id is None:
            return self._get('get_milestone/%s' % milestone_id)
        else:
            try:
                return list(filter(lambda x: x['id'] == milestone_id,
                              self.milestones(project_id)))[0]
            except IndexError:
                raise TestRailError(
                    "Milestone ID '%s' was not found" % milestone_id)

    @UpdateCache(_shared_state['_milestones'])
    def add_milestone(self, milestone):
        fields = ['name', 'description', 'due_on']
        fields.extend(self._custom_field_discover(milestone))

        project_id = milestone.get('project_id')
        payload = self._payload_gen(fields, milestone)
        return self._post('add_milestone/%s' % project_id, payload)

    @UpdateCache(_shared_state['_milestones'])
    def update_milestone(self, milestone):
        fields = ['name', 'description', 'due_on', 'is_completed']
        fields.extend(self._custom_field_discover(milestone))

        data = self._payload_gen(fields, milestone)
        return self._post('update_milestone/%s' % milestone.get('id'), data)

    @UpdateCache(_shared_state['_milestones'])
    def delete_milestone(self, milestone_id):
        return self._post('delete_milestone/%s' % milestone_id)

    # Priority Requests
    def priorities(self):
        if self._refresh(self._priorities['ts']):
            # get new value, if request is good update value with new ts.
            _priorities = self._get('get_priorities')
            self._priorities['value'] = _priorities
            self._priorities['ts'] = datetime.now()
        return self._priorities['value']

    def priority_with_id(self, priority_id):
        try:
            return list(filter(
                lambda x: x['id'] == priority_id, self.priorities()))[0]
        except IndexError:
            raise TestRailError("Priority ID '%s' was not found")

    # Section Requests
    def sections(self, project_id=None, suite_id=-1):
        project_id = project_id or self._project_id
        if self._refresh(self._sections[project_id][suite_id]['ts']):
            params = {'suite_id': suite_id} if suite_id != -1 else None
            endpoint = 'get_sections/%s' % project_id
            self._sections[project_id][suite_id]['value'] = self._paginate_request(endpoint, params, "sections")
            self._sections[project_id][suite_id]['ts'] = datetime.now()
        return self._sections[project_id][suite_id]['value']

    def section_with_id(self, section_id):
        try:
            return list(filter(lambda x: x['id'] == section_id, self.sections()))[0]
        except IndexError:
            raise TestRailError("Section ID '%s' was not found" % section_id)
        except TestRailError:
            # project must not be in single suite mode
            return self._get('get_section/%s' % section_id)

    def add_section(self, section):
        fields = ['description', 'suite_id', 'parent_id', 'name']
        fields.extend(self._custom_field_discover(section))

        project_id = section.get('project_id') or self._project_id
        payload = self._payload_gen(fields, section)
        #TODO get update cache working for now reset cache
        self.flush_cache()
        return self._post('add_section/%s' % project_id, payload)

    # Plan Requests
    def plans(self, project_id=None):
        project_id = project_id or self._project_id
        if self._refresh(self._plans[project_id]['ts']):
            # get new value, if request is good update value with new ts.
            endpoint = 'get_plans/%s' % project_id
            self._plans[project_id]['value'] = self._paginate_request(endpoint, {}, "plans")
            self._plans[project_id]['ts'] = datetime.now()
        return self._plans[project_id]['value']

    def plan_with_id(self, plan_id, with_entries=False):
        #TODO consider checking if plan already has entries and if not add it
        if with_entries:
            return self._get('get_plan/%s' % plan_id)
        try:
            return list(filter(lambda x: x['id'] == plan_id, self.plans()))[0]
        except IndexError:
            raise TestRailError("Plan ID '%s' was not found" % plan_id)

    @UpdateCache(_shared_state['_plans'])
    def add_plan(self, plan):
        fields = ['name', 'description', 'milestone_id', 'entries']
        fields.extend(self._custom_field_discover(plan))

        project_id = plan.get('project_id')
        payload = self._payload_gen(fields, plan)
        return self._post('add_plan/%s' % project_id, payload)

    # can't @UpdateCache b/c it doesn't include project_id
    def add_plan_entry(self, plan_entry):
        fields = ['suite_id', 'name', 'description', 'assignedto_id',
                  'include_all', 'case_ids', 'config_ids', 'runs']
        fields.extend(self._custom_field_discover(plan_entry))

        plan_id = plan_entry.get('plan_id')
        payload = self._payload_gen(fields, plan_entry)
        return self._post('add_plan_entry/%s' % plan_id, payload)

    # Run Requests
    def runs(self, project_id=None, completed=None):
        project_id = project_id or self._project_id
        if self._refresh(self._runs[project_id]['ts']):
            # get new value, if request is good update value with new ts.
            endpoint = 'get_runs/%s' % project_id
            if completed is not None:
                endpoint += '&is_completed=%s' % str(int(completed))
            self._runs[project_id]['value'] = self._paginate_request(endpoint, {}, "runs")
            self._runs[project_id]['ts'] = datetime.now()
        return self._runs[project_id]['value']

    def run_with_id(self, run_id):
        try:
           return list(filter(lambda x: x['id'] == run_id, self.runs()))[0]
        except IndexError:
            raise TestRailError("Run ID '%s' was not found" % run_id)

    @UpdateCache(_shared_state['_runs'])
    def add_run(self, run):
        fields = ['name', 'description', 'suite_id', 'milestone_id',
                  'assignedto_id', 'include_all', 'case_ids']
        fields.extend(self._custom_field_discover(run))

        project_id = run.get('project_id')
        payload = self._payload_gen(fields, run)
        return self._post('add_run/%s' % project_id, payload)

    @UpdateCache(_shared_state['_runs'])
    def update_run(self, run):
        fields = [
            'name', 'description', 'milestone_id', 'include_all', 'case_ids']
        fields.extend(self._custom_field_discover(run))

        data = self._payload_gen(fields, run)
        return self._post('update_run/%s' % run.get('id'), data)

    @UpdateCache(_shared_state['_runs'])
    def close_run(self, run_id):
        return self._post('close_run/%s' % run_id)

    @UpdateCache(_shared_state['_runs'])
    def delete_run(self, run_id):
        return self._post('delete_run/%s' % run_id)

    @UpdateCache(_shared_state['_plans'])
    def add_plan(self, plan):
        fields = ['name', 'description', 'milestone_id']
        fields.extend(self._custom_field_discover(plan))

        project_id = plan.get('project_id')
        payload = self._payload_gen(fields, plan)
        return self._post('add_plan/%s' % project_id, payload)

    @UpdateCache(_shared_state['_plans'])
    def update_plan(self, plan):
        fields = ['name', 'description', 'milestone_id']
        fields.extend(self._custom_field_discover(plan))

        data = self._payload_gen(fields, plan)
        return self._post('update_plan/%s' % plan.get('id'), data)

    @UpdateCache(_shared_state['_plans'])
    def close_plan(self, plan_id):
        return self._post('close_plan/%s' % plan_id)

    @UpdateCache(_shared_state['_plans'])
    def delete_plan(self, plan_id):
        return self._post('delete_plan/%s' % plan_id)

    # Test Requests
    def tests(self, run_id):
        if self._refresh(self._tests[run_id]['ts']):
            endpoint = 'get_tests/%s' % run_id
            self._tests[run_id]['value'] = self._paginate_request(endpoint, {}, "tests")
            self._tests[run_id]['ts'] = datetime.now()
        return self._tests[run_id]['value']

    def test_with_id(self, test_id, run_id=None):
        if run_id is not None:
            try:
                return list(filter(lambda x: x['id'] == test_id, self.tests(run_id)))[0]
            except IndexError:
                raise TestRailError("Test ID '%s' was not found" % test_id)
        else:
            try:
                return self._get('get_test/%s' % test_id)
            except TestRailError:
                raise TestRailError("Test ID '%s' was not found" % test_id)

    # Result Requests
    def results_by_run(self, run_id):
        if self._refresh(self._results[run_id]['ts']):
            endpoint = 'get_results_for_run/%s' % run_id
            self._results[run_id]['value'] = self._paginate_request(endpoint, {}, "results")
            self._results[run_id]['ts'] = datetime.now()
        return self._results[run_id]['value']

    def results_by_test(self, test_id):
        if self._refresh(self._results[test_id]['ts']):
            endpoint = 'get_results/%s' % test_id
            self._results[test_id]['value'] = self._paginate_request(endpoint, {}, "results")
            self._results[test_id]['ts'] = datetime.now()
        return self._results[test_id]['value']

    @UpdateCache(_shared_state['_results'])
    def add_result(self, data):
        fields = ['status_id',
                  'comment',
                  'version',
                  'elapsed',
                  'defects',
                  'assignedto_id']
        fields.extend(self._custom_field_discover(data))

        payload = self._payload_gen(fields, data)
        payload['elapsed'] = str(payload['elapsed']) + 's'
        result = self._post('add_result/%s' % data['test_id'], payload)

        # Need to update the _tests cache to mark the run for refresh
        for run in self._tests:
            for test in self._tests[run]['value']:
                if test['id'] == data['test_id']:
                    self._tests[run]['ts'] = None
                    return result
        else:
            raise TestRailError("Could not find test '%s' in cache to update" % data['test_id'])

    @UpdateCache(_shared_state['_results'])
    def add_results(self, results, run_id):
        fields = ['status_id',
                  'test_id',
                  'comment',
                  'version',
                  'elapsed',
                  'defects',
                  'assignedto_id']

        payload = {'results': list()}
        for result in results:
            custom_field = fields + self._custom_field_discover(result)
            payload['results'].append(self._payload_gen(custom_field + fields, result))

        payload['elapsed'] = str(payload['elapsed']) + 's'
        response = self._post('add_results/%s' % run_id, payload)

        # Need to update the _tests cache to mark the run for refresh
        self._tests[run_id]['ts'] = None

        return response

    def _custom_field_discover(self, entity):
        return [field for field in entity.keys() if field.startswith('custom_')]

    # Status Requests
    def statuses(self):
        if self._refresh(self._statuses['ts']):
            _statuses = self._get('get_statuses')
            self._statuses['value'] = _statuses
            self._statuses['ts'] = datetime.now()
        return self._statuses['value']

    def status_with_id(self, status_id):
        try:
            return list(filter(lambda x: x['id'] == status_id, self.statuses()))[0]
        except IndexError:
            raise TestRailError("Status ID '%s' was not found" % status_id)

    def configs(self):
        if self._refresh(self._configs['ts']):
            _configs = self._get('get_configs/%s' % self._project_id)
            self._configs['value'] = _configs
            self._configs['ts'] = datetime.now()
        return self._configs['value']

    @retry(ServiceUnavailableError, tries=30, delay=10)
    @retry((TooManyRequestsError, ValueError), tries=3, delay=1, backoff=2)
    def _get(self, uri, params=None):
        uri = '/index.php?/api/v2/%s' % uri
        r = requests.get(self._url+uri, params=params, auth=self._auth,
                         headers=self.headers, verify=self.verify_ssl)

        self._raise_on_429_or_503_status(r)

        if r.status_code == 200:
            return r.json()
        else:
            try:
                response = r.json()
            except ValueError:
                response = dict()

            response.update({'response_headers': str(r.headers),
                             'payload': params,
                             'url': r.url,
                             'status_code': r.status_code,
                             'error': response.get('error', None)})
            raise TestRailError(response)

    @retry(ServiceUnavailableError, tries=30, delay=10)
    @retry(TooManyRequestsError, tries=3, delay=1, backoff=2)
    def _post(self, uri, data={}):
        uri = '/index.php?/api/v2/%s' % uri
        r = requests.post(self._url+uri, json=data, auth=self._auth,
                          verify=self.verify_ssl)

        self._raise_on_429_or_503_status(r)

        if r.status_code == 200:
            try:
                return r.json()
            except ValueError:
                return dict()
        else:
            try:
                response = r.json()
            except ValueError:
                response = dict()

            response.update({'post_data': data,
                             'response_headers': str(r.headers),
                             'url': r.url,
                             'status_code': r.status_code,
                             'error': response.get('error', None)})
            raise TestRailError(response)

    def _payload_gen(self, fields, data):
        payload = dict()
        for field in fields:
            if data.get(field) is not None:
                payload[field] = data.get(field)
        return payload
