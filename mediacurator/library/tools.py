#!/usr/bin/env python3
'''
    These are various tools used by mediacurator
'''

import subprocess


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