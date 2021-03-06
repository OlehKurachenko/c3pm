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
    BOLD_YELLOW = "\033[1;33m"

    RESET = "\033[0;0m"

    BOLD = "\033[;1m"

    @staticmethod
    def print(output: str, color: str = "", line_end: str = "\n", ostream = sys.stdout):
        """
        Prints in color to stdout
        :param output: str to be printed in color
        :param color: a property of ColoredPrint, which represents
        :param line_end: str printed in the end of message, not colored
        :param ostream: output stream to which message will be printed
        a color
        """

        if color:
            ostream.write(color)
        ostream.write(output)
        if color:
            ostream.write(ColoredPrint.RESET)
        ostream.write(line_end)
