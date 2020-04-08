from setuptools import setup

setup(
    name = 'gas',
    version = '1.0',
    packages = ['gas'],
    entry_points = {
        'console_scripts': [
            'gas = gas.__main__:main'
        ]
    })