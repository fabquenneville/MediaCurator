#!/usr/bin/env python3
'''
    These are various tools used by mediacurator
'''

import subprocess
import os
import sys

import colorama
colorama.init()


def load_arguments():
    '''Get/load command parameters 

    Args:

    Returns:
        arguments: A dictionary of lists of the options passed by the user
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
        # Confirm with the user that he selected to delete found files
        if "-del" in arg:
            print(
                f"{colorama.Fore.YELLOW}WARNING: Delete option selected!{colorama.Fore.RESET}")
            if not user_confirm(f"Are you sure you wish to delete all found results after selected operations are succesfull ? [Y/N] ?", color="yellow"):
                print(f"{colorama.Fore.GREEN}Exiting!{colorama.Fore.RESET}")
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
    '''Returns the version of ffmpeg that is installed or false

    Args:

    Returns:
        String  :   The version number of the installed FFMPEG
        False   :   The failure of retreiving the version number
    '''
    try:
        txt = subprocess.check_output(
            ['ffmpeg', '-version'], stderr=subprocess.STDOUT).decode()
        if "ffmpeg version" in txt:
            # Strip the useless text and
            return txt.split(' ')[2]
    except:
        pass
    return False


def user_confirm(question, color=False):
    '''Returns the user answer to a yes or no question

    Args:
        question    :   A String containing the user question
        color       :   A String containing the prefered color for a question (reg/yellow)
    Returns:
        Bool        :   Positive or negative return to the user question
    '''
    if color == "yellow":
        print(f"{colorama.Fore.YELLOW}{question} {colorama.Fore.RESET}", end='')
        answer = input()
    elif color == "red":
        print(f"{colorama.Fore.RED}{question} {colorama.Fore.RESET}", end='')
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
    '''Delete a file, Returns a boolean

    Args:
        filepath    :   A string containing the full filepath
    Returns:
        Bool        :   The success of the operation
    '''
    try:
        os.remove(filepath)
    except OSError:
        print(f"{colorama.Fore.RED}Error deleting {filepath}{colorama.Fore.RESET}")
        return False

    print(f"{colorama.Fore.GREEN}Successfully deleted {filepath}{colorama.Fore.RESET}")
    return True


def findfreename(filepath, attempt=0):
    ''' Given a filepath it will try to find a free filename by appending to the name.
    First trying as passed in argument, then adding [HEVC] to the end and if all fail [HEVC](#).

    Args:
        filepath    :   A string containing the full filepath
        attempt     :   The number of times we have already tryed
    Returns:
        filepath    :   The first free filepath we found
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
