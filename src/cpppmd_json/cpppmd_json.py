#
#   Created by Oleh Kurachenko
#          aka soll_nevermind aka okurache
#   on 2018-03-04T13:07:02Z as a part of cpppm
#
#   ask     oleh.kurachenko@gmail.com , I'm ready to help
#   GitHub  https://github.com/OlehKurachenko
#   rate&CV http://www.linkedin.com/in/oleh-kurachenko-6b025b111
#  

# TODO check & fix unnecessare imports

import json
import os
from collections import OrderedDict
import random
import shutil
import sys

class CPPPMDJSON:
    # TODO write comments

    # TODO fix weak incapsultaion here and in cppmd_json
    CLONEDIR = ".cpppm_clonedir"
    PROJECT_JSON = "cpppm_project.json"

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

    def remove_dependency(self, dep_data: str, dep_data_type: str):
        if dep_data_type == "git":
            for key in self.__ordered_dict["dependencies"].keys():
                if self.__ordered_dict["dependencies"][key]["type"] == "git" \
                        and self.__ordered_dict["dependencies"][key]["url"] == dep_data:
                    del self.__ordered_dict["dependencies"][key]

    def list_all_dependencies(self) -> OrderedDict:
        dependencies = OrderedDict(self.__ordered_dict["dependencies"])
        targets = OrderedDict(self.__ordered_dict["dependencies"])
        os.mkdir(CPPPMDJSON.CLONEDIR)  # TODO write
        os.chdir(CPPPMDJSON.CLONEDIR)
        while len(targets):
            dependency = targets.popitem(last=False)
            # TODO handle not git only
            clone_name = str(random.randint(1000000000000, 9999999999999))
            # CPPPMDJSON.__message("DEPENDENCY:" + dependency[0] + " + " + str(dependency[1]), CPPPMDJSON.RED)
            CPPPMDJSON.__message("cloning " + dependency[1]["url"] + " to " + clone_name,
                                 CPPPMDJSON.BLUE)
            os.system("git clone " + dependency[1]["url"] + " " + clone_name)
            CPPPMDJSON.__message("cloned", CPPPMDJSON.BLUE)
            os.chdir(clone_name)
            project_json = CPPPMDJSON.__load_project_json()
            for sub_dependency in project_json.__ordered_dict["dependencies"]:
                if sub_dependency not in dependencies:
                    targets[sub_dependency] = \
                        OrderedDict(project_json.__ordered_dict["dependencies"][sub_dependency])
                    dependencies[sub_dependency] = \
                        OrderedDict(project_json.__ordered_dict["dependencies"][sub_dependency])
            os.chdir("..")
        os.chdir("..")
        shutil.rmtree(CPPPMDJSON.CLONEDIR)
        return dependencies

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

    # TODO remove code duplication with cli_main
    @staticmethod
    def __load_project_json():
        project_json_file = open(CPPPMDJSON.PROJECT_JSON, 'r')
        # TODO handle non-existing cpppm_project.json
        project_json = CPPPMDJSON(project_json_file.read())
        # TODO handle bad json/bad project json
        project_json_file.close()
        CPPPMDJSON.__message(CPPPMDJSON.PROJECT_JSON + " loaded", CPPPMDJSON.BLUE)
        return project_json

    # TODO remove code duplication with cli_main
    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    CYAN = "\033[1;36m"
    GREEN = "\033[1;32m"
    RESET = "\033[0;0m"
    BOLD = "\033[;1m"
    REVERSE = "\033[;7m"

    # TODO remove code duplication with cli_main
    @staticmethod
    def __message(message: str, color: str = ""):
        # print(sys.argv[0], end=": ")
        if color:
            sys.stdout.write(color)
        print(message)
        sys.stdout.write(CPPPMDJSON.RESET)