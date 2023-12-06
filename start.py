import os
import sys

if os.popen('python3 --version').read() == "Python 3.6.8":
        os.system('export PATH=~/.localpython/bin:$PATH')
if os.popen('python3 --version').read() == "Python 3.11.0":
        os.system('python3 main.py')