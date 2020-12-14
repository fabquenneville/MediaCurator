#!/usr/bin/env python3
'''
    These are various tools used by mediacurator
'''

import subprocess
import os

import colorama
colorama.init()


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
    
def user_confirm(question, color=False):
    '''Returns the user answer to a yes or no question'''
    if color == "yellow":
        print(colorama.Fore.YELLOW, end = '')
        answer = input(f"{question} ")
        print(colorama.Fore.RESET)
    elif color == "red":
        print(colorama.Fore.RED, end = '')
        answer = input(f"{question} ")
        print(colorama.Fore.RESET)
    else:
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
        print(f"{colorama.Fore.RED}Error deleting {filename}{colorama.Fore.RESET}")
        return False

    print(f"{colorama.Fore.GREEN}Successfully deleted {filename}{colorama.Fore.RESET}")
    return True

def findfreename(filepath, attempt = 0):
    '''Delete a file, Returns a boolean'''
    
    attempt += 1
    
    filename = str(filepath)[:str(filepath).rindex(".")]
    extension = str(filepath)[str(filepath).rindex("."):]
    
    hevcpath = filename + "[HEVC]" + extension
    copynumpath = filename + f"[HEVC]({attempt})" + extension

    if not os.path.exists(filepath):
        return filepath
    elif not os.path.exists(hevcpath):
        return hevcpath
    elif not os.path.exists(copynumpath):
        return copynumpath
    return findfreename(filepath, attempt)