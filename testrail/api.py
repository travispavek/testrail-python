from datetime import datetime, timedelta
import requests
import collections
from os.path import expanduser
import yaml
from helper import TestRailError
nested_dict = lambda: collections.defaultdict(nested_dict)


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
        with open('%s/.testrail-python-client.conf' % expanduser('~'), 'r') as f:
            config = yaml.load(f)
        self._auth = (config['testrail']['user_email'], config['testrail']['user_pass'])
        self._url = config['testrail']['url']
        self.headers = {'Content-Type': 'application/json'}

    def _refresh(self, ts):
        if not ts:
            return True
        return (datetime.now() - ts).total_seconds() > self._timeout

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
        return filter(lambda x: x['id'] == user_id, self.users())[0]

    def user_with_email(self, user_email):
        return filter(lambda x: x['email'] == user_email, self.users())[0]

    # Project Requests
    def projects(self):
        if self._refresh(self._projects['ts']):
            # get new value, if request is good update value with new ts.
            self._projects['value'] = self._get('get_projects')
            self._projects['ts'] = datetime.now()
        return self._projects['value']

    def project_with_id(self, project_id):
        return filter(lambda x: x['id'] == project_id, self.projects())[0]

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
            return filter(lambda x: x['id'] == suite_id, self.suites())[0]
        except IndexError:
            return None

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
        return filter(lambda x: x['id'] == case_id, self.cases())[0]

    def case_types(self):
        if self._refresh(self._case_types['ts']):
            # get new value, if request is good update value with new ts.
            _case_types = self._get('get_case_types')
            self._case_types['value'] = _case_types
            self._case_types['ts'] = datetime.now()
        return self._case_types['value']

    def case_type_with_id(self, case_type_id):
        try:
            return filter(lambda x: x['id'] == case_type_id, self.case_types())[0]
        except IndexError:
            return None

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
                return filter(lambda x: x['id'] == milestone_id, self.milestones(project_id))[0]
            except IndexError:
                return None

    def add_milestone(self, milestone):
        fields = ['name', 'description', 'due_on']
        project_id = milestone.get('project_id')
        payload = self._payload_gen(fields, milestone)
        self._post('add_milestone/%s' % project_id, payload)

    def update_milestone(self, milestone):
        fields = ['name', 'description', 'due_on', 'is_completed']
        data = self._payload_gen(fields, milestone)
        self._post('update_milestone/%s' % milestone.get('id'), data)

    def delete_milestone(self, milestone_id):
        self._post('delete_milestone/%s' % milestone_id)

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
            return filter(lambda x: x['id'] == priority_id, self.priorities())[0]
        except IndexError:
            return None

    # Section Requests
    def sections(self, project_id, suite_id=-1):
        if self._refresh(self._sections[project_id][suite_id]['ts']):
            params = {'suite_id': suite_id} if suite_id != -1 else None
            _sections = self._get('get_sections/%s' % project_id, params=params)
            self._sections[project_id][suite_id]['value'] = _sections
            self._sections[project_id][suite_id]['ts'] = datetime.now()
        return self._sections[project_id][suite_id]['value']

    def section_with_id(self, section_id):
        try:
            return filter(lambda x: x['id'] == section_id, self.sections())[0]
        except IndexError:
            return None

    # Plan Requests
    def plans(self, project_id):
        if self._refresh(self._plans[project_id]['ts']):
            # get new value, if request is good update value with new ts.
            _plans = self._get('get_plans/%s' % project_id)
            self._plans[project_id]['value'] = _plans
            self._plans[project_id]['ts'] = datetime.now()
        return self._plans[project_id]['value']

    def plan_with_id(self, plan_id):
        return self._get('get_plan/%s' % plan_id)
        # try:
        #     return filter(lambda x: x['id'] == plan_id, self.plans())[0]
        # except IndexError:
        #     return None

    # Run Requests
    def runs(self, project_id):
        if self._refresh(self._runs[project_id]['ts']):
            # get new value, if request is good update value with new ts.
            _runs = self._get('get_runs/%s' % project_id)
            self._runs[project_id]['value'] = _runs
            self._runs[project_id]['ts'] = datetime.now()
        return self._runs[project_id]['value']

    def run_with_id(self, run_id):
        try:
            return filter(lambda x: x['id'] == run_id, self.runs())[0]
        except IndexError:
            return None

    # Test Requests
    def tests(self, run_id):
        if self._refresh(self._tests[run_id]['ts']):
            _tests = self._get('get_tests/%s' % run_id)
            self._tests[run_id]['value'] = _tests
            self._tests[run_id]['ts'] = datetime.now()
        return self._tests[run_id]['value']

    def test_with_id(self, test_id):
        try:
            return filter(lambda x: x['id'] == test_id, self.tests())[0]
        except IndexError:
            return None

    # Result Requests
    def results(self, test_id):
        if self._refresh(self._results[test_id]['ts']):
            _results = self._get('get_results/%s' % test_id)
            self._results[test_id]['value'] = _results
            self._results[test_id]['ts'] = datetime.now()
        return self._results[test_id]['value']

    def add_result(self, data):
        fields = ['status_id', 'comment', 'version', 'elapsed', 'defects', 'assignedto_id']
        payload = self._payload_gen(fields, data)
        self._post('add_result/%s' % data['test_id'], payload)

    def add_results(self, results, run_id):
        fields = ['status_id', 'test_id', 'comment', 'version', 'elapsed', 'defects', 'assignedto_id']
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
            return filter(lambda x: x['id'] == status_id, self.statuses())[0]
        except IndexError:
            return None

    def configs(self):
        if self._refresh(self._configs['ts']):
            _configs = self._get('get_configs/%s' % self._project_id)
            self._configs['value'] = _configs
            self._configs['ts'] = datetime.now()
        return self._configs['value']

    def _get(self, uri, params=None):
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
        r = requests.post(self._url+uri, json=data, auth=self._auth)
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
