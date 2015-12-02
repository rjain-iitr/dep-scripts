#!/usr/bin/python
import depcommon
import sys

if len(sys.argv) < 2:
	print "No token is provided"
	sys.exit(1)

token = sys.argv[1]
authfile = depcommon.getauthfile()
f = open(authfile,"w")
f.write("Token "+token)
f.close()

