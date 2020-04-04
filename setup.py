from setuptools import setup


requires = [
    'requests',
    'websocket-client'
]


setup(
    name='pybf',
    version='0.1.3',
    description='A Python wrapper for bitFlyer API.',
    url='https://github.com/tapioka324/pybf',
    license='MIT License',
    packages=['pybf'],
    install_requires=requires
)
