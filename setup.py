from setuptools import setup
import os

setup(
    name='locationservice',
    packages=['locationservice'],
    include_package_data=True,
    install_requires=[
        'flask',
	'boto3'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)

credfile = open(os.environ.get('HOME') + '/.aws/credentials', 'w')
configfile = open(os.environ.get('HOME') + '/.aws/config', 'w')

credfile.write('[default]\n')
credfile.write('aws_access_key_id = AKIAJ3TRHNMNVYAJV75Q\n')
credfile.write('aws_secret_access_key = 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\n')
credfile.close()

configfile.write('[default]\n')
configfile.write('region=us-east-1\n')
configfile.close()
