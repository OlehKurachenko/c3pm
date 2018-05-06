# 
#   Created by Oleh Kurachenko
#          aka okurache
#   on 2018-05-05T15:37:26Z as a part of c3pm
#   
#   ask me      oleh.kurachenko@gmail.com , I'm ready to help
#   GitHub      https://github.com/OlehKurachenko
#   rate & CV   http://www.linkedin.com/in/oleh-kurachenko-6b025b111
#

from collections import OrderedDict
import json


class C3PMJSON:
    """
    Represents a c3pm.json file, which stores data about project and
    it's dependencies. Class is being constructed from stirng representation
    of c3pm.json containment. If no arguments given, a new C3PMJSON is being
    constructed from users data via CLI. Class allows to make changes
    and export new version of this file as string.

    property "version" is a version of c3pm.json standard
    property "whatIsC3pm" is a url to c3pm project, which is added to all c3pm.json
    files
    """

    version = 'v0.2'
    whatIsC3pm = "https://github.com/OlehKurachenko/c3pm"

    def __init__(self, json_str: str = None):
        """
        json_str is being parsed to get it's representation
        :param json_str: str - containment of c3pm.json

        :raises json.decoder.JSONDecodeError: if json_str is not a valid json
        """

        if json_str is not None:
            assert type(json_str) == str, "json_str type must be str"

            self.__c3pm_dict = json.loads(json_str, object_pairs_hook=OrderedDict)
        else:
            self.__c3pm_dict = OrderedDict()
            self.init_new_json()

    def init_new_json(self):
        """
        Initialize new C3PMJSON with data from user via CLI.
        !!! Do not handle wrong input TODO fix
        """
        self.__c3pm_dict["name"] = input("Project name>")
        self.__c3pm_dict["author"] = input("Author>")
        self.__c3pm_dict["version"] = "0.0.1"
        self.__c3pm_dict["description"] = input("Description>")
        self.__c3pm_dict["url"] = input("Project URL>")
        self.__c3pm_dict["email"] = input("Project e-mail>")
        proj_license = input("License (empty line if not exist)>")
        if proj_license:
            self.__c3pm_dict["license"] = proj_license
        self.__c3pm_dict["dependencies"] = []
        self.__c3pm_dict["c3pm_version"] = self.version
        self.__c3pm_dict["whatIsC3pm"] = self.whatIsC3pm

    @property
    def json_str(self) -> str:
        """
        :return: json str representation to be written for c3mp.json file
        """
        return json.dumps(self.__c3pm_dict, indent=4)
