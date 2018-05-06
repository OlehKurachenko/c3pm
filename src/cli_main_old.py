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

    CLONEDIR = ".cpppm_clonedir"
    EXPORTDIR = "src"
    IMPORTDIR = "imports"
    PROJECT_JSON = "cpppm.json"

    @staticmethod
    def main():
        if len(sys.argv) < 2:
            pass  # TODO handle no args
        if len(sys.argv) == 2 and sys.argv[1] == "init":
            CLIMain.__init_project()
        if len(sys.argv) == 4 and sys.argv[1] == "add" and sys.argv[2] == "git":
            CLIMain.__add_dependency(sys.argv[2], sys.argv[3])  # TODO handle version
        if len(sys.argv) == 4 and sys.argv[1] == "remove" and sys.argv[2] == "git":
            CLIMain.__remove_dependency(sys.argv[3], sys.argv[2])  # TODO handle version
        if len(sys.argv) == 2 and sys.argv[1] == "list":
            CLIMain.__list_dependencies()
        if len(sys.argv) == 2 and sys.argv[1] == "upgrade":
            CLIMain.__upgrade_dependecdies()
        # TODO hangle list
        # TODO handle tree
        # TODO handle upgrade
        # TODO handle remove

    @staticmethod
    def __init_project():
        project_json = cpppmd_json.CPPPMDJSON()
        CLIMain.__write_project_json(project_json)
        CLIMain.__message("cpppm project " + project_json.project_name + " successfully initiated",
                          CLIMain.GREEN)
        if not os.path.isdir(CLIMain.EXPORTDIR):
            if os.path.exists(CLIMain.EXPORTDIR):
                pass  # TODO handle already existing file export_src instead of directory
            os.mkdir(CLIMain.EXPORTDIR)
        CLIMain.__message(CLIMain.EXPORTDIR + " created", CLIMain.GREEN)
        os.chdir(CLIMain.EXPORTDIR)
        os.mkdir(project_json.project_name)
        CLIMain.__message(CLIMain.EXPORTDIR + "/" + project_json.project_name +
                          " created", CLIMain.GREEN)
        os.chdir("..")
        if not os.path.isdir(CLIMain.IMPORTDIR):
            if os.path.exists(CLIMain.IMPORTDIR):
                pass  # TODO handle already existing file import_src instead of directory
            os.mkdir(CLIMain.IMPORTDIR)
        CLIMain.__message(CLIMain.IMPORTDIR + " created", CLIMain.GREEN)
        gitignore_content = ""
        if os.path.exists(".gitignore"):
            if os.path.isdir(".gitignore"):
                pass  # TODO handle fucking existence of .gitignore as fucking directory
            gitignore_content = open(".gitignore", "r").read()  # TODO close
        open(".gitignore", "w+").write(gitignore_content + "\n" + "import_src/**" + "\n" +
                                       CLIMain.CLONEDIR + "/**")  # TODO close
        CLIMain.__message(".gitignore written", CLIMain.GREEN)

    @staticmethod
    def __add_dependency(dep_type: str, location: str, version: str = ""):
        project_json = CLIMain.__load_project_json()
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
        CLIMain.__write_project_json(project_json)
        CLIMain.__message("adding dependency " + dep_name + " to project "
                          + project_json.project_name + " succeeded", CLIMain.GREEN)

    @staticmethod
    def __remove_dependency(dep_name: str, dep_type: str = "name"):
        project_json = CLIMain.__load_project_json()
        project_json.remove_dependency(dep_name, dep_type)
        CLIMain.__write_project_json(project_json)
        CLIMain.__message(dep_name + " removed", CLIMain.GREEN)
        # TODO handle deleting by name

    @staticmethod
    def __list_dependencies():
        project_json = CLIMain.__load_project_json()
        dependencies = project_json.list_all_dependencies()
        while len(dependencies):
            dependency = dependencies.popitem(last=False)
            sys.stdout.write(CLIMain.CYAN)
            print(dependency[0] + ":" + dependency[1]["type"] + "->" + dependency[1]["url"] + "->" +
                  dependency[1]["version"])
            sys.stdout.write(CLIMain.RESET)

    # TODO handle errors
    @staticmethod
    def __upgrade_dependecdies():
        project_json = CLIMain.__load_project_json()
        dependencies = project_json.list_all_dependencies()
        shutil.rmtree(CLIMain.IMPORTDIR)
        os.mkdir(CLIMain.IMPORTDIR)
        os.mkdir(CLIMain.CLONEDIR)
        os.chdir(CLIMain.CLONEDIR)
        while len(dependencies):
            dependency = dependencies.popitem(last=False)
            sys.stdout.write(CLIMain.BLUE)
            print("loading: " + dependency[0] + ":" + dependency[1]["type"] + "->"
                  + dependency[1]["url"] + "->" + dependency[1]["version"])
            sys.stdout.write(CLIMain.RESET)
            CLIMain.__message("cloning " + dependency[1]["url"] + " to " + CLIMain.CLONEDIR + " ...",
                              CLIMain.BLUE)
            os.system("git clone " + dependency[1]["url"] + " " + dependency[0])
            CLIMain.__message("cloned!", CLIMain.BLUE)
            CLIMain.__message("copying " + dependency[0] + "/" + CLIMain.EXPORTDIR + "" + " form "
                              + CLIMain.CLONEDIR + "/" + dependency[0]
                              + " to " + CLIMain.IMPORTDIR + "/" + dependency[0])
            shutil.copytree(dependency[0] + "/" + CLIMain.EXPORTDIR + "/" + dependency[0], "../"
                            + CLIMain.IMPORTDIR + "/" + dependency[0])
            CLIMain.__message("copied!", CLIMain.GREEN)
            shutil.rmtree(dependency[0])
        os.chdir("..")
        shutil.rmtree(CLIMain.CLONEDIR)
        CLIMain.__message("Project upgraded", CLIMain.GREEN)

    @staticmethod
    def __load_project_json() -> cpppmd_json.CPPPMDJSON :
        project_json_file = open(CLIMain.PROJECT_JSON, 'r')
        # TODO handle non-existing cpppm_project.json
        project_json = cpppmd_json.CPPPMDJSON(project_json_file.read())
        # TODO handle bad json/bad project json
        project_json_file.close()
        CLIMain.__message(CLIMain.PROJECT_JSON + " loaded", CLIMain.BLUE)
        return project_json

    @staticmethod
    def __write_project_json(project_json: cpppmd_json.CPPPMDJSON):
        # TODO handle file not opened
        with open(CLIMain.PROJECT_JSON, "w+") as project_json_file:
            project_json_file.write(str(project_json))
            CLIMain.__message(CLIMain.PROJECT_JSON + " written", CLIMain.GREEN)

    @staticmethod
    def __message(message: str, color: str = ""):
        # print(sys.argv[0], end=": ")
        if color:
            sys.stdout.write(color)
        print(message)
        sys.stdout.write(CLIMain.RESET)


if __name__ == "__main__":
    CLIMain.main()
