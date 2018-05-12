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
            CLIMain.__error_message("At least one CLI argument expected")  # TODO show usage
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
            CLIMain.__error_message(C3PMJSON.C3PM_JSON_FILENAME + " is a directory. "
                                    + C3PMJSON.C3PM_JSON_FILENAME + " have to be a file")
            sys.exit()

        if os.path.isfile(C3PMJSON.C3PM_JSON_FILENAME):
            CLIMain.__error_message(C3PMJSON.C3PM_JSON_FILENAME + " already exist. Delete it to re-init"
                                                                  "the project")
            sys.exit()

        if os.path.isfile(CLIMain.SRC_DIR):
            CLIMain.__error_message("File " + CLIMain.SRC_DIR + " already exist in project directory. "
                                    + CLIMain.SRC_DIR + " have to be a directory!")
            sys.exit()

        if os.path.isfile(CLIMain.SRC_DIR + "/" + CLIMain.EXPORT_DIR):
            CLIMain.__error_message("File " + CLIMain.SRC_DIR + "/" + CLIMain.EXPORT_DIR +
                                    " already exist in project directory. " +
                                    CLIMain.SRC_DIR + "/" + CLIMain.EXPORT_DIR + " have to be a directory!")
            sys.exit()

        c3pmjson = C3PMJSON()

        if not os.path.isdir(CLIMain.SRC_DIR):
            os.mkdir(CLIMain.SRC_DIR)
            CLIMain.__success_message(CLIMain.SRC_DIR + "directory created")

        os.chdir(CLIMain.SRC_DIR)

        if not os.path.isdir(CLIMain.EXPORT_DIR):
            os.mkdir(CLIMain.EXPORT_DIR)
            CLIMain.__success_message(CLIMain.SRC_DIR + "/" + CLIMain.EXPORT_DIR + " directory created")

        os.chdir("..")

        if os.path.isdir(".git"):
            gitignore_content = ""
            if os.path.exists(".gitignore"):
                if os.path.isdir(".gitignore"):
                    CLIMain.__error_message(".gitignore is directory!!!")
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
                CLIMain.__success_message(".gitinore written")

        c3pmjson.write()
        CLIMain.__success_message(C3PMJSON.C3PM_JSON_FILENAME + " successfully written")

    # @staticmethod
    # def __add_git_c3pm_dependency(git_url: str, version: str = ""):
    #     """
    #     Adds a new dependency, which is a git repository of c3pm-project to project.
    #     :param git_url: url of git repository
    #     :param version: branch, tag of commit  # TODO handle it (now unused, master if used)
    #     """
    #
    #     # Handling possible errors performing actions
    #     CLIMain.__check_clonedir()
    #
    #     try:
    #         c3pm_json = C3PMJSON(load_from_file=True)
    #     except json.decoder.JSONDecodeError:
    #         CLIMain.__error_message("bad " + C3PMJSON.C3PM_JSON_FILENAME + " file")
    #         sys.exit()
    #     except FileNotFoundError:
    #         CLIMain.__error_message("no " + C3PMJSON.C3PM_JSON_FILENAME + " file in directory")
    #         sys.exit()
    #     except C3PMJSON.BadC3PMJSONError as err:
    #         CLIMain.__error_message("bad " + C3PMJSON.C3PM_JSON_FILENAME + " in actual project:" +
    #                                 err.problem)
    #
    #     os.mkdir(CLIMain.CLONE_DIR)
    #     CLIMain.__success_message(CLIMain.CLONE_DIR + " made")
    #     os.chdir(CLIMain.CLONE_DIR)
    #
    #     CLIMain.__info_message("cloning " + git_url + " to " + CLIMain.CLONE_DIR + " ...")
    #     if subprocess.check_call(["git", "clone", git_url]) != 0:
    #         CLIMain.__error_message("cloning " + git_url + " failed!")
    #         os.chdir("..")
    #         shutil.rmtree(CLIMain.CLONE_DIR)
    #         sys.exit()
    #     CLIMain.__success_message("successfully cloned.")
    #
    #     clone_dir_list = subprocess.check_output(["ls"]).split()
    #
    #     if len(clone_dir_list) != 1:
    #         CLIMain.__error_message("wrong number of directories (" + str(len(clone_dir_list)) + ") in "
    #                                 + CLIMain.CLONE_DIR + " after cloning, 1 expected")
    #         os.chdir("..")
    #         shutil.rmtree(CLIMain.CLONE_DIR)
    #         sys.exit()
    #
    #     cloned_dir_name = clone_dir_list[0].decode("ascii")
    #     os.chdir(cloned_dir_name)
    #
    #     CLIMain.__info_message("checking project...")
    #     try:
    #         dependency_c3pm_json = C3PMJSON(load_from_file=True)
    #     except json.decoder.JSONDecodeError:
    #         CLIMain.__error_message("bad c3pm.json file in cloned project")
    #         os.chdir("../..")
    #         shutil.rmtree(CLIMain.CLONE_DIR)
    #         sys.exit()
    #     except FileNotFoundError:
    #         CLIMain.__error_message("no c3pm.json file in cloned project")
    #         os.chdir("../..")
    #         shutil.rmtree(CLIMain.CLONE_DIR)
    #         sys.exit()
    #     except C3PMJSON.BadC3PMJSONError as err:
    #         CLIMain.__error_message("bad " + C3PMJSON.C3PM_JSON_FILENAME + " in cloned project:" +
    #                                 err.problem)
    #         os.chdir("../..")
    #         shutil.rmtree(CLIMain.CLONE_DIR)
    #         sys.exit()
    #     if not os.path.isdir(CLIMain.SRC_DIR + "/" + CLIMain.EXPORT_DIR):
    #         CLIMain.__error_message("no " + CLIMain.SRC_DIR + "/" + CLIMain.EXPORT_DIR + " in"
    #                                 "cloned directory")
    #         os.chdir("../..")
    #         shutil.rmtree(CLIMain.CLONE_DIR)
    #         sys.exit()
    #
    #     CLIMain.__info_message("dependency project name is " + dependency_c3pm_json.name)
    #
    #     # As now in alpha version, branches and pseudonyms are not handled, simply checks
    #     # is there an identical project
    #
    #     # todo refactor
    #     dep_name = clone_project_json.project_name
    #     CLIMain.__message("dependency project name is " + dep_name, CLIMain.GREEN)
    #     os.chdir("../..")
    #     shutil.rmtree(CLIMain.CLONEDIR)
    #     CLIMain.__message(CLIMain.CLONEDIR + " deleted", CLIMain.BLUE)
    #     if project_json.get_dependency(dep_name):
    #         CLIMain.__message("dependency " + dep_name + " already exist", CLIMain.RED)
    #         pass  # TODO handle dependency already exist
    #     else:
    #         project_json.add_dependency("git", dep_name, location, "master")
    #         CLIMain.__message("dependency " + dep_name + " added to project" +
    #                           project_json.project_name, CLIMain.GREEN)
    #     CLIMain.__write_project_json(project_json)
    #     CLIMain.__message("adding dependency " + dep_name + " to project "
    #                       + project_json.project_name + " succeeded", CLIMain.GREEN)
    #     # todo refactor

    # Errors handling section

    @staticmethod
    def __check_clonedir():
        """
        Checks an ability to make clone_dir, if no, shows error message and terminates
        execution
        """
        if os.path.isfile(CLIMain.CLONE_DIR):
            CLIMain.__error_message(CLIMain.CLONE_DIR + " is a file. Delete or rename it")
            sys.exit()

    # Console message methods section

    @staticmethod
    def __success_message(message: str):
        """
        Writes a success message to stdout (in green)
        :param message: message to be printed
        """
        print(sys.argv[0], end=": ")
        ColorP.print(message, ColorP.BOLD_GREEN)

    @staticmethod
    def __error_message(message: str):
        """
        Writes a success message to stderr (in red)
        :param message: message to be printed
        """
        sys.stderr.write(sys.argv[0] + ": ")
        ColorP.print(output=message, color=ColorP.BOLD_RED, ostream=sys.stderr)

    @staticmethod
    def __info_message(message: str):
        """
        Writes an info message to stdout (in blue)
        :param message: message to be printed
        """
        print(sys.argv[0], end=": ")
        ColorP.print(message, ColorP.BOLD_BLUE)


if __name__ == "__main__":
    CLIMain.main()
