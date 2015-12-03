#How to use

##Important steps

- One time
	- Create Github repositories
	- Login into Aassemble server with github account
	- Copy your auth token from Profile
	- Clone dep-scripts repo to your machine (which has VPN access) and run the following scripts in dep-scripts folder.
	- Call `generate_auth_file.py` with your auth token. It will store your auth token for future use.
	- Call `external.sh` to register external dependencies. These external depedencies are required for kilo build of glance and nova.
	- Add your github repos and branch to Aassmeble. Once, you added github repos, their builds will be generated.
	- Call script `multiple_repos.py` which will create mirror and snapshot. Once you get the snapshot, you can deploy the snapshot URL to install package.

- Every time when a new package is built
	- Call `multiple_repos.py`. It will give you snapshot URL.


