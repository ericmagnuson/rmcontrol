## RM Control
RM Control is an app to control an RM2 by BroadLink.  It allows users to learn IR and RF codes, store them, and fire them.

### Components
1. vue.js front-end
2. python back-end
3. process watcher by supervisord

### Requirements
1. `build-essential`
2. `libavahi-compat-libdnssd-dev`
3. `nodejs v6+`
4. `node-gyp`

### Installation
1. `python setup.py install`
2. `export FLASK_APP=rmcontrol; python -m flask initdb`
3. `python run.py`

RM Control can be interacted with by visiting the included web interface found at http://127.0.0.1:5000 or by talking directly with the API as described farther below.

### VM Initialization (Under construction.)
1. `curl -sL https://deb.nodesource.com/setup_6.x -o nodesource_setup.sh`
2. `sudo bash nodesource_setup.sh`
3. `sudo apt-get update`
4. `sudo apt-get install build-essential git libavahi-compat-libdnssd-dev nodejs node-gyp`
5. `sudo reboot now`
6. `sudo npm install -g --unsafe-perm request homebridge homebridge-httpmulti`

### Supervisor Setup
Coming soon.

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
- Gracefully handle errors if RM2 cannot be found.
