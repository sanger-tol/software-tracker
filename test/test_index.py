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

def test_main_page(client):
	result = call(client,'/',{})
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
