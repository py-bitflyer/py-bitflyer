# pybf

A Python wrapper for bitFlyer API.

## Install

```
$ pip3 install git+https://github.com/tapioka324/pybf.git
```

## For Usage
```python
from pybf import api


public_api = api.API()
# Get markets informations
public_api.markets() 

# Get executions
# If you want 10 executions, pass count as a variable
public_api.executions(count=10)

```
