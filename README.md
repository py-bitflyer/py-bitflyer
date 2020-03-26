# pybf

A Python wrapper for bitFlyer API.

## Install

```
$ pip3 install git+https://github.com/tapioka324/pybf.git
```

## For Usage
```python
from pybf import api


pybf_ = api.API()
# Get markets informations
pybf_.markets() 

# Get executions
# If you want 10 executions, pass count as a variable
pybf_.markets(count=10)

```
