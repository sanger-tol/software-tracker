from flask import Flask, jsonify, request, render_template, send_from_directory
import re
import os
import json
import mysql.connector

def load_config_file(filename="config.json"):
    with open(filename, 'r') as myfile:
        data=myfile.read()
    return json.loads(data)

def connect_db(db,schema=''):
    if schema == '':
        schema = str(config[db]['schema'])
    return mysql.connector.connect(
        host=str(config[db]['host']),
        user=str(config[db]['user']),
        database=schema,
        port=str(config[db]['port']),
        passwd=str(config[db]['password'])
    )


app = Flask(__name__)
app.config["DEBUG"] = True

config = load_config_file()

@app.route('/', methods=['GET'])
def home():
    return """
    <h1>Pathogens Software</h1>
    <p>This is an API to manange software installs by Pathogen Informatics.</p>
    Available API functions:
    <ul>
    	<li>
    		<p><b>query</b> [GET]</p>
    		<p>
    			Parameters:
	    		<ul>
	    			<li><tt>user</tt>=username (<i>optional</i>)</li>
	    			<li><tt>before</tt>=timestamp <= VALUE (<i>optional</i>)</li>
	    			<li><tt>after</tt>=timestamp >= VALUE (<i>optional</i>)</li>
	    			<li><tt>image</tt>=image name (<i>optional</i>)</li>
	    			<li><tt>executable</tt>=executable name (<i>optional</i>)</li>
	    			<li><tt>parameters</tt>=parameter string, finds all parameters with that substing (<i>optional</i>)</li>
	    		</ul>
	    	</p>
    	</li>
    </ul>
    """

@app.route('/query', methods=['GET'])
def query():
	ret = { "status":"OK" }
	user = request.args.get('user', default = '', type = str)
	before = request.args.get('before', default = '', type = str)
	after = request.args.get('after', default = '', type = str)
	image = request.args.get('image', default = '', type = str)
	executable = request.args.get('executable', default = '', type = str)
	parameters = request.args.get('parameters', default = '', type = str)
	db = connect_db('pathdb_ro')
	sql = [ '1=1' ]
	values = []
	if user!='':
		sql.append ( 'user=%s' )
		values.append ( user )
	if before!='':
		sql.append ( 'timestamp<=%s' )
		values.append ( before )
	if after!='':
		sql.append ( 'timestamp>=%s' )
		values.append ( after )
	if image!='':
		sql.append ( 'image=%s' )
		values.append ( image )
	if executable!='':
		sql.append ( 'executable=%s' )
		values.append ( executable )
	if parameters!='':
		sql.append ( 'parameters LIKE "%%%s%%"' )
		values.append ( parameters )
	sql = "SELECT * FROM vw_rows WHERE " +' AND '.join ( sql )
	mycursor = db.cursor(buffered=True)
	mycursor.execute(sql,values)
	ret['data'] = []
	for x in mycursor:
		ret['data'].append(x)
	return jsonify(ret)

@app.route('/log', methods=['POST'])
def log():
	ret = { "status":"OK" }
	ret["post"] = request.form['data']
	return jsonify(ret)

if __name__ == "__main__":
	app.run()
