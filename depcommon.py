#!/usr/bin/python
#It will take following parameters:
'''
- Session from ~/auth
- JSON input
- API URL
- Repo Id
'''
import json
import os
import urllib2

def getauthfile():
	return os.path.join(os.environ["HOME"], "auth")

def getauthdata(auth_file):
	with open(auth_file) as authdata:
		data = authdata.read()
	return data

def gpg_keydata(filename):
	with open(filename) as keyfile:
		data = keyfile.read()
	return data

def get_json_data(file_path):
	with open(file_path) as datafile:
		data = json.load(datafile)
	return data

def get_response(url, auth_data):
	req = urllib2.Request(url)
	req.add_header("Authorization", auth_data.rstrip())
	try:
		resp = urllib2.urlopen(req)
		return resp.read()
	except urllib2.HTTPError,error:
		pass

