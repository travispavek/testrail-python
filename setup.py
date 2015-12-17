from distutils.core import setup

setup(
    name = 'testrail',
    packages = ['testrail'],
    version = '0.1a',
    description = 'Python library for interacting with TestRail via REST APIs.',
    author = 'Travis Pavek',
    author_email = 'travis.pavek@gmail.com',
    url = 'https://github.com/travispavek/testrail',
    download_url = 'https://github.com/travispavek/testrail/tarball/0.1',
    keywords = ['testrail', 'api', 'client', 'library', 'rest'],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
)
