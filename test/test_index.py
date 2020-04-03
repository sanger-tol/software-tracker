import pytest
from flask import Flask, jsonify, request, render_template, send_from_directory
from urllib.parse import urlencode
import re
import sys, os
import json
import mysql.connector
import base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../')
from api import *

def call_raw(client, path, params):
    url = path + '?' + urlencode(params)
    response = client.get(url)
    return response

def call(client, path, params):
	return call_raw(client, path, params).data.decode('utf-8')

def call_json(client, path, params):
	return json.loads(call(client, path, params))

#-----

def test_main_page_via_client(client):
	result = call(client,'/',{})
	assert('PAthogens SOftware' in str(result))

def test_main_page_directly(client):
	result = home()
	assert('PAthogens SOftware' in str(result))

def test_get_current_timestamp(client):
	assert(len(get_current_timestamp())==19)

def test_save_to_database(client):
	db = connect_db('dummy')
	json = {
		'user':'xyz9',
		'timestamp':'2020-03-02 11:22:33',
		'image':'the_image.sif',
		'executable':'run_me',
		'path':'/nfs/foo/bar',
		'parameters':"""the_first "the last" 'eternity'"""
	}
	id = save_to_database(json)
	assert(id==12345)

def test_query(client):
	# Fake result
	j = call_json(client,'/query',{'user':'mm6'})
	assert(j=={'data': [{'id': 1}], 'status': 'OK'})

	# No result
	j = call_json(client,'/query',{'user':'no such user'})
	assert(j=={'data': [], 'status': 'OK'})

def test_render_query_html(client):
	assert(render_query_html([])=="""<b>No data</b>""")

	rows = [ {"foo":"bar","baz":1} ]
	html = render_query_html(rows)
	assert("bootstrap" in html)
	assert("""<table class='table'><thead><th>Foo</th><th>Baz</th></thead><tbody><tr><td>bar</td><td>1</td></tr></tbody></table></div>""" in html)

def test_log(client):
	j = client.post('/log',json={}).get_json()
	assert(j=={'status': 'ERROR: Missing JSON keys'})

	params = {
		'executable':'foo',
		'image':'bar',
		'user':'mm6',
		'path':'/baz',
		'timestamp':'2020-04-03 14:45:40' # Passing timestamp to compare result more easily
	}
	j = client.post('/log',json=params).get_json()
	assert(j=={'json': {'executable': 'foo', 'image': 'bar', 'parameters': '', 'path': '/baz', 'timestamp': '2020-04-03 14:45:40', 'user': 'mm6'}, 'status': 'OK'})
