from setuptools import setup


with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

requires = [
    'requests',
    'websocket-client'
]


setup(
    name='py_bitflyer',
    version='0.1.3',
    description='A Python wrapper for bitFlyer API.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/py-bitflyer/py-bitflyer',
    license='MIT License',
    packages=['py_bitflyer'],
    install_requires=requires,
    keywords='bitflyer',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ]
)
