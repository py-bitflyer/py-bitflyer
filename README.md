# py-bitflyer

A Python wrapper for [bitFlyer API](https://lightning.bitflyer.com/docs#http-api).

## Install

```
$ pip install git+https://github.com/py-bitflyer/py-bitflyer.git
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
Create config.json and write down your *APIKey* and *APISecret*.
(!Atention!)
 This config.json has very very secret infomation of your bitflyer account.

`/path/to/config.json`
```json
{
    "Key" : "Your APIKey",
    "Secret" : "Your APISecret"
}
```

```python
import pybf


private_api = pybf.API(mode='Private', config='/path/to/config.json')

# Get balance
private_api.balance()

# Get a list of own executions
private_api.childorders_list()
```
