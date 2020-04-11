# pybf

A Python wrapper for [bitFlyer API](https://lightning.bitflyer.com/docs#http-api).

## Install

```
$ pip3 install git+https://github.com/tapioka324/pybf.git
```

## For Usage

### For public_api
```python
import pybf


public_api = pybf.API()

# Get markets informations
public_api.markets() 

# Get executions
# If you want 10 executions, pass count as a variable
public_api.executions(count=10)
```

### For private_api  
Create config.json under the `/pybf`. And write down your *APIKey* and *APISecret*.  
(!Atention)  
 This config.json has very very secret infomation of your bitflyer account. This repository has been set not to upload "config.json" in .gitignore.

`/path/to/config.json`
```json
{
    "Key" : "Your APIKey",
    "Secret" : "Your APISecret"
}
```

```python
import pybf


private_api = pybf.API(mode='Private', config=config_path)

# Get balance
private_api.balance()

# Get a list of own executions
private_api.childorders_list()
```
