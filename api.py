from flask import Flask, jsonify, request, render_template, send_from_directory
from datetime import datetime
import re
import os
import json
import mysql.connector

def load_config_file(filename="config.json"):
	if app.config['TESTING']:
		return {}
	try:
		with open(filename, 'r') as myfile:
			data=myfile.read()
		return json.loads(data)
	except: # No file
		return {}

def connect_db(db,schema=''):
    if app.config['TESTING']:
    	return app.test_db
    if schema == '':
        schema = str(config['databases'][db]['schema'])
    return mysql.connector.connect(
        host=str(config['databases'][db]['host']),
        user=str(config['databases'][db]['user']),
        database=schema,
        port=str(config['databases'][db]['port']),
        passwd=str(config['databases'][db]['password'])
    )

def get_current_timestamp():
	now = datetime.now()
	return datetime.strftime(now,'%Y-%m-%d %H:%M:%S')

def get_text_id(db,text):
	query = ("SELECT `id` FROM `text` WHERE `text`=%s")
	args = [ text ]
	cursor = db.cursor(buffered=True,dictionary=True)
	cursor.execute(query, args)
	for row in cursor:
		return row['id']

	query = "INSERT IGNORE INTO `text` (`text`) VALUES (%s)"
	cursor = db.cursor(buffered=True,dictionary=True)
	cursor.execute(query, args)
	return cursor.lastrowid

def get_container_id(db,image):
	query = "SELECT `id` FROM `container` WHERE `image`=%s"
	args = [ image ]
	cursor = db.cursor(buffered=True,dictionary=True)
	cursor.execute(query, args)
	for row in cursor:
		return row['id']

	query = "INSERT IGNORE INTO `container` (`image`) VALUES (%s)"
	args = [ image ]
	cursor = db.cursor(buffered=True,dictionary=True)
	cursor.execute(query, args)
	db.commit()
	return cursor.lastrowid

def get_executable_id(db,container_id,executable):
	cursor = db.cursor(buffered=True,dictionary=True)
	args = [ container_id ]
	query = "SELECT `id` FROM `executable` WHERE `container_id`=%s "
	if executable=="":
		query += "AND `name` IS NULL"
	else:
		query += "AND `name`=%s"
		args.append(executable)
	cursor.execute(query, args )
	for row in cursor:
		return row['id']

	cursor = db.cursor(buffered=True,dictionary=True)
	if executable=="":
		query = "INSERT IGNORE INTO `executable` (`container_id`) VALUES (%s)"
	else:
		query = "INSERT IGNORE INTO `executable` (`container_id`,`name`) VALUES (%s,%s)"
	cursor.execute(query, args )
	db.commit()
	return cursor.lastrowid

def save_to_database(json):
	db = connect_db ( 'pathdb_rw' )
	container_id = get_container_id ( db , json["image"] )
	executable_id = get_executable_id ( db , container_id , json["executable"] )
	path_id = get_text_id ( db , json["path"] )
	parameters_id = get_text_id ( db , json["parameters"] )
	query = "INSERT IGNORE INTO `module_usage` (`user`,`timestamp`,`executable_id`,`path`,`parameters`) VALUES (%s,%s,%s,%s,%s)"
	args = (json["user"],json["timestamp"],executable_id,path_id,parameters_id)
	cursor = db.cursor(buffered=True,dictionary=True)
	cursor.execute(query, args)
	db.commit()
	return cursor.lastrowid

def save_to_boring_database(json):
	db = connect_db ( 'pathdb_rw' )
	query = "INSERT IGNORE INTO `logging_event` (`uuid`,`user`,`timestamp`,`image`,`executable`,`path`,`parameters`) VALUES (uuid(),%s,%s,%s,%s,%s,%s)"
	args = (json["user"],json["timestamp"],json["image"],json["executable"],json["path"],json["parameters"])
	cursor = db.cursor(buffered=True)
	cursor.execute(query, args)
	db.commit()
	return cursor.lastrowid

def save_to_logfile(json):
	if not 'logfile' in config:
		return
	output = f'{json["user"]},{json["timestamp"]},{json["image"]},{json["path"]},{json["executable"]},{json["parameters"]}\n'
	with open(config["logfile"], "a") as logfile:
		logfile.write(output)

