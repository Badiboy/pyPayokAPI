[![PyPi Package Version](https://img.shields.io/pypi/v/pyPayokAPI.svg)](https://pypi.python.org/pypi/pyPayokAPI)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/pyPayokAPI.svg)](https://pypi.python.org/pypi/pyPayokAPI)
[![PyPi downloads](https://img.shields.io/pypi/dm/pyPayokAPI.svg)](https://pypi.org/project/pyPayokAPI/)

# <p align="center">pyPayokAPI</p>
Python implementation of [Payok.io](https://payok.io) public [API](https://payok.io/cabinet/documentation/doc_main.php)

**This library may not fully implement API. However I will continue to maintain it, so if you need some not implemented methods - just open an issue.**

# Installation
Installation using pip (a Python package manager):
```
$ pip install pyPayokAPI
```

# Usage
Everything is as simple as the [API](https://payok.io/cabinet/documentation/doc_main.php) itself.
1. Create pyPayokAPI instance
2. Access API methods
3. Most methods return result as correspondent class, so you can access data as fields 
```
from pyPayokAPI import pyPayokAPI
client = pyPayokAPI(
    xxxx,        # API ID
    "xxxxxxx")   # API key
balance = client.balance()
print("Balance: {}\nRef.balance: {}".format(balance.balance, balance.ref_balance))
```
You can also check tests.py.

# Exceptions
Exceptions are rised using pyPayokAPIException class.
