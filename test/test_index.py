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

def test_main_page(client):
	result = call(client,'/',{})
	assert('PAthogens SOftware' in str(result))

def test_get_current_timestamp(client):
	assert(len(get_current_timestamp())==19)

def test_get_text_id(client):
	db = connect_db('dummy')
	id = get_text_id(db,'foo') # Exists
	assert(id==123)
	id = get_text_id(db,'bar') # New
	assert(id==789)

def test_get_container_id(client):
	db = connect_db('dummy')
	id = get_container_id(db,'foo') # Exists
	assert(id==456)
	id = get_container_id(db,'bar') # New
	assert(id==135)

def test_get_executable_id(client):
	db = connect_db('dummy')
	id = get_executable_id(db,111,'foo') # Exists
	assert(id==112)
	id = get_executable_id(db,111,'bar') # New
	assert(id==113)
	
'''
def call_raw(client, path, params):
    url = path + '?' + urlencode(params)
    response = client.get(url)
    return response

def call(client, path, params):
	return call_raw(client, path, params).data.decode('utf-8')

def call_json(client, path, params):
	return json.loads(call(client, path, params))

def test_send_js(client):
	result = call(client,'/js/jquery.min.js',{})
	assert(str(result).startswith('/*! jQuery v'))

def test_api_study(client):
	# Can't really test this without DB access, so...
	result = call_json(client,'/api/study/123',{})
	assert(result['status']=="OK")
'''