def render_query_html(rows):
	if len(rows) == 0:
		return "<b>No data</b>"
	html = """
	<link href="https://tools-static.wmflabs.org/cdnjs/ajax/libs/twitter-bootstrap/4.4.0/css/bootstrap.min.css" rel="stylesheet">
	<script src="https://tools-static.wmflabs.org/cdnjs/ajax/libs/twitter-bootstrap/4.4.0/js/bootstrap.min.js"></script>
	<div class="container">
	"""
	html += "<table class='table'><thead>"
	columns = rows[0].keys()
	for col in columns:
		html += "<th>" + col[0].upper() + col[1:] + "</th>"
	html += "</thead><tbody>"
	for row in rows:
		html += "<tr>"
		for col in columns:
			html += "<td>"
			html += str(row[col])
			html += "</td>"
		html += "</tr>"
	html += "</tbody></table></div>"
	return html

app = Flask(__name__)
#app = Flask(__name__, static_url_path='') # If you want to serve static HTML pages
#app.config["CACHE_TYPE"] = "null" # DEACTIVATES CACHE FOR DEVLEOPEMENT; COMMENT OUT FOR PRODUCTION!!!
app.config["DEBUG"] = True
config = load_config_file()

@app.route('/', methods=['GET'])
def home():
	with open('html/index.html', 'r') as file:
		html = file.read()
	return str(html)

@app.route('/query', methods=['GET'])
def query():
	ret = { "status":"OK" }
	user = request.args.get('user', default = '', type = str)
	before = request.args.get('before', default = '', type = str)
	after = request.args.get('after', default = '', type = str)
	image = request.args.get('image', default = '', type = str)
	executable = request.args.get('executable', default = '', type = str)
	parameters = request.args.get('parameters', default = '', type = str)
	output_format = request.args.get('format', default = 'json', type = str)
	aggregate = request.args.get('aggregate', default = '', type = str).split(",")
	limit = request.args.get('limit', default = 500, type = int)

	aggregates = []
	for agg in aggregate:
		if agg in ['user','image','executable','year','month','week']:
			aggregates.append ( agg )

	db = connect_db('pathdb_ro')
	sql = []
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

	if len(aggregates) == 0:
		sql_base = "SELECT * "
	else:
		sql_base = "SELECT "
		for agg in aggregates:
			if agg in ['user','image','executable']:
				sql_base += "`" + agg + "`,"
			elif agg == 'year':
				sql_base += "year(`timestamp`) AS `year`,"
			elif agg == 'month':
				sql_base += "substr(`timestamp`,1,7) as `month`,"
			elif agg == 'week':
				sql_base += "week(`timestamp`) AS `week`,"
		sql_base += "count(*) AS `count` "
	sql_base += " FROM vw_rows" ;
	if len(sql) > 0:
		sql = sql_base + " WHERE " + ' AND '.join ( sql ) ;
	if len(aggregates) == 0:
		sql += " LIMIT " + str(limit)
	else:
		sql += " GROUP BY " + ','.join ( aggregates )
	cursor = db.cursor(buffered=True,dictionary=True)
	cursor.execute(sql,values)
	ret['data'] = []
	#ret['sql'] = sql ;
	for row in cursor:
		if 'timestamp' in row:
			row['timestamp'] = datetime.strftime(row['timestamp'],'%Y-%m-%d %H:%M:%S')
		ret['data'].append(row)

	if output_format == 'json':
		return jsonify(ret)
	else:
		return render_query_html(ret["data"])

@app.route('/log', methods=['GET','POST'])
def log():
	ret = { "status":"OK" }
	json = request.get_json()
	if 'executable' in json and 'image' in json and 'user' in json and 'path' in json:
		if not 'timestamp' in json:
			json["timestamp"] = get_current_timestamp()
		if not 'parameters' in json:
			json["parameters"] = ""
		else:
			json["parameters"] = json["parameters"].strip()
		json["executable"] = json["executable"].strip()
		json["image"] = json["image"].strip()
		json["user"] = json["user"].strip()
		json["path"] = json["path"].strip()
		save_to_boring_database(json)
		save_to_database(json)
		save_to_logfile(json)
		ret["json"] = json
	else:
		ret["status"] = "ERROR: Missing JSON keys"

	return jsonify(ret)

if __name__ == "__main__":
	app.run()
