# dep-scripts
Scripts related to packaging and deployment and dependency management.

## dependency.py
This script is to add external dependencies to a given repo. Its usage is shown below:

    python depedency.py http://10.140.221.229:9000 test.json 4
    #where http://10.140.221.229:9000 is API URL
    #     test.json is json file describing external dependencies
    #     4 is repository id
    #
    # It is using v1 API.
  
A sample JSON is shown below:

    {"external_dependencies":
      [
        {
          "url":"http://archive.ubuntu.com/ubuntu",
          "series":["trusty-updates"],
          "components":["main","universe"],
          "keys":{
                  "trusty-updates":"../gpg.key"
                }
        }
      ]
    }

JSON file should contains:

1. `external_dependencies`: This array contains external dependencies.
2. Each dependency is described as shown below:
    a. `url`: dependent repo URL
    b. `series`: This array describes the series to be picked for the URL
    c. `components`: This array describes the components to be picked up for each series
    d. `keys`: This dictionary specifies key for each series as file.
