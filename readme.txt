## RM Control
RM Control is an app to control an RM2 by BroadLink.  It allows users to learn IR and RF codes, store them, and fire them.

### Components
1. vue.js front-end
2. python back-end
3. process watcher by supervisord

### Requirements
1. `build-essential`
2. `libavahi-compat-libdnssd-dev`
3. `nodejs` (>6.0.0)
4. `node-gyp`
5. `python` (2.7)

### Installation
1. `git clone https://github.com/ericmagnuson/rmcontrol.git && cd rmcontrol`
2. `python setup.py install`
3. `export FLASK_APP=rmcontrol; python -m flask initdb`
4. `python run.py`

RM Control can be interacted with by visiting the included web interface found at http://127.0.0.1:5000 or by talking directly with the API as described farther below.

### VM Initialization (Under construction.)
1. `curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh`
2. `sudo bash nodesource_setup.sh`
3. `sudo apt-get update`
4. `sudo apt-get install build-essential git libavahi-compat-libdnssd-dev nodejs node-gyp python-setuptools python-pip`
5. `pip install pycrypto`
6. `sudo reboot now`
7. `sudo npm install -g --unsafe-perm request homebridge homebridge-httpmulti`
8. To install RM Control, follow the steps in Installation above.
9. Using Homebridge-HttpMulti, configure Homebridge to send commands to the RM Control API. See `config.json.sample` for an example.

### Supervisor Setup
1. `sudo apt-get install supervisor`
2. In `/etc/supervisor/conf.d/`, add two configuration files, `rmcontrol.conf` and `homebridge.conf`. See sample files for help.
3. `sudo service supervisor reload`

### API Documentation

`GET /`

Shows all commands.

`POST / {name: <name>}`

Listens for a command from the RM2, and if a command is received, it will be saved with the given name.

`POST /<name>`

Fire the given command.

`PATCH /<name> {name: <name?>, code: <code?>}`

Edit the requested command by passing in a new name and/or code.

`DELETE /<name>`

Delete the given command.

### To Do
- Add progress icon when learning.
- Finish edit capability.
- Gracefully handle errors if RM2 cannot be found.
