# py-bitflyer

A Python wrapper for [bitFlyer API](https://lightning.bitflyer.com/docs#http-api).

## Install

```bash
$ pip install py-bitflyer
```

## For Usage

### For public_api
```python
import py_bitflyer


public_api = py_bitflyer.API()

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
import py_bitflyer


private_api = py_bitflyer.API(mode='Private', config='/path/to/config.json')

# Get balance
private_api.balance()

# Get a list of own executions
private_api.childorders_list()
```
