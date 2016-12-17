# -*- coding: utf-8 -*-
import os
import sqlite3
import time
import json
import broadlink
from flask import Flask, request, Response, render_template, url_for, g



###############################################################################
# Set up app                                                                  #
###############################################################################

app = Flask(__name__)

app.config.from_object(__name__)

if __name__ == '__main__':
    app.run(debug=True)



###############################################################################
# Database setup and RM methods                                               #
###############################################################################

"""
Initializes the database.
"""
def init_db():
    db = get_db()
    with app.open_resource('database/schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()



"""
Creates the database tables.
"""
@app.cli.command('initdb')
def initdb_command():
    init_db()
    print('Initialized the database.')



"""
Connects to the specific database.
"""
def connect_db():
    db = sqlite3.connect(os.path.join(app.root_path, 'database/rmcontrol.db'))
    db.text_factory = str
    db.row_factory = sqlite3.Row
    return db



"""
Opens a new database connection if there is none yet.
"""
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db



"""
Closes the database again at the end of the request.
"""
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()



"""
Get the RM2 device.
"""
def get_device():
    device = broadlink.rm2()
    device.discover()
    device.auth()
    return device



###############################################################################
# Routes                                                                      #
###############################################################################

"""
Show web interface.
"""
@app.route('/')
def index():
    return render_template('index.html')



"""
Get all commands.
"""
@app.route('/commands')
def list():
    if os.stat(os.path.join(app.root_path, 'database/rmcontrol.db')).st_size == 0:
        init_db()

    db = get_db()
    cursor = db.execute('select name from commands order by name asc')

    json_string = json.dumps([dict(command) for command in cursor])
    response = Response(json_string, status = 200, mimetype = 'application/json')
    return response



"""
Create a new command. Takes JSON POST data of "name".
"""
@app.route('/commands', methods = ['POST'])
def create():
    name = request.get_json()['name']

    if not name:
        json_string = json.dumps({'status': 'error', 'message': 'Name field is required.'})
        http_status = 400

    else:
        db = get_db()
        cursor = db.execute('select count(*) from commands where name = ?', [name])
        count = cursor.fetchone()[0]

        if count == 1:
            json_string = json.dumps({'status': 'error', 'message': 'The name \'%s\' is already taken.' % name})
            http_status = 400

        else:
            device = get_device()
            device.enter_learning()

            time.sleep(5) # This gives the user 5 seconds to enter.
            code = device.check_data()

            if not code:
                json_string = json.dumps({'status': 'error', 'message': 'No code received.'})
                http_status = 400

            else:
                db.execute('insert into commands (name, code) values (?, ?)', [name, code])
                db.commit()
                json_string = json.dumps({'status': 'success'})
                http_status = 200

    response = Response(json_string, http_status, mimetype = 'application/json')
    return response



"""
Fire a command. Note: not using GET here as to reserve
that for retrieving a specific record if needed in the future.
"""
@app.route('/commands/<name>', methods = ['POST'])
def fire(name):
    db = get_db()
    cursor = db.execute('select code from commands where name = ?', [name])
    command = cursor.fetchone()
    code = command[0]

    device = get_device()
    device.send_data(code)

    json_string = json.dumps({'status': 'success'})
    response = Response(json_string, status = 200, mimetype = 'application/json')
    return response



"""
Update a command. Takes PATCH data of "name" and/or "code".
"""
@app.route('/commands/<name>', methods = ['PATCH'])
def update(name):
    json_string = json.dumps({'status': 'error', 'message': 'Not yet implemented.'})
    response = Response(json_string, status = 501, mimetype = 'application/json')
    return response



"""
Delete a command.
"""
@app.route('/commands/<name>', methods = ['DELETE'])
def delete(name):
    db = get_db()
    db.execute('delete from commands where name = ?', [name])
    db.commit()

    json_string = json.dumps({'status': 'success'})
    response = Response(json_string, status = 200, mimetype = 'application/json')
    return response
