from setuptools import setup
import os


setup(
    name='locationservice',
    packages=['locationservice'],
    include_package_data=True,
    install_requires=[
        'flask',
        'requests',
	    'boto3'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)