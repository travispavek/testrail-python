from setuptools import setup

setup(
    name = 'testrail',
    packages = ['testrail'],
    version = '0.2.1',
    description = 'Python library for interacting with TestRail via REST APIs.',
    author = 'Travis Pavek',
    author_email = 'travis.pavek@gmail.com',
    url = 'https://github.com/travispavek/testrail-python',
    download_url = 'https://github.com/travispavek/testrail-python/tarball/0.2.0',
    keywords = ['testrail', 'api', 'client', 'library', 'rest'],
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Quality Assurance',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
