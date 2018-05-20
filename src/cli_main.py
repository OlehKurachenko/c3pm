#!/usr/bin/env python3

#
#   Created by Oleh Kurachenko
#          aka okurache
#   on 2018-05-05T15:30:56Z as a part of c3pm
#   
#   ask me      oleh.kurachenko@gmail.com , I'm ready to help
#   GitHub      https://github.com/OlehKurachenko
#   rate & CV   http://www.linkedin.com/in/oleh-kurachenko-6b025b111
#

import json
import shutil
import sys
import os
import subprocess

from collections import OrderedDict

from colored_print import ColoredPrint as ColorP
from c3pm_json import C3PMJSON


class CLIMain:
    """
    Main class, which encapsulates main functionality
    """

    """
    Temporary directory in which dependency repositories are cloned
    """
    CLONE_DIR = ".c3pm_clonedir"

    SRC_DIR = "src"
    EXPORT_DIR = "exports"

    IMPORT_DIR = "imports"

    @staticmethod
    def main():
        """
        Main method
        """
        if len(sys.argv) < 2:
            CLIMain.Messages.error_message("At least one CLI argument expected")  # TODO show usage
            sys.exit()
        if sys.argv[1] == "init":
            if len(sys.argv) == 2:
                CLIMain.__init_project()
                return
        if sys.argv[1] == "add":
            if sys.argv[2] == "git-c3pm":
                if sys.argv[4] == "master" and len(sys.argv) == 5:
                    pass  # TODO call
        pass  # TODO add usage message, probably remove "if len(sys.argv) < 2:"

    @staticmethod
    def __init_project():
        """
        Initialize a new c3pm project by creating c3pm.json by users data via CLI,
        (if not exist) "src" and "src/exports". Adds IMPORT_DIR and CLONE_DIR to .gitignore
        """

        # Handling possible errors before starting a dialog with user
        if os.path.isdir(C3PMJSON.C3PM_JSON_FILENAME):
            CLIMain.Messages.error_message(C3PMJSON.C3PM_JSON_FILENAME + " is a directory. "
                                           + C3PMJSON.C3PM_JSON_FILENAME + " have to be a file")
            sys.exit()

        if os.path.isfile(C3PMJSON.C3PM_JSON_FILENAME):
            CLIMain.Messages.error_message(C3PMJSON.C3PM_JSON_FILENAME + " already exist. Delete it to re-init"
                                                                         "the project")
            sys.exit()

        if os.path.isfile(CLIMain.SRC_DIR):
            CLIMain.Messages.error_message("File " + CLIMain.SRC_DIR + " already exist in project directory. "
                                           + CLIMain.SRC_DIR + " have to be a directory!")
            sys.exit()

        if os.path.isfile(CLIMain.SRC_DIR + "/" + CLIMain.EXPORT_DIR):
            CLIMain.Messages.error_message("File " + CLIMain.SRC_DIR + "/" + CLIMain.EXPORT_DIR +
                                           " already exist in project directory. " +
                                           CLIMain.SRC_DIR + "/" + CLIMain.EXPORT_DIR + " have to be a directory!")
            sys.exit()

        c3pmjson = C3PMJSON()

        if not os.path.isdir(CLIMain.SRC_DIR):
            os.mkdir(CLIMain.SRC_DIR)
            CLIMain.Messages.success_message(CLIMain.SRC_DIR + "directory created")

        os.chdir(CLIMain.SRC_DIR)

        if not os.path.isdir(CLIMain.EXPORT_DIR):
            os.mkdir(CLIMain.EXPORT_DIR)
            CLIMain.Messages.success_message(CLIMain.SRC_DIR + "/" + CLIMain.EXPORT_DIR + " directory created")

        os.chdir("..")

        if os.path.isdir(".git"):
            gitignore_content = ""
            if os.path.exists(".gitignore"):
                if os.path.isdir(".gitignore"):
                    CLIMain.Messages.error_message(".gitignore is directory!!!")
                else:
                    with open(".gitignore", "r") as gitignore_file:
                        gitignore_content = gitignore_file.read()
            if gitignore_content and gitignore_content[len(gitignore_content) - 1] != '\n':
                gitignore_content += "\n"
            if CLIMain.IMPORT_DIR + "/**" not in gitignore_content.split():
                gitignore_content += CLIMain.IMPORT_DIR + "/**" + "\n"
            if CLIMain.CLONE_DIR + "/**" not in gitignore_content.split():
                gitignore_content += CLIMain.CLONE_DIR + "/**" + "\n"

            if not os.path.isdir(".gitignore"):
                with open(".gitignore", "w+") as gitignore_file:
                    gitignore_file.write(gitignore_content)
                CLIMain.Messages.success_message(".gitinore written")

        c3pmjson.write()
        CLIMain.Messages.success_message(C3PMJSON.C3PM_JSON_FILENAME + " successfully written")

    # @staticmethod
    # def __add_git_c3pm_dependency(git_url: str, version: str = ""):
    #     """
    #     Adds a new dependency, which is a git repository of c3pm-project to project.
    #     :param git_url: url of git repository
    #     :param version: branch, tag of commit  # TODO handle it (now unused, master if used)
    #     """
    #
    #     # Handling possible errors performing actions TODO replace with new method
    #     if not CLIMain.ProjectChecker.clonedir_is_ok():
    #         CLIMain.error_message(CLIMain.ProjectChecker.problem_with_clone_dir())
    #
    #     try:
    #         c3pm_json = C3PMJSON(load_from_file=True)
    #     except json.decoder.JSONDecodeError:
    #         CLIMain.error_message("bad " + C3PMJSON.C3PM_JSON_FILENAME + " file")
    #         sys.exit()
    #     except FileNotFoundError:
    #         CLIMain.error_message("no " + C3PMJSON.C3PM_JSON_FILENAME + " file in directory")
    #         sys.exit()
    #     except C3PMJSON.BadC3PMJSONError as err:
    #         CLIMain.error_message("bad " + C3PMJSON.C3PM_JSON_FILENAME + " in actual project:" +
    #                                 err.problem)
    #
    #     os.mkdir(CLIMain.CLONE_DIR)
    #     CLIMain.success_message(CLIMain.CLONE_DIR + " made")
    #     os.chdir(CLIMain.CLONE_DIR)
    #
    #     CLIMain.info_message("cloning " + git_url + " to " + CLIMain.CLONE_DIR + " ...")
    #     if subprocess.check_call(["git", "clone", git_url]) != 0:
    #         CLIMain.error_message("cloning " + git_url + " failed!")
    #         os.chdir("..")
    #         shutil.rmtree(CLIMain.CLONE_DIR)
    #         sys.exit()
    #     CLIMain.success_message("successfully cloned.")
    #
    #     clone_dir_list = subprocess.check_output(["ls"]).split()
    #
    #     if len(clone_dir_list) != 1:
    #         CLIMain.error_message("wrong number of directories (" + str(len(clone_dir_list)) + ") in "
    #                                 + CLIMain.CLONE_DIR + " after cloning, 1 expected")
    #         os.chdir("..")
    #         shutil.rmtree(CLIMain.CLONE_DIR)
    #         sys.exit()
    #
    #     cloned_dir_name = clone_dir_list[0].decode("ascii")
    #     os.chdir(cloned_dir_name)
    #
    #     CLIMain.info_message("checking project...")
    #     try:
    #         dependency_c3pm_json = C3PMJSON(load_from_file=True)
    #     except json.decoder.JSONDecodeError:
    #         CLIMain.error_message("bad c3pm.json file in cloned project")
    #         os.chdir("../..")
    #         shutil.rmtree(CLIMain.CLONE_DIR)
    #         sys.exit()
    #     except FileNotFoundError:
    #         CLIMain.error_message("no c3pm.json file in cloned project")
    #         os.chdir("../..")
    #         shutil.rmtree(CLIMain.CLONE_DIR)
    #         sys.exit()
    #     except C3PMJSON.BadC3PMJSONError as err:
    #         CLIMain.error_message("bad " + C3PMJSON.C3PM_JSON_FILENAME + " in cloned project:" +
    #                                 err.problem)
    #         os.chdir("../..")
    #         shutil.rmtree(CLIMain.CLONE_DIR)
    #         sys.exit()
    #     if not os.path.isdir(CLIMain.SRC_DIR + "/" + CLIMain.EXPORT_DIR):
    #         CLIMain.error_message("no " + CLIMain.SRC_DIR + "/" + CLIMain.EXPORT_DIR + " in"
    #                                 "cloned directory")
    #         os.chdir("../..")
    #         shutil.rmtree(CLIMain.CLONE_DIR)
    #         sys.exit()
    #
    #     CLIMain.info_message("dependency project name is " + dependency_c3pm_json.name)
    #
    #     # As now in alpha version, branches and pseudonyms are not handled, simply checks
    #     # is there an identical project
    #
    #     # todo refactor
    #     dep_name = clone_project_json.project_name
    #     CLIMain.message("dependency project name is " + dep_name, CLIMain.GREEN)
    #     os.chdir("../..")
    #     shutil.rmtree(CLIMain.CLONEDIR)
    #     CLIMain.message(CLIMain.CLONEDIR + " deleted", CLIMain.BLUE)
    #     if project_json.get_dependency(dep_name):
    #         CLIMain.message("dependency " + dep_name + " already exist", CLIMain.RED)
    #         pass  # TODO handle dependency already exist
    #     else:
    #         project_json.add_dependency("git", dep_name, location, "master")
    #         CLIMain.message("dependency " + dep_name + " added to project" +
    #                           project_json.project_name, CLIMain.GREEN)
    #     CLIMain.write_project_json(project_json)
    #     CLIMain.message("adding dependency " + dep_name + " to project "
    #                       + project_json.project_name + " succeeded", CLIMain.GREEN)
    #     # todo refactor

    # @staticmethod
    # def __list_dependencies() -> OrderedDict:
    #
    #     c3pm_json = CLIMain.__load_c3pm_json_with_project_check(is_object=True)
    #
    #     # todo refactor
    #     dependencies = OrderedDict(self.__ordered_dict["dependencies"])
    #     targets = OrderedDict(self.__ordered_dict["dependencies"])
    #     os.mkdir(CPPPMDJSON.CLONEDIR)  # TODO write
    #     os.chdir(CPPPMDJSON.CLONEDIR)
    #     while len(targets):
    #         dependency = targets.popitem(last=False)
    #         # TODO handle not git only
    #         clone_name = str(random.randint(1000000000000, 9999999999999))
    #         # CPPPMDJSON.__message("DEPENDENCY:" + dependency[0] + " + " + str(dependency[1]), CPPPMDJSON.RED)
    #         CPPPMDJSON.__message("cloning " + dependency[1]["url"] + " to " + clone_name,
    #                              CPPPMDJSON.BLUE)
    #         os.system("git clone " + dependency[1]["url"] + " " + clone_name)
    #         CPPPMDJSON.__message("cloned", CPPPMDJSON.BLUE)
    #         os.chdir(clone_name)
    #         project_json = CPPPMDJSON.__load_project_json()
    #         for sub_dependency in project_json.__ordered_dict["dependencies"]:
    #             if sub_dependency not in dependencies:
    #                 targets[sub_dependency] = \
    #                     OrderedDict(project_json.__ordered_dict["dependencies"][sub_dependency])
    #                 dependencies[sub_dependency] = \
    #                     OrderedDict(project_json.__ordered_dict["dependencies"][sub_dependency])
    #         os.chdir("..")
    #     os.chdir("..")
    #     shutil.rmtree(CPPPMDJSON.CLONEDIR)
    #     # todo refactor
    #     pass  # TODO finish

    @staticmethod
    def __load_c3pm_json_with_project_check(is_object: bool = False) -> C3PMJSON:
        """
        Loads C3PMJSON, checks is project a valid c3pm project.
        If error occures, error message is being printed and programm execution stops
        :param is_object: False by default. If True, checks can c3pm commands be applied
        to this project, otherwise - is project a valid c3pm project to be cloned.
        :return: C3PMJSON loaded from file c3pm.json in directory called
        """
        problem_with_project = CLIMain.ProjectChecker.problem_with_project(is_object)
        if problem_with_project:
            CLIMain.Messages.error_message("Bad project:" + problem_with_project)
            sys.exit()
        try:
            c3pm_json = C3PMJSON(load_from_file=True)
            return c3pm_json
        except json.decoder.JSONDecodeError:
            CLIMain.Messages.error_message("bad " + C3PMJSON.C3PM_JSON_FILENAME + " file")
            sys.exit()
        except FileNotFoundError:
            CLIMain.Messages.error_message("no " + C3PMJSON.C3PM_JSON_FILENAME + " file in directory")
            sys.exit()
        except C3PMJSON.BadC3PMJSONError as err:
            CLIMain.Messages.error_message("bad " + C3PMJSON.C3PM_JSON_FILENAME + " in project:" +
                                    err.problem)
            sys.exit()

    class Messages:
        """
        Class-envelope for CLI messages methods
        """

        @staticmethod
        def success_message(message: str):
            """
            Writes a success message to stdout (in green)
            :param message: message to be printed
            """
            print(sys.argv[0], end=": ")
            ColorP.print(message, ColorP.BOLD_GREEN)

        @staticmethod
        def error_message(message: str):
            """
            Writes a success message to stderr (in red)
            :param message: message to be printed
            """
            sys.stderr.write(sys.argv[0] + ": ")
            ColorP.print(output=message, color=ColorP.BOLD_RED, ostream=sys.stderr)

        @staticmethod
        def info_message(message: str):
            """
            Writes an info message to stdout (in blue)
            :param message: message to be printed
            """
            print(sys.argv[0], end=": ")
            ColorP.print(message, ColorP.BOLD_BLUE)

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
                problem_with_clone_dir = CLIMain.ProjectChecker.problem_with_clone_dir()
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


if __name__ == "__main__":
    CLIMain.main()
