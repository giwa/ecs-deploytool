from setuptools import setup


setup(
    name='ecs-deploytool',
    version='0.0.1',
    py_modules=['ecs_deploytool'],
    packages=['ecs_deploytool'],
    install_requires=[
        'Click',
        'boto3'
        ],
    entry_points='''
        [console_scripts]
        ecs-deploytool=ecs_deploytool:cli
    '''
    )
