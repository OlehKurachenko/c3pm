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

import sys

from c3pm_project import C3PMProject
from cli_message import CLIMessage
from colored_print import ColoredPrint as ColorP


class CLIMain:
    """
    Main class, which encapsulates main functionality

    Properties: ISSUES_LINK -- link to GitHub project issues

    """

    ISSUES_LINK = "https://github.com/OlehKurachenko/c3pm/issues"

    @staticmethod
    def main():
        """
        Main method
        """
        if len(sys.argv) < 2:
            CLIMessage.error_message("At least one CLI argument expected")  # TODO show usage
            sys.exit()
        if sys.argv[1] == "init" and len(sys.argv) == 2:
            CLIMain.__init_project()
            return
        if sys.argv[1] == "add":
            if sys.argv[2] == "git-c3pm":
                if sys.argv[5] == "master" and len(sys.argv) == 6:
                    CLIMain.__add_git_c3pm_dependency(sys.argv[3], sys.argv[4])
                    return
        if sys.argv[1] == "list" and len(sys.argv) == 2:
            CLIMain.__list_dependencies()
            return
        CLIMessage.error_message("bad CLI usage")
        # TODO add usage message, probably remove "if # len(sys.argv) < 2:"

    @staticmethod
    def __init_project():
        """
        Initialize a new c3pm project by creating c3pm.json by users data via CLI,
        (if not exist) "src" and "src/exports". Adds IMPORT_DIR and CLONE_DIR to .gitignore
        """

        try:
            c3pm_project = C3PMProject(is_object=True, init_new_project=True)
            c3pm_project.write()
        except C3PMProject.BadC3PMProject as err:
            CLIMessage.error_message("bad project directory: " + err.problem)
            sys.exit()
        except Exception:
            CLIMessage.error_message("unknown error happen, please, report the following on " +
                                     CLIMain.ISSUES_LINK)
            raise
        CLIMessage.success_message(C3PMProject.C3PM_JSON_FILENAME + " successfully written")

    @staticmethod
    def __add_git_c3pm_dependency(name: str, git_url: str, version: str = "master"):
        """
        Add dependency of type c3pm_dependency
        :param name: name for new dependency
        :param git_url: url of .git repository
        :param version: have to "master" at this moment
        """
        try:
            c3pm_project = C3PMProject(is_object=True)
            c3pm_project.add_c3pm_dependency(name, git_url, version)
            c3pm_project.write()
        except C3PMProject.BadC3PMProject as err:
            CLIMessage.error_message("bad project: " + err.problem)
            sys.exit()
        except C3PMProject.BadValue as err:
            CLIMessage.error_message("bad argument: " + str(err))
            sys.exit()
        except Exception:
            CLIMessage.error_message("unknown error happen, please, report the following on " +
                                     CLIMain.ISSUES_LINK)
            raise

    @staticmethod
    def __list_dependencies():
        try:
            c3pm_project = C3PMProject(is_object=True)
            project_dependencies_dict = c3pm_project.list_all_dependencies()
            ColorP.print("Dependencies for " + c3pm_project.name + ":", ColorP.BOLD_CYAN)
            for dependency_name in project_dependencies_dict:
                if project_dependencies_dict[dependency_name]["type"] == "git-c3pm":
                    ColorP.print("├─── " + dependency_name + "-> ", ColorP.BOLD_CYAN, line_end="")
                    ColorP.print("type: git-c3pm", ColorP.BOLD_GREEN, line_end="")
                    ColorP.print(", url: " + project_dependencies_dict[dependency_name]["url"]
                                 + ", version: " + project_dependencies_dict[dependency_name][
                                     "version"], ColorP.BOLD_CYAN)
        except C3PMProject.BadC3PMProject as err:
            CLIMessage.error_message("bad project: " + err.problem)
            sys.exit()
        except Exception:
            CLIMessage.error_message("unknown error happen, please, report the following on " +
                                     CLIMain.ISSUES_LINK)
            raise


if __name__ == "__main__":
    CLIMain.main()
