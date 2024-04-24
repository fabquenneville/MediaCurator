#!/usr/bin/env python3
'''
    These are various tools used by mediacurator
'''

import subprocess
import os
import sys

# Import colorama for colored output
import colorama
colorama.init()

# Define color codes for colored output
cgreen = colorama.Fore.GREEN
cyellow = colorama.Fore.YELLOW
cred = colorama.Fore.RED
creset = colorama.Fore.RESET

def load_arguments():
    '''Get/load command parameters

    Returns:
        dict: A dictionary containing lists of options passed by the user
    '''
    arguments = {
        "directories": list(),
        "files": list(),
        "inputs": list(),
        "filters": list(),
        "outputs": list(),
        "printop": list(),
    }

    for arg in sys.argv:
        # Confirm with the user that they selected to delete found files
        if "-del" in arg:
            print(
                f"{cyellow}WARNING: Delete option selected!{creset}")
            if not user_confirm(f"Are you sure you wish to delete all found results after selected operations are successful? [Y/N] ?", color="yellow"):
                print(f"{cgreen}Exiting!{creset}")
                exit()
        elif "-in:" in arg:
            arguments["inputs"] += arg[4:].split(",")
        elif "-filters:" in arg:
            arguments["filters"] += arg[9:].split(",")
        elif "-out:" in arg:
            arguments["outputs"] += arg[5:].split(",")
        elif "-print:" in arg:
            arguments["printop"] += arg[7:].split(",")
        elif "-files:" in arg:
            arguments["files"] += arg[7:].split(",,")
        elif "-dirs:" in arg:
            arguments["directories"] += arg[6:].split(",,")

    return arguments


def detect_ffmpeg():
    '''Returns the version of ffmpeg that is installed or False

    Returns:
        str: The version number of the installed FFMPEG
        False: If version retrieval failed
    '''
    try:
        txt = subprocess.check_output(
            ['ffmpeg', '-version'], stderr=subprocess.STDOUT).decode()
        if "ffmpeg version" in txt:
            # Strip the useless text
            return txt.split(' ')[2]
    except:
        pass
    return False


def user_confirm(question, color=False):
    '''Returns the user's answer to a yes or no question

    Args:
        question (str): The user question
        color (str, optional): The preferred color for a question (red/yellow)
    Returns:
        bool: True for a positive response, False otherwise
    '''
    if color == "yellow":
        print(f"{cyellow}{question} {creset}", end='')
        answer = input()
    elif color == "red":
        print(f"{cred}{question} {creset}", end='')
        answer = input()
    else:
        answer = input(f"{question} ")
    if answer.lower() in ["y", "yes"]:
        return True
    elif answer.lower() in ["n", "no"]:
        return False
    print("Please answer with yes (Y) or no (N)...")
    return user_confirm(question)


def deletefile(filepath):
    '''Delete a file and return a boolean indicating success

    Args:
        filepath (str): The full filepath
    Returns:
        bool: True if successful, False otherwise
    '''
    try:
        os.remove(filepath)
    except OSError:
        print(f"{cred}Error deleting {filepath}{creset}")
        return False

    print(f"{cgreen}Successfully deleted {filepath}{creset}")
    return True


def findfreename(filepath, attempt=0):
    '''Find a free filename by appending [HEVC] or [HEVC](#) to the name if necessary

    Args:
        filepath (str): The full filepath
        attempt (int, optional): The number of attempts made
    Returns:
        str: The first free filepath found
    '''
    attempt += 1
    filename = str(filepath)[:str(filepath).rindex(".")]
    extension = str(filepath)[str(filepath).rindex("."):]
    hevcpath = filename + "[HEVC]" + extension
    copynumpath = filename + f"[HEVC]({attempt})" + extension

    if not os.path.exists(filepath) and attempt <= 2:
        return filepath
    elif not os.path.exists(hevcpath) and attempt <= 2:
        return hevcpath
    elif not os.path.exists(copynumpath):
        return copynumpath
    return findfreename(filepath, attempt)
