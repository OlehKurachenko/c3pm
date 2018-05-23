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

from c3pm_json import C3PMProject
from cli_message import CLIMessage


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

        try:
            c3pmjson = C3PMProject(is_object=True, init_new_project=True)
        except C3PMProject.BadC3PMProject as err:
            CLIMessage.error_message("bad project directory: " + err.problem)
            sys.exit()
        except Exception:
            CLIMessage.error_message("unknown error happen, please, report the following on " +
                                     CLIMain.ISSUES_LINK)
            raise

        c3pmjson.write()
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


if __name__ == "__main__":
    CLIMain.main()
