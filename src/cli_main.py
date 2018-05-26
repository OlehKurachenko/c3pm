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
                if sys.argv[4] == "master" and len(sys.argv) == 5:
                    pass  # TODO call
        if sys.argv[1] == "list" and len(sys.argv) == 2:
            CLIMain.__list_dependencies()
            return
        pass  # TODO add usage message, probably remove "if len(sys.argv) < 2:"

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
