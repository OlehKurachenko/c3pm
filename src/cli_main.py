#!/usr/bin/env python3

#
#   Created by Oleh Kurachenko
#          aka soll_nevermind aka okurache
#   on 2018-03-04T00:37:36Z as a part of cpppm
#
#   ask     oleh.kurachenko@gmail.com , I'm ready to help
#   GitHub  https://github.com/OlehKurachenko
#   rate&CV http://www.linkedin.com/in/oleh-kurachenko-6b025b111
#  

import sys
import cpppmd_json
import os
import subprocess
import shutil

class CLIMain:
    # TODO add comments
    # TODO add man

    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    CYAN = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD = "\033[;1m"
    REVERSE = "\033[;7m"

    CLONEDIR = ".cpppm_clonedir"
    PROJECT_JSON = "cpppm_project.json"

    @staticmethod
    def main():
        if len(sys.argv) < 2:
            pass  # TODO handle no args
        if len(sys.argv) == 2 and sys.argv[1] == "init":
            CLIMain.__init_project()
        if len(sys.argv) == 4 and sys.argv[1] == "add" and sys.argv[2] == "git":
            CLIMain.__add_dependency(sys.argv[2], sys.argv[3])  # TODO handle version
        # TODO hangle list
        # TODO handle tree
        # TODO handle upgrade
        # TODO handle add
        # TODO handle remove

    @staticmethod
    def __init_project():
        if not os.path.isdir("export_src"):
            if os.path.exists("export_src"):
                pass  # TODO handle already existing file export_src instead of directory
            os.mkdir("export_src")
        CLIMain.__message("export_src created", CLIMain.GREEN)
        if not os.path.isdir("import_src"):
            if os.path.exists("import_src"):
                pass  # TODO handle already existing file import_src instead of directory
            os.mkdir("import_src")
        CLIMain.__message("import_src created", CLIMain.GREEN)
        gitignore_content = ""
        if os.path.exists(".gitignore"):
            if os.path.isdir(".gitignore"):
                pass  # TODO handle fucking existence of .gitignore as fucking directory
            gitignore_content = open(".gitignore", "r").read()  # TODO close
        open(".gitignore", "w+").write(gitignore_content + "\n" + "import_src/**" + "\n" +
                                       CLIMain.CLONEDIR + "/**")  # TODO close
        CLIMain.__message(".gitignore written", CLIMain.GREEN)
        project_json = cpppmd_json.CPPPMDJSON()
        open(CLIMain.PROJECT_JSON, 'w+').write(str(project_json)) # TODO close
        CLIMain.__message(CLIMain.PROJECT_JSON + " written", CLIMain.GREEN)
        CLIMain.__message("cpppm project " + project_json.project_name + " successfully initiated",
                          CLIMain.GREEN)

    @staticmethod
    def __add_dependency(dep_type: str, location: str, version: str = ""):
        project_json_file = open(CLIMain.PROJECT_JSON, 'r')
        # TODO handle non-existing cpppm_project.json
        project_json = cpppmd_json.CPPPMDJSON(project_json_file.read())
        project_json_file.close()
        # TODO handle bad json/bad project json
        os.mkdir(CLIMain.CLONEDIR)
        # TODO hangle existance of clonedir
        os.chdir(CLIMain.CLONEDIR)
        CLIMain.__message("cloning " + location + " to " + CLIMain.CLONEDIR + " ...", CLIMain.BLUE)
        os.system("git clone " + location)
        # TODO hangle correctness of git link
        CLIMain.__message("successfully cloned", CLIMain.GREEN)
        dir_list = subprocess.check_output(["ls"]).split()
        if len(dir_list) != 1:
            CLIMain.__message("wrong number of directories in " + CLIMain.CLONEDIR, CLIMain.RED)
            pass  # TODO handle error cloning
        clone_name = dir_list[0].decode("ascii")
        CLIMain.__message("cloned directory name is " + clone_name, CLIMain.BLUE)
        os.chdir(clone_name)
        if not os.path.exists(CLIMain.PROJECT_JSON):
            CLIMain.__message("no " + CLIMain.PROJECT_JSON + "found in repository!", CLIMain.RED)
            pass  # TODO handle not a cpppm project
        with open(CLIMain.PROJECT_JSON, "r") as clone_project_json_file:
            clone_project_json = cpppmd_json.CPPPMDJSON(clone_project_json_file.read())
        dep_name = clone_project_json.project_name
        CLIMain.__message("dependency project name is " + dep_name, CLIMain.GREEN)
        os.chdir("../..")
        shutil.rmtree(CLIMain.CLONEDIR)
        CLIMain.__message(CLIMain.CLONEDIR + " deleted", CLIMain.BLUE)
        if project_json.get_dependency(dep_name):
            CLIMain.__message("dependency " + dep_name + " already exist", CLIMain.RED)
            pass  # TODO handle dependency already exist
        else:
            project_json.add_dependency("git", dep_name, location, "master")
            CLIMain.__message("dependency " + dep_name + " added to project" +
                              project_json.project_name, CLIMain.GREEN)
        with open(CLIMain.PROJECT_JSON, "w+") as project_json_file:
            project_json_file.write(str(project_json))
            CLIMain.__message(CLIMain.PROJECT_JSON + " written", CLIMain.GREEN)
        CLIMain.__message("adding dependency " + dep_name + " to project "
                          + project_json.project_name + " succeeded", CLIMain.GREEN)

    @staticmethod
    def __message(message: str, color: str = ""):
        print(sys.argv[0], end=": ")
        if color:
            sys.stdout.write(color)
        print(message)
        sys.stdout.write(CLIMain.RESET)


if __name__ == "__main__":
    CLIMain.main()
