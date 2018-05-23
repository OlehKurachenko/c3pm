# 
#   Created by Oleh Kurachenko
#          aka okurache
#   on 2018-05-20T23:05:25Z as a part of c3pm
#   
#   ask me      oleh.kurachenko@gmail.com , I'm ready to help
#   GitHub      https://github.com/OlehKurachenko
#   rate & CV   http://www.linkedin.com/in/oleh-kurachenko-6b025b111
# 

import sys
from colored_print import ColoredPrint as ColorP


class CLIMessage:
    """
    Class-envelope for CLI messages methods
    """

    @staticmethod
    def success_message(message: str):
        """
        Writes a success message to stdout (in green)
        :param message: message to be printed
        """
        print(sys.argv[0], end=": ")
        ColorP.print(message, ColorP.BOLD_GREEN)

    @staticmethod
    def error_message(message: str):
        """
        Writes a success message to stderr (in red)
        :param message: message to be printed
        """
        sys.stderr.write(sys.argv[0] + ": ")
        ColorP.print(output=message, color=ColorP.BOLD_RED, ostream=sys.stderr)

    @staticmethod
    def info_message(message: str):
        """
        Writes an info message to stdout (in blue)
        :param message: message to be printed
        """
        print(sys.argv[0], end=": ")
        ColorP.print(message, ColorP.BOLD_BLUE)

