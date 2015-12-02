#!/usr/bin/python
#It will take following parameters:
'''
- Session from ~/auth
- JSON input
- API URL
- Repo Id
'''
import sys
import json
import urllib2
import os

if len(sys.argv) < 4:
	print "Insufficient arguments. Provide URL and JSON file of dependencies"
	print "%s <API URL> <JSON File providing dependency info> <Repo Id>"%(sys.argv[0],)
	sys.exit(1)

auth_file = os.path.join(os.environ["HOME"],"auth")
api_url = sys.argv[1]
file_path = sys.argv[2]
repo_id = sys.argv[3]

def getauthdata():
	with open(auth_file) as authdata:
		data = authdata.read()
	return data

def gpg_keydata(filename):
	with open(filename) as keyfile:
		data = keyfile.read()
	return data

with open(file_path) as datafile:
	data = json.load(datafile)

if not data.has_key("external_dependencies"):
	print "No external dependencies"
	sys.exit(0)

auth_data = getauthdata()

for dependencies in data["external_dependencies"]:
	print "URL: " + dependencies["url"]
	url = dependencies["url"]
	#print "    Series: ",
	for series in dependencies["series"]:
		for components in dependencies["components"]:
			req = urllib2.Request(api_url+"/api/v1/external_dependencies/")
			req.add_header("Authorization",auth_data.rstrip())
			req.add_header("Content-type", "application/json")
			mydatadict = {}
			mydatadict["url"] = url
			mydatadict["series"] = series
			mydatadict["components"] = components
			mydatadict["repository"] = api_url+"/api/v1/repositories/"+repo_id+"/"
			if dependencies.has_key("keys") and dependencies["keys"].has_key(series):
				mydatadict["key"] = gpg_keydata(dependencies["keys"][series])
				#print "Key "+ mydatadict["key"]
			#print "JSON : "+json.dumps(mydatadict)
			req.add_data(json.dumps(mydatadict))
			print "Header " + `req.header_items()`
			print "Data "+req.get_data()
			try:
				resp = urllib2.urlopen(req)
				print "Code : "+ `resp.code`
				print "Message : " + `resp.msg`
			except urllib2.HTTPError, error:
				print "==================Content"
				contents = error.read()
				print contents
				pass
			#else:
			#	print "No error for " + dependencies["url"] + "/"+series+" "+components

