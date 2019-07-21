# Waste Flooding
Phishing Retaliation Tool

## Requirements
  - Install [Python 3.7.4](https://www.python.org/downloads/) (last version)
  - Pip will be installed as default
#### Install the following libraries using pip:
 ```python
pip install gevent
pip install requests
pip install lxml
```

# Usage
To use the tool, just run the command from the starting folder (replacing URL with the target):
 ```python
python waste.py URL
```

#### Verbose usage
If you want to see the attack structure, just add "-v" or "-verbose" to your call:
 ```python
python waste.py URL -v
```
OR
 ```python
python waste.py URL -verbose
```


## Big Thanks:
  - [Placidina](https://github.com/Placidina) for the [GetProxies](https://github.com/Placidina/GetProxies) - I am still integrating other calls on the tool, but I want to thank you in advance
