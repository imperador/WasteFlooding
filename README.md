# Waste Flooding
Phishing Retaliation Tool

## Requirements
  - Install [Python 3.7.4](https://www.python.org/downloads/) (last version)
  - Pip will be installed by default
  
### Install the following libraries using pip:
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

### Options
#### -v or -verbose
If you want to see the attack structure, just add "-v" or "-verbose" to your call:
 ```python
python waste.py URL -v
python waste.py URL -verbose
```
#### -min and -max
To define custom minimum and maximum waiting time, just add "-min" and/or "-max", respectively, followed by desired values (in seconds):
 ```python
python waste.py URL -min 0 -max 5000
python waste.py URL -min 5
python waste.py URL -max 5000
```
#### -r 
To reset proxy list, just add "-r" as argument. You don't need to pass an URL if you only want to reset your proxy collection:
 ```python
python waste.py URL -r
python waste.py -r
```

## Big Thanks:
  - [Placidina](https://github.com/Placidina) for the [GetProxies](https://github.com/Placidina/GetProxies) - I am still integrating other calls on the tool, but I want to thank you in advance
