from distutils.core import setup

setup(
    name='battery',
    version='0.1',
    description='Build several Python versions to aim at your software',
    author='Brandon Craig Rhodes',
    author_email='brandon@rhodesmill.org',
    #url='',
    packages=['battery'],
    entry_points={'console_scripts': [
            'battery = battery.command:main',
            ]}
    )
