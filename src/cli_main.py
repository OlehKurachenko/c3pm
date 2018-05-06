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
import os

from colored_print import ColoredPrint as ColorP
from c3pm_json import C3PMJSON


class CLIMain:
    """
    Main class, which encapsulates main functionality
    """

    """
    Temporary directory in which dependency repositories are cloned
    """
    CLONE_DIR = ".cpppm_clonedir"

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
        if len(sys.argv) == 2 and sys.argv[1] == "init":
            CLIMain.__init_project()
            return

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
        Writes a success message to stdout (in red)
        :param message: message to be printed
        """

        sys.stderr.write(sys.argv[0] + ": ")
        ColorP.print(output=message, color=ColorP.BOLD_RED, ostream=sys.stderr)


if __name__ == "__main__":
    CLIMain.main()
