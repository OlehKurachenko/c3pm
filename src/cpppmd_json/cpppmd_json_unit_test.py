#
#   Created by Oleh Kurachenko
#          aka soll_nevermind aka okurache
#   on 2018-03-04T22:59:39Z as a part of cpppm
#
#   ask     oleh.kurachenko@gmail.com , I'm ready to help
#   GitHub  https://github.com/OlehKurachenko
#   rate&CV http://www.linkedin.com/in/oleh-kurachenko-6b025b111
#  

import unittest
from cpppmd_json import CPPPMDJSON


class MyTestCase(unittest.TestCase):
    def test_something(self):
        project_json = CPPPMDJSON()
        print(str(project_json))


if __name__ == '__main__':
    unittest.main()
