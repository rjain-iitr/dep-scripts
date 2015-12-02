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
import depcommon

if len(sys.argv) < 2:
	print "Insufficient arguments. Provide URL and JSON file of dependencies"
	print "%s <API URL> <JSON File providing dependency info>"%(sys.argv[0],)
	sys.exit(1)

auth_file = depcommon.getauthfile()
api_url = sys.argv[1]
file_path = sys.argv[2]

data = depcommon.get_json_data(file_path)

if not data.has_key("external_dependencies"):
	print "No external dependencies"
	sys.exit(0)

auth_data = depcommon.getauthdata(auth_file)

def get_repo_lists(auth_data):
	repolist = depcommon.get_response(api_url+"/api/v1/repositories/", auth_data)
	dictobj = json.loads(repolist)
	results = dictobj["results"]
	return map(lambda x: x["self"], results)

def get_external_dependency_list(auth_data):
	deplist = depcommon.get_response(api_url+"/api/v1/external_dependencies/", auth_data)
	dictobj = json.loads(deplist)
	return dictobj["results"]

current_external_dependencies = get_external_dependency_list(auth_data)
repo_lists = get_repo_lists(auth_data)
#print "Repo lists : "+`repo_lists`

def find_dependency(ced, url, series, components, repository):
	return len(filter(lambda x: x["url"]==url and x["series"]==series and x["components"]==components and x["repository"]==repository, ced)) > 0

for dependencies in data["external_dependencies"]:
	#print "URL: " + dependencies["url"]
	url = dependencies["url"]
	#print "    Series: ",
	for series in dependencies["series"]:
		for components in dependencies["components"]:
			for repo_url in repo_lists:
				if find_dependency(current_external_dependencies, url, series, components, repo_url):
					print "Already Added: " + url + " "+series+" "+components+" "+repo_url
					continue
				req = urllib2.Request(api_url+"/api/v1/external_dependencies/")
				req.add_header("Authorization",auth_data.rstrip())
				req.add_header("Content-type", "application/json")
				mydatadict = {}
				mydatadict["url"] = url
				mydatadict["series"] = series
				mydatadict["components"] = components
				mydatadict["repository"] = repo_url
				if dependencies.has_key("keys") and dependencies["keys"].has_key(series):
					mydatadict["key"] = depcommon.gpg_keydata(dependencies["keys"][series])
					#print "Key "+ mydatadict["key"]
				#print "JSON : "+json.dumps(mydatadict)
				req.add_data(json.dumps(mydatadict))
				#print "Header " + `req.header_items()`
				#print "Data "+req.get_data()
				try:
					resp = urllib2.urlopen(req)
					print "Code : "+ `resp.code`
					print "Message : " + `resp.msg`
				except urllib2.HTTPError, error:
					print "==================ERROR Content"
					contents = error.read()
					print contents
					pass
				#else:
			#	print "No error for " + dependencies["url"] + "/"+series+" "+components

