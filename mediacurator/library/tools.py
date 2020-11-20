#!/usr/bin/env python3
'''
    These are various tools used by mediacurator
'''

import subprocess
import os
from .bcolors import BColors


def detect_ffmpeg():
    '''Returns the version of ffmpeg that is installed or false'''
    try:
        txt = subprocess.check_output(['ffmpeg', '-version'], stderr=subprocess.STDOUT).decode()
        if "ffmpeg version" in txt:
            # Strip the useless text and 
            return txt.split(' ')[2]
    except:
        pass
    return False
    
def user_confirm(question):
    '''Returns the user answer to a yes or no question'''
    answer = input(question)
    if answer.lower() in ["y","yes"]:
        return True
    elif answer.lower() in ["n","no"]:
        return False
    print("Please answer with yes (Y) or no (N)...")
    return user_confirm(question)

def deletefile(filename):
    '''Delete a file, Returns a boolean'''
    try:
        os.remove(filename)
    except OSError:
        print(f"{BColors.FAIL}Error deleting {filename}{BColors.ENDC}")
        return False

    print(f"{BColors.OKGREEN}Successfully deleted {filename}{BColors.ENDC}")
    return True