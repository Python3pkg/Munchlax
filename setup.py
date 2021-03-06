from setuptools import setup

setup(
    name='munchlax',
    version='0.1.4',
    description='Asynchronous Slack library for Python 3.4+',
    long_description='Asynchronous Slack library for Python 3.4+',
    url='https://github.com/WildAndrewLee/Munchlax',
    author='reticence',
    author_email='andrew@reticent.io',
    license='WTFPL',
    packages=['munchlax', 'munchlax.lib'],
    zip_safe=False,
    install_requires=['slackclient']
)