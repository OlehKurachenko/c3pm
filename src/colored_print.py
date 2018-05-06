# 
#   Created by Oleh Kurachenko
#          aka okurache
#   on 2018-05-06T13:09:39Z as a part of c3pm
#   
#   ask me      oleh.kurachenko@gmail.com , I'm ready to help
#   GitHub      https://github.com/OlehKurachenko
#   rate & CV   http://www.linkedin.com/in/oleh-kurachenko-6b025b111
#

import sys


class ColoredPrint:
    """
    Color constants and static methods to print in color via CLI
    """

    BOLD_RED = "\033[1;31m"
    BOLD_BLUE = "\033[1;34m"
    BOLD_CYAN = "\033[1;36m"
    BOLD_GREEN = "\033[1;32m"

    __RESET = "\033[0;0m"

    BOLD = "\033[;1m"

    @staticmethod
    def print(output: str, color: str = ""):
        """
        Prints in color to stdout
        :param output: str to be printed in color
        :param color: a property of ColoredPrint, which represents
        a color
        """

        if color:
            sys.stdout.write(color)
        sys.stdout.write(output)
        if color:
            sys.stdout.write(ColoredPrint.__RESET)
