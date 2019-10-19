# switchsd
A tool to automatically download the latest versions of the required sd files for Atmosphere

## Usage:

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

## Credits:

- nh-server.github.io/switch-guide/
- Folk of #trusted who approved the idea and fools of #switch-assistance who inspired me to write this
- Ofcourse everyone in the switch hacking scene that made Atmosphere possible in the first place
