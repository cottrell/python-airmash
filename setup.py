from setuptools import setup
setup(
    name='airmash',
    packages=['airmash'],  # this must be the same as the name above
    version='0.0.1',
    description='A Python client for the game AIRMASH',
    author='Phil Howard',
    author_email='phil@gadgetoid.com',
    url='https://github.com/gadgetoid/python-airmash',  # use the URL to the github repo
    classifiers=[],
    install_requires=[
        # 'construct',
        'argh',
        'names'
    ],
    dependency_links=[
        # 'git@github.com:construct/construct.git',
        'git+https://github.com/construct/construct.git'
        ],

)
