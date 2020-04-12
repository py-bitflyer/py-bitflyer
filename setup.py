from setuptools import setup


requires = [
    'requests',
    'websocket-client'
]


setup(
    name='py_bitflyer',
    version='0.1.3',
    description='A Python wrapper for bitFlyer API.',
    url='https://github.com/py-bitflyer/py-bitflyer',
    license='MIT License',
    packages=['py_bitflyer'],
    install_requires=requires
)
