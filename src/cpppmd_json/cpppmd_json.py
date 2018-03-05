#
#   Created by Oleh Kurachenko
#          aka soll_nevermind aka okurache
#   on 2018-03-04T13:07:02Z as a part of cpppm
#
#   ask     oleh.kurachenko@gmail.com , I'm ready to help
#   GitHub  https://github.com/OlehKurachenko
#   rate&CV http://www.linkedin.com/in/oleh-kurachenko-6b025b111
#  

import json
from collections import OrderedDict


class CPPPMDJSON:
    # TODO write comments

    def __init__(self, json_str: str = ""):
        assert type(json_str) == str, "Illegal type"

        if json_str:
            self.__ordered_dict = json.loads(json_str, object_pairs_hook=OrderedDict)
        else:
            self.__ordered_dict = OrderedDict()
            self.init_new_json()

    def __str__(self):
        return json.dumps(self.__ordered_dict, indent=4)

    @property
    def project_name(self):
        return self.__ordered_dict["name"]

    def get_dependency(self, dep_name: str):
        if dep_name in self.__ordered_dict["dependencies"]:
            return self.__ordered_dict["dependencies"][dep_name]
        else:
            return None

    def add_dependency(self, dep_type: str, dep_name: str, location: str, version: str):
        assert dep_name not in self.__ordered_dict["dependencies"], "Dependency already exist"

        if dep_type == "git":
            self.__ordered_dict["dependencies"][dep_name] = OrderedDict()
            self.__ordered_dict["dependencies"][dep_name]["type"] = "git"
            self.__ordered_dict["dependencies"][dep_name]["url"] = location
            self.__ordered_dict["dependencies"][dep_name]["version"] = version

    def init_new_json(self):
        self.__ordered_dict["name"] = input("Project name>")
        self.__ordered_dict["author"] = input("Author>")
        self.__ordered_dict["version"] = "0.0.1"
        self.__ordered_dict["description"] = "Project dependencies for " + \
                                             self.__ordered_dict["name"]
        self.__ordered_dict["url"] = input("Project URL>")
        self.__ordered_dict["email"] = input("Project e-mail>")
        proj_license = input("License (empty line if not exist)>")
        if proj_license:
            self.__ordered_dict["license"] = proj_license
        self.__ordered_dict["dependencies"] = OrderedDict()
