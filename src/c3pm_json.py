# 
#   Created by Oleh Kurachenko
#          aka okurache
#   on 2018-05-05T15:37:26Z as a part of c3pm
#   
#   ask me      oleh.kurachenko@gmail.com , I'm ready to help
#   GitHub      https://github.com/OlehKurachenko
#   rate & CV   http://www.linkedin.com/in/oleh-kurachenko-6b025b111
#
import os
from collections import OrderedDict
from colored_print import ColoredPrint as ColorP
import json

from cli_message import CLIMessage


class C3PMProject:
    """
    Represents a c3pm project, and mostly, it's c3pm.json file, which stores data about project
    and it's dependencies. Class is being constructed from c3pm.json in directory where it is
    called of from user's data via CLI. Other containment of directory is being checked. Class
    allows to make changes and export new version of c3pm.json file as string or write it
    directly to file.

    property "version" is a version of c3pm.json standard property "whatIsC3pm" is a url to c3pm
    project, which is added to all c3pm.json files

    Properties:
        C3PM_JSON_VERSION -- version of c3pm.json standard
        WHAT_IS_C3PM_LINK -- link for field "whatIsC3pm" in c3pm.json
        CLONE_DIR -- name of temporary directory in which dependency repositories are cloned
        SRC_DIR -- name of directory for sources
        EXPORT_DIR -- name of subdirectory of SRC_DIR, which used for sources which will be exported
        IMPORT_DIR -- name of directory to which imports

    Attributes:
        __c3pm_dict -- an OrderedDict with containment of c3pm.json
    """

    C3PM_JSON_VERSION = "v0.2"
    WHAT_IS_C3PM_LINK = "https://github.com/OlehKurachenko/c3pm"
    C3PM_JSON_FILENAME = "c3pm.json"
    CLONE_DIR = ".c3pm_clonedir"
    SRC_DIR = "src"
    EXPORT_DIR = "exports"
    IMPORT_DIR = "imports"

    def __init__(self, is_object: bool = False, init_new_project: bool = False):
        """
        If init_new_project is True, directory is checked and if all ok, new c3pm project is
        being initiated by creating new c3pm.json, creating directories "src" and "src/exports",
        and making changed to ".gitignore" if this file exist.
        If init_new_project is False, project is checked and c3pm.json is being read.
        :param is_object: False by default. If True, checks can c3pm commands be applied
        to this project, otherwise - is project a valid c3pm project to be cloned.
        :param init_new_project: if True, new project is being initialized, otherwise project is
        being loaded

        :raises C3PMProject.BadC3PMProject if project directory check failed
        :raises json.decoder.JSONDecodeError: if json_str is not a valid json
        :raises FileNotFoundError: if self.C3PM_JSON_FILENAME cannot be opened
        :raises AssertionError: if call parameters are forbidden
        """

        assert type(is_object) == bool, "argument is_object have to bool"
        assert type(init_new_project) == bool, "argument init_new_project have to be bool"

        if init_new_project:

            # Checking project directory before starting dialog with user
            if os.path.isdir(self.C3PM_JSON_FILENAME):
                raise self.BadC3PMProject(self.C3PM_JSON_FILENAME + " is a directory")
            if os.path.isfile(self.C3PM_JSON_FILENAME):
                raise self.BadC3PMProject(self.C3PM_JSON_FILENAME + " already exist")
            if os.path.isfile(self.SRC_DIR):
                raise self.BadC3PMProject(self.SRC_DIR + " is a file")
            if os.path.isfile(self.SRC_DIR + "/" + self.EXPORT_DIR):
                raise self.BadC3PMProject(self.SRC_DIR + "/" + self.EXPORT_DIR + " is a file")

            self.__c3pm_dict = OrderedDict()
            self.init_new_json()

            try:
                if not os.path.isdir(self.SRC_DIR):
                    os.mkdir(self.SRC_DIR)
                    CLIMessage.success_message(self.SRC_DIR + "directory created")
            except:
                raise self.BadC3PMProject("unable to create directory " + self.SRC_DIR)
            try:
                if not os.path.isdir(self.SRC_DIR + "/" + self.EXPORT_DIR):
                    os.mkdir(self.SRC_DIR + "/" + self.EXPORT_DIR)
                    CLIMessage.success_message(self.SRC_DIR + "/" + self.EXPORT_DIR
                                               + " directory created")
            except:
                raise self.BadC3PMProject("unable to create directory " + self.SRC_DIR + "/"
                                          + self.EXPORT_DIR)

            if os.path.isdir(".git"):
                if os.path.isdir(".gitignore"):
                    CLIMessage.error_message(".gitignore is directory!!!")
                else:
                    gitignore_content = ""
                    if os.path.isfile(".gitignore"):
                        with open(".gitignore", "r") as gitignore_file:
                            gitignore_content = gitignore_file.read()
                            if gitignore_content and gitignore_content[len(gitignore_content) -
                                                                       1] != '\n':
                                gitignore_content += "\n"
                            if self.IMPORT_DIR + "/**" not in gitignore_content.split():
                                gitignore_content += self.IMPORT_DIR + "/**" + "\n"
                            if self.CLONE_DIR + "/**" not in gitignore_content.split():
                                gitignore_content += self.CLONE_DIR + "/**" + "\n"
                    with open(".gitignore", "w+") as gitignore_file:
                        gitignore_file.write(gitignore_content)
                    CLIMessage.success_message(".gitinore written")

        else:
            # TODO check project
            with open(self.C3PM_JSON_FILENAME, "r") as c3pm_json_file:
                self.__c3pm_dict = json.loads(c3pm_json_file.read(), object_pairs_hook=OrderedDict)
                self.__check_c3pm_dict()

        # TODO check
        """
        If json_str is not None (default), it is being parsed to get it's representation. In this
        case, load_from_file have to be False (default), otherwise it causes an assertion error.
        If json_str is None and load_from_file if False, it is being constructed with users data
        via CLI.
        If json_str in None and load_from_file if True, containment is being red from file
        self.C3PM_JSON_FILENAME.
        :param json_str: str - containment of c3pm.json
        :param load_from_file: if True, json is being red directly from file

        :raises json.decoder.JSONDecodeError: if json_str is not a valid json
        :raises FileNotFoundError: if self.C3PM_JSON_FILENAME cannot be opened
        :raises C3PMJSON.BadC3PMJSONError: if json is not a valid s3pm project json
        :raises AssertionError: if call parameters are forbidden
        """

        # # todo refactor
        # assert not (json_str and load_from_file), "if json_str is not None (default)," \
        #                                           "load_from_file have to be False (default)"
        #
        #
        #     if load_from_file:
        #         with open(self.C3PM_JSON_FILENAME, "r") as c3pm_json_file:
        #             self.__c3pm_dict = json.loads(c3pm_json_file.read(), object_pairs_hook=OrderedDict)
        #             self.__check_c3pm_dict()
        #     else:
        #         self.__c3pm_dict = OrderedDict()
        #         self.init_new_json()
        # # todo refactor

    def init_new_json(self):
        """
        Initialize new C3PMJSON with data from user via CLI.
        !!! Do not handle wrong input TODO fix
        """

        # TODO check

        # Getting name
        while True:
            name = input("Project name>")
            problem_with_name = C3PMProject.FieldsChecker.problem_with_name(name)
            if problem_with_name:
                ColorP.print("Bad name: " + problem_with_name)
            else:
                self.__c3pm_dict["name"] = name
                break

        self.__c3pm_dict["author"] = input("Author>")
        self.__c3pm_dict["version"] = "0.0.1"
        self.__c3pm_dict["description"] = input("Description>")
        self.__c3pm_dict["url"] = input("Project URL>")
        self.__c3pm_dict["email"] = input("Project e-mail>")
        proj_license = input("License (empty line if not exist)>")
        if proj_license:
            self.__c3pm_dict["license"] = proj_license
        self.__c3pm_dict["dependencies"] = OrderedDict()
        self.__c3pm_dict["c3pm_version"] = self.C3PM_JSON_VERSION
        self.__c3pm_dict["whatIsC3pm"] = self.whatIsC3pm

    # TODO check
    @property
    def name(self) -> str:
        return self.__c3pm_dict["name"]

    # TODO check
    @name.setter
    def name(self, name: str):
        """
        :param name: new name
        :raises ValueError: if name is not a valid c3pm-project name
        """
        problem_with_name = C3PMProject.FieldsChecker.problem_with_name(name)
        if problem_with_name:
            raise ValueError(problem_with_name)
        self.__c3pm_dict["name"] = name

    # TODO check
    @property
    def json_str(self) -> str:
        """
        :return: json str representation to be written for c3mp.json file
        """
        return json.dumps(self.__c3pm_dict, indent=4)

    # TODO check
    def write(self):
        """
        Writes/re-writes c3mp.json
        """
        with open(C3PMProject.C3PM_JSON_FILENAME, "w+") as c3pm_json_file:
            c3pm_json_file.write(self.json_str)

    # TODO check
    def __check_c3pm_dict(self):
        """
        Checks is a self.__s3mp_dict which is parsed from c3pm.json is valid
        :raises C3PMJSON.BadC3PMJSONError: when self.__s3mp_dict is not valid
        """
        # name section
        if "name" not in self.__c3pm_dict:
            raise C3PMProject.BadC3PMJSONError("no name")
        problem_with_name = C3PMProject.FieldsChecker.problem_with_name(self.__c3pm_dict["name"])
        if problem_with_name:
            raise C3PMProject.BadC3PMJSONError(problem_with_name)

    # TODO check
    class FieldsChecker:
        """
        Class-envelop for methods, which check value is a proper value for c3pm.json field
        """

        ALLOWED_SPECIAL_CHARACTERS = "-_"
        ALLOWED_CHARACTERS = "abcdefghijklmnopqrstuvwxyz0123456789"

        @staticmethod
        def problem_with_name(name: str) -> str:
            """
            Checks name value
            :param name: value for name field of c3pm.json
            :return: empty line if all ok, str with problem text otherwise
            """
            if type(name) != str:
                return "name is not a string"
            if name == "":
                return "name is empty string"
            if len(name) > 100:
                return "length of name is greater than 100"
            for i, character in enumerate(name, start=1):
                if character not in (C3PMProject.FieldsChecker.ALLOWED_CHARACTERS
                                     + C3PMProject.FieldsChecker.ALLOWED_SPECIAL_CHARACTERS):
                    return "name have bad character '" + character + "' (code " + str(ord(character)) \
                            + ") at position " + str(i)
            if name[0] not in C3PMProject.FieldsChecker.ALLOWED_CHARACTERS:
                return "first character is not a latin letter"
            if name[len(name) - 1] not in C3PMProject.FieldsChecker.ALLOWED_CHARACTERS:
                return "last character is not a latin letter"
            return ""

    # TODO check
    class BadC3PMJSONError(Exception):
        """
        Raised when c3pm.json containment, on which class is constructed, is a valid json
        but is not a valid c3pm.json because of bad data

        Attributes:
            problem -- a reason why json is not a valid c3mp.json
        """

        def __init__(self, problem: str):
            self.problem = problem

    class BadC3PMProject(Exception):
        """
        Raised when project is not valid c3pm project

        Attributes:
            problem -- a project with project
        """

        def __init__(self, problem: str):
            self.problem = problem
