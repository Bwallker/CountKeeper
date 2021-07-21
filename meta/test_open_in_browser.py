import unittest
from logs.log import print
import webbrowser
import os
class OpenInBrowserTest(unittest.TestCase):
    def test_open_report(self):
        
        path = os.getcwd()
        path += "/htmlcov/index.html"
        path = "file://" + path
        webbrowser.open(path, new=2)
    
if __name__ == '__main__':
    unittest.main()