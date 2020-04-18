from setuptools import setup

setup(
    name = 'gas',
    version = '0.1.0',
    packages = ['gas','gas.utils','gas.common'],
    entry_points = {
        'console_scripts': [
            'gas = gas.__main__:main'
        ]
    })