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


class CLIMain:

    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    CYAN = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD = "\033[;1m"
    REVERSE = "\033[;7m"

    @staticmethod
    def main():
        if len(sys.argv) < 2:
            pass  # TODO handle no args
        if len(sys.argv) == 2 and sys.argv[1] == "init":
            CLIMain.__init_project()
        # TODO handle init
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
            gitignore_content = open(".gitignore", "r").read()
        open(".gitignore", "w+").write(gitignore_content + "\n" + "import_src/**" + "\n" +
                                       ".cpppm_clonedir/**")
        CLIMain.__message(".gitignore written", CLIMain.GREEN)
        project_json = cpppmd_json.CPPPMDJSON()
        open("cpppm_project.json", 'w+').write(str(project_json))
        CLIMain.__message("cpppm_project.json written", CLIMain.GREEN)
        CLIMain.__message("cpppm project " + project_json.project_name + " successfully initiated",
                          CLIMain.GREEN)

    @staticmethod
    def __message(message: str, color: str = ""):
        print(sys.argv[0], end=": ")
        if color:
            sys.stdout.write(color)
        print(message)
        sys.stdout.write(CLIMain.RESET)


if __name__ == "__main__":
    CLIMain.main()
