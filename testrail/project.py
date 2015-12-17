class Project(object):
    def __init__(self, response={}):
        self._content = response

    @property
    def announcement(self):
        """The description/announcement of the project"""
        return self._content.get('annoucement')

    @announcement.setter
    def announcement(self, value):
        # ToDo verify value is string
        self._content['announcement'] = value

    @property
    def completed_on(self):
        """The date/time when the project was marked as completed"""
        # ToDo convert to datetime?
        return self._content.get('completed_on')

    @completed_on.setter
    def completed_on(self, value):
        # ToDo figure out what type should be and convert to unix timestamp
        self._content['completed_on'] = value

    @property
    def id(self):
        """The unique ID of the project"""
        return self._content.get('id')

    @id.setter
    def id(self, value):
        self._content['id'] = value

    @property
    def is_completed(self):
        """True if the project is marked as completed and false otherwise"""
        return self._content.get('is_completed', False)

    @is_completed.setter
    def is_completed(self, value):
        self._content['is_completed'] = value

    @property
    def name(self):
        """The name of the project"""
        return self._content.get('name')

    @name.setter
    def name(self, value):
        # ToDo verity it is a string?
        self._content['name'] = value

    @property
    def show_announcement(self):
        """True to show the announcement/description and false otherwise"""
        return self._content.get('show_announcement', False)

    @show_announcement.setter
    def show_announcement(self, value):
        # Verify boolean
        self._content['show_announcement'] = value

    @property
    def suite_mode(self):
        """The suite mode of the project (1 for single suite mode,
           2 for single suite + baselines, 3 for multiple suites)
           (added with TestRail 4.0)
        """
        return self._content.get('suite_mode')

    @suite_mode.setter
    def suite_mode(self, value):
        self._content['suite_mode'] = value

    @property
    def url(self):
        """The address/URL of the project in the user interface"""
        return self._content.get('url')

    @url.setter
    def url(self, value):
        self._content['url'] = value
