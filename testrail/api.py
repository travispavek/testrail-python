from __future__ import division

import os
import collections
from builtins import dict
from datetime import datetime, timedelta

import yaml
import requests

from testrail.helper import TestRailError

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
        project_id = update_obj['project_id']

        if not self.cache[project_id]['ts']:
            # The cache will clear on the next read, so no reason to add/update
            return

        obj_list = self.cache[project_id]['value']
        for index, obj in enumerate(obj_list):
            if obj['id'] == update_obj['id']:
                obj_list[index] = update_obj
                return
        else:
            # If we get this far, it means we searched all objects without
            # finding a match. Add the object
            obj_list.append(update_obj)
            obj_list.sort(key=lambda x: x['id'])

            return


class API(object):
    _ts = datetime.now() - timedelta(days=1)
    _shared_state = {'_users': nested_dict(),
                     '_projects': nested_dict(),
                     '_plans': nested_dict(),
                     '_cases': nested_dict(),
                     '_runs': nested_dict(),
                     '_suites': nested_dict(),
                     '_milestones': nested_dict(),
                     '_priorities': nested_dict(),
                     '_case_types': nested_dict(),
                     '_sections': nested_dict(),
                     '_results': nested_dict(),
                     '_statuses': nested_dict(),
                     '_tests': nested_dict(),
                     '_configs': nested_dict(),
                     '_timeout': 30,
                     '_project_id': None}

    def __init__(self):
        self.__dict__ = self._shared_state
        config = self._conf()
        self._auth = (config['email'], config['key'])
        self._url = config['url']
        self.headers = {'Content-Type': 'application/json'}

    def _conf(self):
        TR_EMAIL = 'TESTRAIL_USER_EMAIL'
        TR_KEY = 'TESTRAIL_USER_KEY'
        TR_URL = 'TESTRAIL_URL'

        conf_path = '%s/.testrail.conf' % os.path.expanduser('~')

        if os.path.isfile(conf_path):
            with open(conf_path, 'r') as f:
                config = yaml.load(f)
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

        return {'email': _email, 'key': _key, 'url': _url}

    def _refresh(self, ts):
        if not ts:
            return True

        td = (datetime.now() - ts)
        since_last =  (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6

        return since_last > self._timeout

    @classmethod
    def flush_cache(cls):
        """ Set all cache objects to refresh
        """
        for cache in cls._shared_state.values():
            if not isinstance(cache, dict):
                continue
            elif 'ts' in cache:
                cache['ts'] = None

            for project in cache.values():
                if isinstance(project, dict) and 'ts' in project:
                    project['ts'] = None

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
            self._projects['value'] = self._get('get_projects')
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

    # Case Requests
    def cases(self, project_id=None, suite_id=10):
        project_id = project_id or self._project_id
        if self._refresh(self._cases[project_id][suite_id]['ts']):
            # get new value, if request is good update value with new ts.
            params = {'suite_id': suite_id} if suite_id != -1 else None
            _cases = self._get('get_cases/%s' % project_id, params=params)
            self._cases[project_id][suite_id]['value'] = _cases
            self._cases[project_id][suite_id]['ts'] = datetime.now()
        return self._cases[project_id][suite_id]['value']

    def case_with_id(self, case_id):
        try:
            return list(filter(lambda x: x['id'] == case_id, self.cases()))[0]
        except IndexError:
            raise TestRailError("Case ID '%s' was not found" % case_id)

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
            _milestones = self._get('get_milestones/%s' % project_id)
            self._milestones[project_id]['value'] = _milestones
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
        project_id = milestone.get('project_id')
        payload = self._payload_gen(fields, milestone)
        return self._post('add_milestone/%s' % project_id, payload)

    @UpdateCache(_shared_state['_milestones'])
    def update_milestone(self, milestone):
        fields = ['name', 'description', 'due_on', 'is_completed']
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
            _sections = self._get(
                'get_sections/%s' % project_id, params=params)
            self._sections[project_id][suite_id]['value'] = _sections
            self._sections[project_id][suite_id]['ts'] = datetime.now()
        return self._sections[project_id][suite_id]['value']

    def section_with_id(self, section_id):
        try:
            return list(filter(lambda x: x['id'] == section_id, self.sections()))[0]
        except IndexError:
            raise TestRailError("Section ID '%s' was not found" % section_id)

    # Plan Requests
    def plans(self, project_id=None):
        project_id = project_id or self._project_id
        if self._refresh(self._plans[project_id]['ts']):
            # get new value, if request is good update value with new ts.
            _plans = self._get('get_plans/%s' % project_id)
            self._plans[project_id]['value'] = _plans
            self._plans[project_id]['ts'] = datetime.now()
        return self._plans[project_id]['value']

    def plan_with_id(self, plan_id):
        try:
            return list(filter(lambda x: x['id'] == plan_id, self.plans()))[0]
        except IndexError:
            return list()

    # Run Requests
    def runs(self, project_id=None, completed=None):
        project_id = project_id or self._project_id
        if self._refresh(self._runs[project_id]['ts']):
            # get new value, if request is good update value with new ts.
            end_point = 'get_runs/%s' % project_id
            if completed is not None:
                end_point += '&is_completed=%s' % str(int(completed))
            _runs = self._get(end_point)
            self._runs[project_id]['value'] = _runs
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
        project_id = run.get('project_id')
        payload = self._payload_gen(fields, run)
        return self._post('add_run/%s' % project_id, payload)

    @UpdateCache(_shared_state['_runs'])
    def update_run(self, run):
        fields = [
            'name', 'description', 'milestone_id', 'include_all', 'case_ids']
        data = self._payload_gen(fields, run)
        return self._post('update_run/%s' % run.get('id'), data)

    @UpdateCache(_shared_state['_runs'])
    def close_run(self, run_id):
        return self._post('close_run/%s' % run_id)

    @UpdateCache(_shared_state['_runs'])
    def delete_run(self, run_id):
        return self._post('delete_run/%s' % run_id)

    # Test Requests
    def tests(self, run_id):
        if self._refresh(self._tests[run_id]['ts']):
            _tests = self._get('get_tests/%s' % run_id)
            self._tests[run_id]['value'] = _tests
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
    def results(self, test_id):
        if self._refresh(self._results[test_id]['ts']):
            _results = self._get('get_results/%s' % test_id)
            self._results[test_id]['value'] = _results
            self._results[test_id]['ts'] = datetime.now()
        return self._results[test_id]['value']

    def add_result(self, data):
        fields = ['status_id',
                  'comment',
                  'version',
                  'elapsed',
                  'defects',
                  'assignedto_id']

        payload = self._payload_gen(fields, data)
        self._post('add_result/%s' % data['test_id'], payload)

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
            payload['results'].append(self._payload_gen(fields, result))
        self._post('add_results/%s' % run_id, payload)

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

    def _get(self, uri, params=None):
        uri = '/index.php?/api/v2/%s' % uri
        r = requests.get(self._url+uri, params=params, auth=self._auth,
                         headers=self.headers)
        content = r.json()
        if r.status_code == 200:
            return content
        else:
            content.update({'payload': params,
                            'url': r.url,
                            'status_code': r.status_code,
                            'error': content.get('error', None)})
            raise TestRailError(content)

    def _post(self, uri, data={}):
        uri = '/index.php?/api/v2/%s' % uri
        r = requests.post(self._url+uri, json=data, auth=self._auth)
        # TODO if 429 wait 5 seconds and try again.
        if r.status_code == 200:
            try:
                return r.json()
            except ValueError:
                return {}
        else:
            response = r.json()
            response.update({'data': data,
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
