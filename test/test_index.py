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

def test_main_page(client):
	result = call(client,'/',{})
	assert('PAthogens SOftware' in str(result))

def test_get_current_timestamp(client):
	assert(len(get_current_timestamp())==19)

'''
def test_send_js(client):
	result = call(client,'/js/jquery.min.js',{})
	assert(str(result).startswith('/*! jQuery v'))

def test_send_css(client):
	result = call(client,'/css/bootstrap.min.css',{})
	assert(str(result).startswith('/*!'))

def test_send_img(client):
	result = call_raw(client,'/img/all_pathogens.jpg',{})
	assert(str(base64.b64encode(result.data)).startswith("""b'/9j/4AAQSkZJR"""))

def test_send_404(client):
	result = call(client,'/img/blah',{})
	assert(str(result).startswith('<!DOCTYPE HTML'))

def test_api_autocomplete_species(client):
	# Can't really test this without DB access, so...
	result = call_json(client,'/api/autocomplete/species/test',{})
	assert(result['more']==0)

def test_api_study(client):
	# Can't really test this without DB access, so...
	result = call_json(client,'/api/study/123',{})
	assert(result['status']=="OK")

def test_api_mlwh_studies(client):
	# Can't really test this without DB access, so...
	result = call_json(client,'/api/mlwh_studies',{})
	assert(str(type(result))=="""<class 'dict'>""")

def test_api_teams(client):
	result = call_json(client,'/api/teams',{})
	assert(result==teams)

def test_api_organism_types(client):
	result = call_json(client,'/api/organism_types',{})
	assert(result==config['organism_types'])

def test_api_mappers(client):
	result = call_json(client,'/api/mappers',{})
	assert(result['smalt']=='smalt')

def test_api_post_mapping_actions(client):
	result = call_json(client,'/api/post_mapping_actions',{})
	assert('snp-calling' in result)

def test_api_references_species(client):
	result = call_json(client,'/api/references/0/Plasmodium chabau',{})
	assert(len(result)==5)

# TODO
# api_references NOT USED
# api_register_study
# api_submit_qc_mapping
'''