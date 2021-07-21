import webbrowser
import os

def not_a_text():
    
    path = os.getcwd()
    print(path)
    webbrowser.open('file://' + os.path.realpath(filename))
    true: bool = True
    assert true