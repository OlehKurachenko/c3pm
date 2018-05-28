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
import shutil
import subprocess
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
    WHAT_IS_C3PM_LINK = "https://github.com/c3pm/c3pm"
    C3PM_JSON_FILENAME = "c3pm.json"
    CLONE_DIR = ".c3pm_clonedir"
    SRC_DIR = "src"
    EXPORT_DIR = "exports"
    IMPORT_DIR = "imports"

    ROOT_NAME_FOR_DEPENDENCIES_LIST = "~root~project~"

    def __init__(self, is_object: bool = False, init_new_project: bool = False):
        """
        If init_new_project is True, directory is checked and if all ok, new c3pm project is
        being initiated by creating new c3pm.json, creating directories "src" and "src/exports" (
        if they do not exist, with file "readme.txt" inside of "src/exports") and making changed
        to ".gitignore" if this file exist.
        If init_new_project is False, project is checked and c3pm.json is being read.
        :param is_object: False by default. If True, checks can c3pm commands be applied
        to this project, otherwise - is project a valid c3pm project to be cloned.
        :param init_new_project: if True, new project is being initialized, otherwise project is
        being loaded

        :raises C3PMProject.BadC3PMProject if project directory check failed
        :raises json.decoder.JSONDecodeError: if json_str is not a valid json
        :raises FileNotFoundError: if self.C3PM_JSON_FILENAME cannot be opened
        :raises AssertionError: if call parameters are forbidden
        TODO rewrite constructor removing exceptions except BadC3PMProject and AssetionError
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
                    CLIMessage.success_message(self.SRC_DIR + " directory created")
            except:
                raise self.BadC3PMProject("unable to create directory " + self.SRC_DIR)
            try:
                if not os.path.isdir(self.SRC_DIR + "/" + self.EXPORT_DIR):
                    os.mkdir(self.SRC_DIR + "/" + self.EXPORT_DIR)
                    CLIMessage.success_message(self.SRC_DIR + "/" + self.EXPORT_DIR
                                               + " directory created")
                    with open(self.SRC_DIR + "/" + self.EXPORT_DIR + "/readme.txt", "w+") as \
                            readme_file:
                        readme_file.write("place your files which have to be taken by a dependent "
                                          "project")
                        CLIMessage.success_message(self.SRC_DIR + "/" + self.EXPORT_DIR +
                                                   "/readme.txt written")
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
            problem_with_project = C3PMProject.ProjectChecker.problem_with_project()
            if problem_with_project:
                raise self.BadC3PMProject(problem_with_project)
            with open(self.C3PM_JSON_FILENAME, "r") as c3pm_json_file:
                self.__c3pm_dict = json.loads(c3pm_json_file.read(), object_pairs_hook=OrderedDict)
                problem_with_c3pm_json = \
                    C3PMProject.C3PMJSONChecker.problem_with_c3pm_json(self.__c3pm_dict)
                if problem_with_c3pm_json:
                    raise self.BadC3PMProject("bad " + self.C3PM_JSON_FILENAME + ": "
                                              + problem_with_c3pm_json)

    @property
    def name(self) -> str:
        return self.__c3pm_dict["name"]

    @name.setter
    def name(self, name: str):
        """
        :param name: new name
        :raises ValueError: if name is not a valid c3pm-project name or already used by one of
        existing dependencies
        TODO rewrite using list
        """
        problem_with_name = C3PMProject.C3PMJSONChecker.problem_with_name(name)
        if problem_with_name:
            raise ValueError(problem_with_name)
        if name in self.list_all_dependencies():
            raise ValueError("name is already used by one of dependencies")
        self.__c3pm_dict["name"] = name

    def add_c3pm_dependency(self, name: str, url: str, version: str = "master"):
        """
        Adds new dependency of type git-c3pm (see docs)
        :param name: name for new dependency (have to be identical with the name of that project)
        :param url: url of .git repository
        :param version: have to be "master" by now
        :raises C3PMProject.BadValue: if any of parameters have incorrect value
        """

        temporary_directory_name = "~tempdir~"

        if version != "master":
            raise C3PMProject.BadValue("version", 'have to be "master"')
        if name in self.list_all_dependencies():
            raise C3PMProject.BadValue("name", "dependency with this name already exist, "
                                               "use list to see")

        try:
            os.mkdir(C3PMProject.CLONE_DIR)
            os.chdir(C3PMProject.CLONE_DIR)
            C3PMProject.clone_git_repository('repository for new dependency "' + name + '"', url,
                                             temporary_directory_name)
        except C3PMProject.BadValue:
            raise
        else:
            try:
                os.chdir(temporary_directory_name)
                c3pm_project = C3PMProject()
            except C3PMProject.BadC3PMProject as err:
                raise C3PMProject.BadValue("url", "in cloned project by this url:" + str(err))
            else:
                if c3pm_project.name != name:
                    raise C3PMProject.BadValue("name", "does not match project name (in " +
                                               C3PMProject.C3PM_JSON_FILENAME + ")")
                self.__c3pm_dict["dependencies"][name] = OrderedDict()
                self.__c3pm_dict["dependencies"][name]["type"] = "git-c3pm"
                self.__c3pm_dict["dependencies"][name]["url"] = url
                self.__c3pm_dict["dependencies"][name]["version"] = "master"
            finally:
                os.chdir("..")
                shutil.rmtree(temporary_directory_name)
        finally:
            os.chdir("..")
            shutil.rmtree(C3PMProject.CLONE_DIR)

    def remove_dependency(self, name: str, version: str = "master"):
        """
        Removes dependency from project.
        :param name: name of dependency to be removed
        :param version: version of dependency to be removed, have to be "master" at this moment
        """
        if version != "master":
            raise self.BadValue("version", 'have to be "master"')
        for dependency_name in self.__c3pm_dict["dependencies"]:
            if dependency_name == name:
                ColorP.print("directory to be removed", line_end=": ", color=ColorP.BOLD_CYAN)
                print(self.dependency_str_representation(dependency_name, colored=True))
                del self.__c3pm_dict["dependencies"][dependency_name]
                return
        raise self.BadValue("name", "no such dependency")

    def dependency_str_representation(self, dependency_name: str, colored: bool = False) -> str:
        """
        Returns str representation of dependency, one line, easy human readable.
        :param dependency_name:
        :param colored: if True, line is colored using color constants from
        colored_print.ColoredPrint
        :return: str representation
        """
        # Color constants
        bold_cyan = ""
        bold_green = ""
        bold_yellow = ""
        reset = ""
        if colored:
            bold_cyan = ColorP.BOLD_CYAN
            bold_green = ColorP.BOLD_GREEN
            bold_yellow = ColorP.BOLD_YELLOW
            reset = ColorP.RESET

        dependency = self.__c3pm_dict["dependencies"][dependency_name]
        result = bold_green + dependency_name + bold_cyan + " -> " + bold_yellow + "type: " + \
            dependency["type"] + bold_cyan
        if dependency["type"] == "git-c3pm":
            result += " , url: " + dependency["url"] + " , version: " + dependency["version"] + \
                      reset
        return result

    def list_all_dependencies(self) -> OrderedDict:
        """
        Loads all project's dependencies recursively to list all their own dependencies. In the
        result, a list of all projects which have to be loaded is listed.
        :raises C3PMProject.BadC3PMProject:
        :return: list of all dependencies
        """

        # TODO clean clone dir

        def full_dependency_branch(dependency_name: str) -> str:
            """
            Returns one of branches to dependency
            :param dependency_name:
            :return: full branch-path to dependency
            """
            result = dependency_name
            next_dependency_name = dependency_name
            while next_dependency_name != C3PMProject.ROOT_NAME_FOR_DEPENDENCIES_LIST:
                next_dependency_name = dependency_parent_list[next_dependency_name]
                result = next_dependency_name + "->" + result
            return result

        CLIMessage.info_message("Listing all dependencies for project " + self.name)
        # OrderedDict of all dependencies, will be returned
        all_dependencies = OrderedDict(self.__c3pm_dict["dependencies"])
        # OrderedDict of dependencies, which are not yet checked
        unchecked_dependencies = OrderedDict(self.__c3pm_dict["dependencies"])
        # dict of dependencies parent name (dependency_name: str -> parent_dependency_name: str)
        dependency_parent_list = dict()

        os.mkdir(C3PMProject.CLONE_DIR)
        os.chdir(C3PMProject.CLONE_DIR)

        for cloned_project_dependency_name in all_dependencies:
            dependency_parent_list[cloned_project_dependency_name] = \
                C3PMProject.ROOT_NAME_FOR_DEPENDENCIES_LIST
        while len(unchecked_dependencies):
            unchecked_dependency = unchecked_dependencies.popitem(last=False)
            unchecked_dependency_name = unchecked_dependency[0]

            try:
                C3PMProject.clone_git_repository(full_dependency_branch(
                    unchecked_dependency_name), unchecked_dependency[1]["url"],
                    unchecked_dependency_name)
            except C3PMProject.BadValue as err:
                raise C3PMProject.BadC3PMProject(str(err))
            else:
                os.chdir(unchecked_dependency_name)
                try:
                    c3pm_cloned_project = C3PMProject()
                    cloned_project_dependencies_dict = \
                        c3pm_cloned_project.__c3pm_dict["dependencies"]
                    for cloned_project_dependency_name in cloned_project_dependencies_dict:
                        if cloned_project_dependency_name in all_dependencies:
                            if cloned_project_dependencies_dict[cloned_project_dependency_name] != \
                                    all_dependencies[cloned_project_dependency_name]:
                                raise C3PMProject.BadC3PMProject(
                                    "duplicated dependencies names:\n"
                                    # dependency 1 name =
                                    + full_dependency_branch(cloned_project_dependency_name) + ":\n"
                                    # dependency 1 info =
                                    + json.dumps(all_dependencies[cloned_project_dependency_name],
                                                 indent=4) + "\n"
                                    # dependency 2 name =
                                    + full_dependency_branch(c3pm_cloned_project.name) + "->"
                                    + cloned_project_dependency_name
                                    # dependency 2 info =
                                    + cloned_project_dependencies_dict[
                                        cloned_project_dependency_name])
                        else:
                            all_dependencies[cloned_project_dependency_name] = OrderedDict(
                                cloned_project_dependencies_dict[cloned_project_dependency_name])
                            unchecked_dependencies[cloned_project_dependency_name] = OrderedDict(
                                cloned_project_dependencies_dict[cloned_project_dependency_name])
                            dependency_parent_list[cloned_project_dependency_name] = \
                                c3pm_cloned_project.name
                except C3PMProject.BadC3PMProject as err:
                    raise C3PMProject.BadC3PMProject("in cloned project " + full_dependency_branch(
                        unchecked_dependency_name) + ":bad project directory: " + err.problem)
                except Exception:
                    raise C3PMProject.BadC3PMProject("in cloned project " + full_dependency_branch(
                        unchecked_dependency_name) + ":unknown error happen, please report that")
                os.chdir("..")
                shutil.rmtree(unchecked_dependency_name)
        os.chdir("..")
        shutil.rmtree(C3PMProject.CLONE_DIR)
        return all_dependencies

    def init_new_json(self):
        """
        Initialize new C3PMJSON with data from user via CLI.
        !!! Do not handle wrong input TODO fix
        """

        # Getting name
        while True:
            name = input("Project name>")
            problem_with_name = C3PMProject.C3PMJSONChecker.problem_with_name(name)
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
        self.__c3pm_dict["whatIsC3pm"] = self.WHAT_IS_C3PM_LINK

    def write(self):
        """
        Writes/re-writes c3mp.json
        """
        with open(C3PMProject.C3PM_JSON_FILENAME, "w+") as c3pm_json_file:
            c3pm_json_file.write(json.dumps(self.__c3pm_dict, indent=4))

    class C3PMJSONChecker:
        """
        Class-envelop for methods, which checks c3pm.json containment
        """

        ALLOWED_SPECIAL_CHARACTERS = "-_"
        ALLOWED_CHARACTERS = "abcdefghijklmnopqrstuvwxyz0123456789"

        @staticmethod
        def problem_with_c3pm_json(json_representation: OrderedDict) -> str:
            """
            Checks is a self.__s3mp_dict which is parsed from c3pm.json is valid
            :return: empty line if all ok, str with problem text otherwise
            """
            # name section
            if "name" not in json_representation:
                return "no name"
            problem_with_name = \
                C3PMProject.C3PMJSONChecker.problem_with_name(json_representation["name"])
            if problem_with_name:
                return "bad name:" + problem_with_name

            # TODO write "dependencies" check

            return ""

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
                if character not in (C3PMProject.C3PMJSONChecker.ALLOWED_CHARACTERS
                                     + C3PMProject.C3PMJSONChecker.ALLOWED_SPECIAL_CHARACTERS):
                    return "name have bad character '" + character + "' (code " \
                           + str(ord(character)) + ") at position " + str(i)
            if name[0] not in C3PMProject.C3PMJSONChecker.ALLOWED_CHARACTERS:
                return "first character is not a latin letter"
            if name[len(name) - 1] not in C3PMProject.C3PMJSONChecker.ALLOWED_CHARACTERS:
                return "last character is not a latin letter"
            return ""

    class ProjectChecker:
        """
        Class-envelope for methods which check is project a valid c3pm-project
        """

        @staticmethod
        def problem_with_project(is_object: bool = False) -> str:
            """
            Checks is project a valid c3pm project according to "docs/c3pm project.md",
            with an exception of c3pm.json - it is being checked while reading it
            It is obvious that this method checks project in the directory where it is called
            :param is_object: False by default. If True, checks can c3pm commands be applied
            to this project, otherwise - is project a valid c3pm project to be cloned.
            :return: empty str if all ok, string with error message otherwise
            """

            if os.path.isfile("src"):
                return '"src" is the file in project directory'
            if os.path.isfile("src/exports"):
                return '"src/exports" is the file in project directory'

            if is_object:
                problem_with_clone_dir = C3PMProject.ProjectChecker.problem_with_clone_dir()
                if problem_with_clone_dir:
                    return problem_with_clone_dir
                if os.path.isfile("imports"):
                    return '"imports" in the file in project directory'

            return ""

        @staticmethod
        def problem_with_clone_dir() -> str:
            """
            Checks does clone dir meets requirements
            ":return: empty str if all ok, string with error message otherwise
            """
            if os.path.isfile(".c3pm_clonedir"):
                return '".c3pm_clonedir" is the file in project directory'
            if os.path.isdir(".c3pm_clonedir"):
                return '".c3pm_clonedir" is the directory in project directory'
            # noinspection PyBroadException
            try:
                os.mkdir(".c3pm_clonedir")
                os.rmdir(".c3pm_clonedir")
            except:
                return '".c3pm_clonedir" cannot be created for undefined reason'

    class BadC3PMProject(Exception):
        """
        Raised when project is not valid c3pm project

        Attributes:
            problem -- a project with project
        """

        def __init__(self, problem: str):
            self.problem = problem

    class BadValue(Exception):
        """
        Raised when value passed to some method of C3PMProject is not correct

        Attributes:
            __problem_object -- meaning or name of parameter to which wrong value was passed
            __problem -- a problem with value
        """

        def __init__(self, problem_object: str, problem: str):
            self.__problem_object = str(problem_object)
            self.__problem = str(problem)

        def __str__(self):
            return "bad value of " + self.__problem_object + ": " + self.__problem

    @staticmethod
    def clone_git_repository(name: str, url: str, target_directory_name: str):
        """
        Clones git repository by url and checks is it cloned correct
        :param name: name of project which will be cloned
        :param url: url of .git repository
        :param target_directory_name: a directory name for cloning
        :raises C3PMProject.BadValue: if cloning failed
        """

        CLIMessage.info_message("cloning " + name + " (" + url + ") to " + target_directory_name)
        os.system("git clone " + url + " " + target_directory_name)
        clone_dir_ls = subprocess.check_output(["ls"]).split()
        if len(clone_dir_ls) == 0:
            raise C3PMProject.BadValue("url", "cloning " + name + " (" + url + ") to " +
                                       target_directory_name + " failed: nothing cloned.")
        if len(clone_dir_ls) != 1:
            raise C3PMProject.BadValue("url", "cloning " + name + " (" + url + ") to " +
                                       target_directory_name + " failed: to many directories in "
                                                               "clone directory.")
        CLIMessage.success_message(name + " cloned")
