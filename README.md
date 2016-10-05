# TestRail Python Library
[![Build Status](https://travis-ci.org/travispavek/testrail-python.svg?branch=master)](https://travis-ci.org/travispavek/testrail-python)
[![Coverage Status](https://coveralls.io/repos/github/travispavek/testrail-python/badge.svg?branch=master)](https://coveralls.io/github/travispavek/testrail-python?branch=master) [![PyPI version](https://badge.fury.io/py/testrail.svg)](https://badge.fury.io/py/testrail)

This Python Library allows you to easily publish results and manage your TestRail instance.

### Warning
This library is still in beta.  This means little to no testing and future releases may break compatibility.  Please evaluate and report bugs/enhancements.

## Quick Start
```python
from testrail import TestRail

testrail = TestRail(project_id=1)
milestone = testrail.milestone('rel-2.3')
milestone.is_completed = True
testrail.update(milestone)
```

For a more indepth example, see the [examples folder](examples/)


#### Configuration
Create '.testrail.conf' in your home directory with the following:
```
testrail:
    user_email: 'your email address'
    user_key: 'your API key or password'
    url: 'domain for TestRail instance'
```

You can override the config file with the following environment variables:

* TESTRAIL_USER_EMAIL
* TESTRAIL_USER_KEY
* TESTRAIL_URL

## Installation
The easiest and recommended way to install testrail is through [pip](https://pip.pypa.io):
```
$ pip install testrail
```

This will handle the client itself as well as any requirements.

## Usage
Full documentation will hopefully be available soon.  In the mean time, skimming over client.py should give you a good idea of how things work.

**Important:** For performance reasons, response content is cached for 30 seconds.  This can be adjusted by changing the timeout in api.py.  Setting it to zero is not recommended and will probably annoy you to no end!
