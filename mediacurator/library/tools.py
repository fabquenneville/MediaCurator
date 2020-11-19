#!/usr/bin/env python3
'''
    These are various tools used by mediacurator
'''

import subprocess
import os
from .bcolors import BColors


def detect_ffmpeg():
    try:
        txt = subprocess.check_output(['ffmpeg', '-version'], stderr=subprocess.STDOUT).decode()
        return txt.partition('\n')[0]
    except:
        return False
    
def user_confirm(question):
    answer = input(question)
    if answer.lower() in ["y","yes"]:
        return True
    elif answer.lower() in ["n","no"]:
        return False
    print("Please answer with yes (Y) or no (N)...")
    return user_confirm(question)

def deletefile(filename):
    try:
        os.remove(filename)
    except OSError:
        print(f"{BColors.FAIL}Error deleting {filename}{BColors.ENDC}")
        return False

    print(f"{BColors.OKGREEN}Successfully deleted {filename}{BColors.ENDC}")
    return True