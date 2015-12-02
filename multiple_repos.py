import json
import sys
import httplib
import requests
import yaml
import time
import depcommon

base_api_url = "http://10.140.221.229"
api_url = base_api_url+":9000"

def get_repo_list(authtoken):
	Headers2 = {'Authorization':authtoken}
	r = requests.get(api_url+"/api/v1/repositories/", headers=Headers2)
	values = json.loads(r.content)
	repolists = []
	for result in values["results"]:
		repourl = result["binary_source_list"].split()
		repo = {"location":repourl[1], "release":repourl[2], "repos":repourl[3]}
		repolists.append(repo)
	return repolists

def read_from_yaml(authtoken,filename):
    with open(filename, 'r') as f:
        doc = yaml.load(f)
        count=len(doc['repositories'])
        mirrors=[]
        for x in doc['repositories']:
            mirror=check_for_mirror( authtoken,x["location"],x["release"],x["repos"])
            mirrors.append(mirror)
    return mirrors

def for_each_repo(authtoken):
	repo_lists = get_repo_list(authtoken)
	mirrors = []
	for repo in repo_lists:
		mirror = check_for_mirror(authtoken, repo["location"], repo["release"], repo["repos"])
		mirrors.append(mirror)
	return mirrors

def create_mirror(authtoken,mirrorurl,mirrorseries,mirrorcomponent):
    Headers2 = {'Authorization':authtoken}
    body = {}
    body['url']=mirrorurl
    series=[]
    series.append(mirrorseries)
    components=[]
    components.append(mirrorcomponent)
    body['series']=series
    body['components']=components
    body['public']=True
    r = requests.post(api_url+"/api/v1/mirrors/", data=body, headers=Headers2)
    values = json.loads(r.content)
    return values["self"]


def check_for_mirror(authtoken,mirrorurl,mirrorseries,mirrorcomponent):
    Headers2 = {'Authorization':authtoken}
    r = requests.get(api_url+"/api/v1/mirrors/", headers=Headers2)
    seriesbool=False
    componentsbool=False
    result=False
    values = json.loads(r.content)
    mirrors = []
    for count in range(0,values["count"]):
        mirrors = values["results"][count]
        series = set(mirrors["series"])
        components = set (mirrors["components"])
        if ((mirrorseries in series) and (mirrorcomponent in components) and (mirrorurl == mirrors['url'])):
            result=True
            break

    if result:
        trigger_mirror_update(authtoken,mirrors["self"])
        return mirrors["self"]

    else:
        return create_mirror(authtoken,mirrorurl,mirrorseries,mirrorcomponent)

def trigger_mirror_update(authtoken,mirrorurl):
    Headers2 = {'Authorization':authtoken}
    url = mirrorurl+"refresh/"
    body={}
    r = requests.post(url, headers=Headers2)
    refresh_happened=False
    while(not refresh_happened):
        time.sleep(2)
        r = requests.get(mirrorurl, data=body, headers=Headers2)
        values=json.loads(r.content)
        refresh_happenning=values["refresh_in_progress"]
        refresh_happened= not refresh_happenning
        time.sleep(5)

def create_mirror_set(authtoken,mirrorselfurl):
    Headers2 = {'Authorization':authtoken}
    body = {}
    body['mirrors']=mirrorselfurl
    r = requests.post(api_url+"/api/v1/mirror_sets/", data=body, headers=Headers2)
    values = json.loads(r.content)
    return values["self"]


def check_for_mirror_set(authtoken,mirrorselfurl):
    Headers2 = {'Authorization':authtoken}
    r = requests.get(api_url+"/api/v1/mirror_sets/", headers=Headers2)
    seriesbool=False
    componentsbool=False
    result=False
    values = json.loads(r.content)
    mirrorselfurl1 = set(mirrorselfurl)
    mirrorsets = []
    for count in range(0,values["count"]):
        mirrorsets = values["results"][count]
        mirrorset = set(mirrorsets["mirrors"])
        if ((mirrorselfurl1 == mirrorset)):
            result=True
            break

    if result:
        return mirrorsets["self"]

    else:
        return create_mirror_set(authtoken,mirrorselfurl)


def create_snapshot(authtoken,mirrorsetselfurl):
    Headers2 = {'Authorization':authtoken}
    body = {}
    mirrorset=[]
    mirrorset.append(mirrorsetselfurl)
    body['mirrorset']=mirrorset
    r = requests.post(api_url+"/api/v1/snapshots/", data=body, headers=Headers2)
    values = json.loads(r.content)
    return base_api_url+"/snapshots/"+filter(lambda x: x!='', values["self"].split("/"))[-1]+"/"

def main():
    authtoken = depcommon.getauthdata(depcommon.getauthfile())
    #mirrorselfurl=read_from_yaml(authtoken,filename)
    mirrorselfurl = for_each_repo (authtoken)
    mirrorsetselfurl=check_for_mirror_set(authtoken,mirrorselfurl)
    snapshot=create_snapshot(authtoken,mirrorsetselfurl)
    return snapshot


if __name__ == "__main__":
     #sys.exit(main(filename))
     sys.exit(main())
