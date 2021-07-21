"""
import unittest
from logs.log import print
import webbrowser
import os
class Brave(webbrowser.BaseBrowser):
    pass

class OpenInBrowserTest(unittest.TestCase):
    def test_open_report(self):
        path = os.getcwd()
        path += "/htmlcov/index.html"
        path = "file://" + path
        webbrowser.open(path, new=2, autoraise=True)
        self.assertTrue(True)
    
if __name__ == '__main__':
    unittest.main()
"""