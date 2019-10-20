# switchsd
A tool to automatically download the latest versions of the required sd files for Atmosphere

## Direct Usage:

- First ensure that you have a python 3+ distribution
- Then run the following command to install the requests library
```bash
$ pip install requests
```
- If you wish to run emuMMC on your switch, run the following command to generate the appropriate sd files:
```bash
$ python switchsd.py
```
- However, if you wish to run Atmosphere purely on sysnand because of space constraints, run the following command:
```bash
$ python switchsd.py --sys
```
- The download should take a few minutes. Once completed, you will see a `switchsd` directory in the same directory as the script
- Copy all the contents of that folder to the root of your sd card and you are good to go!

## Optional: GitHub OAuth token

- You can add a GitHub OAuth personal token by going to https://github.com/settings/tokens and generating a new token
- You do not need to give it any permissions. Just generate a token to use with the application
- This lets you make 5000 API requests per hour as opposed to 60 with unauthenticated access. 
- This script is coded to work with both authenticated and unauthenticated access.

## Serving the application via Flask

- This requires a linux based server. 
- Make sure your `python3` and `python3-pip` installations are in order
- Install flask using the following command:
```bash
$ pip3 install flask
```
- You can then run the application by running:
```bash
$ python3 app.py
```
- You can then download the sd files from the following URLs:
```
EMUNAND: <external-IP>/emunand
SYSNAND: <external-IP>/sysnand
```


## Credits:

- nh-server.github.io/switch-guide/
- Folk of #trusted who approved the idea and fools of #switch-assistance who inspired me to write this
- Ofcourse everyone in the switch hacking scene that made Atmosphere possible in the first place
