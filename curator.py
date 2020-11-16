#!/usr/bin/env python3
'''
    MediaCurator is a Python command line tool to manage a media database.
        * List all the video's and their codecs with or without filters
        * Batch recode videos to more modern codecs (x265 / AV1) based on filters: extentions, codecs ...
    ex:
    ./converter.py list -in:any -filters:old -dir:/mnt/media/ >> ../medlist.txt
    ./converter.py convert -del -in:any -filters:mpeg4 -out:x265,mkv -dir:"/mnt/media/Movies/"
    ./converter.py convert -del -verbose -in:avi,mpg -dir:/mnt/media/
'''

import sys
import os
import subprocess
from getpass import getuser
from pathlib import Path
from pprint import pprint
from hurry.filesize import size

def main():
    ffmpeg_version = detect_ffmpeg()
    if not ffmpeg_version:
        print(f"{bcolors.FAIL}No ffmpeg version detected{bcolors.ENDC}")
        exit()
    print(f"{bcolors.OKBLUE}ffmpeg detected: {ffmpeg_version}{bcolors.ENDC}")
    
    if len(sys.argv) >= 2:
        # Get command parameters
        directories = []
        inputs = []
        filters = []
        outputs = []
        for arg in sys.argv:
            if "-in:" in arg:
                inputs += arg[4:].split(",")
            elif "-filters:" in arg:
                filters += arg[9:].split(",")
            elif "-out:" in arg:
                outputs += arg[5:].split(",")
            elif "-dir:" in arg:
                directories += arg[5:].split(",,")
        

        if sys.argv[1] == "list":
            if any("-file" in argv for argv in sys.argv):
                pass
            elif any("-dir" in argv for argv in sys.argv):
                videolist = []
                #directory = sys.argv[sys.argv.index("-dir") + 1]
                for directory in directories:
                    videolist += get_videolist(directory, inputs, filters)
                videolist.sort()
                for video in videolist:
                    print(f"{get_codec(video)} - {get_resolution(video)[0]}p - {get_size(video)}mb - {video}")
            else:
                print(f"{bcolors.FAIL}Missing directory: {bcolors.ENDC}")
        elif sys.argv[1] == "test":
            if any("-file" in argv for argv in sys.argv):
                pass
            elif any("-dir" in argv for argv in sys.argv):
                print(f"directories = {directories}, inputs = {inputs}, filters = {filters}, outputs = {outputs}")
                exit()
            else:
                print("{bcolors.FAIL}Missing directory: {bcolors.ENDC}")

            
        elif sys.argv[1] == "convert":
            if "av1" in outputs:
                codec = "av1"
            else:
                codec = "x265"
            if any("-file" in argv for argv in sys.argv):
                video = sys.argv[sys.argv.index("-file") + 1]
                folder = str(video)[:str(video).rindex("/") + 1]
                oldfilename = str(video)[str(video).rindex("/") + 1:]

                # Setting new filename
                if "mp4" in outputs:
                    newfilename = oldfilename[:-4] + ".mp4"
                    if oldfilename == newfilename:
                        newfilename = oldfilename[:-4] + "[HEVC]" + ".mp4"
                else:
                    newfilename = oldfilename[:-4] + ".mkv"
                    if oldfilename == newfilename:
                        newfilename = oldfilename[:-4] + "[HEVC]" + ".mkv"
                

                
                print(f"{bcolors.OKCYAN}***********   converting {oldfilename} to {newfilename} ({codec})  ***********{bcolors.ENDC}")
                try:
                    if convert(folder + oldfilename, folder + newfilename, codec):
                        #subprocess.call(['chown', f"{getuser()}:{getuser()}", folder + newfilename])
                        subprocess.call(['chmod', '777', folder + newfilename])
                        if "-del" in sys.argv:
                            delete(folder + oldfilename)
                except:
                    delete(folder + newfilename)
                    return False
            elif any("-dir" in argv for argv in sys.argv):
                videolist = []
                for directory in directories:
                    videolist += get_videolist(directory, inputs, filters)
                videolist.sort()
                counter = 0
                for video in videolist:
                    folder = str(video)[:str(video).rindex("/") + 1]
                    oldfilename = str(video)[str(video).rindex("/") + 1:]

                    if "mp4" in outputs:
                        newfilename = oldfilename[:-4] + ".mp4"
                        if oldfilename == newfilename:
                            newfilename = oldfilename[:-4] + "[HEVC]" + ".mp4"
                    else:
                        newfilename = oldfilename[:-4] + ".mkv"
                        if oldfilename == newfilename:
                            newfilename = oldfilename[:-4] + "[HEVC]" + ".mkv"

                    counter += 1
                    print(f"{bcolors.OKCYAN}***********   convert {counter} of {len(videolist)}   ***********{bcolors.ENDC}")
                    try:
                        if convert(folder + oldfilename, folder + newfilename, codec):
                            #output = (['chown', f"{getuser()}:{getuser()}", folder + newfilename], stderr=subprocess.STDOUT)
                            #output = (['chown', f"{getuser()}:{getuser()}", folder + newfilename], stderr=subprocess.STDOUT)
                            subprocess.call(['chmod', '777', folder + newfilename])
                            if "-del" in sys.argv:
                                delete(folder + oldfilename)
                    except:
                        delete(folder + newfilename)
                        return False

def get_videolist(parentdir, inputs = ["any"], filters = []):
    print(f"{bcolors.OKGREEN}Scanning files in {parentdir} for videos{bcolors.ENDC}")
    videolist = []

    path = Path(parentdir)
    if "wmv" in inputs or "any" in inputs or len(inputs) < 1:
        videolist += list(path.rglob("*.[wW][mM][vV]"))
    if "avi" in inputs or "any" in inputs or len(inputs) < 1:
        videolist += list(path.rglob("*.[aA][vV][iI]"))
    if "mkv" in inputs or "any" in inputs or len(inputs) < 1:
        videolist += list(path.rglob("*.[mM][kK][vV]"))
    if "mp4" in inputs or "any" in inputs or len(inputs) < 1:
        videolist += list(path.rglob("*.[mM][pP]4"))
    if "m4v" in inputs or "any" in inputs or len(inputs) < 1:
        videolist += list(path.rglob("*.[mM]4[vV]"))
    if "flv" in inputs or "any" in inputs or len(inputs) < 1:
        videolist += list(path.rglob("*.[fF][lL][vV]"))
    if "mpg" in inputs or "any" in inputs or len(inputs) < 1:
        videolist += list(path.rglob("*.[mM][pP][gG]"))
    if "vid" in inputs or "any" in inputs or len(inputs) < 1:
        videolist += list(path.rglob("*.[vV][iI][dD]"))
    
    
    # Remove folders
    videolist_tmp = videolist
    videolist = [video for video in videolist_tmp if video.is_file()]
    
    # Filter the list for specific codecs
    videolist_tmp = videolist
    print(f"{bcolors.OKGREEN}Filtering {len(videolist)} videos for the requested parameters{bcolors.ENDC}")
    if len([filt for filt in filters if filt not in ["lowres", "hd"]]) > 0:
        videolist = []

        if "old" in filters:
            videolist += [video for video in videolist_tmp if get_codec(video) not in ["hevc", "av1"]]

        if "mpeg4" in filters or "mpeg" in filters:
            videolist += [video for video in videolist_tmp if get_codec(video) in ["mpeg4", "msmpeg4v3"]]

        if "mpeg" in filters:
            videolist += [video for video in videolist_tmp if get_codec(video) in ["mpeg1video"]]

        if "wmv3" in filters or "wmv" in filters:
            videolist += [video for video in videolist_tmp if get_codec(video) in ["wmv3"]]

        if "x264" in filters:
            videolist += [video for video in videolist_tmp if get_codec(video) in ["x264"]]
        
    if len(filters) > 0 and "lowres" in filters:
        videolist_tmp = videolist
        videolist = [video for video in videolist_tmp if get_resolution(video)[0] < 720]
    elif len(filters) > 0 and "hd" in filters:
        videolist_tmp = videolist
        videolist = [video for video in videolist_tmp if get_resolution(video)[0] >= 720]
    elif len(filters) > 0 and "720" in filters:
        videolist_tmp = videolist
        videolist = [video for video in videolist_tmp if get_resolution(video)[0] == 720]
    elif len(filters) > 0 and "1080" in filters:
        videolist_tmp = videolist
        videolist = [video for video in videolist_tmp if get_resolution(video)[0] == 720]

    print(f"{bcolors.OKGREEN}Found {len(videolist)} videos for the requested parameters{bcolors.ENDC}")
    return videolist


def get_resolution(filename):
    try:
        args = ["ffprobe","-v","error","-select_streams","v:0", "-show_entries","stream=width,height","-of","csv=s=x:p=0",str(filename)]
        output = subprocess.check_output(args, stderr=subprocess.STDOUT)
        output = output.decode().strip()

        # Dealing with malformed video chapters
        if "Referenced QT chapter track not found" in output:
            args = ["ffprobe","-v","error","-select_streams","v:0", "-ignore_chapters", "1", "-show_entries","stream=width,height","-of","csv=s=x:p=0",str(filename)]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            output = output.decode().strip()
    except subprocess.CalledProcessError:
        print(f"{bcolors.FAIL}There seams to be an error with {filename}{bcolors.ENDC}")
        return False
    return [int(output.split("x")[1]), int(output.split("x")[0])]

def get_size(filename):
    try:
        size = int(os.path.getsize(filename) / 1024 / 1024)
    except subprocess.CalledProcessError:
        print(f"{bcolors.FAIL}There seams to be an error with {filename}{bcolors.ENDC}")
        return False
    return size

def get_codec(filename):
    try:
        args = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", str(filename)]
        output = subprocess.check_output(args, stderr=subprocess.STDOUT)
        output = output.decode().strip()

        # Dealing with malformed video chapters
        if "Referenced QT chapter track not found" in output:
            args = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-ignore_chapters", "1", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", str(filename)]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            output = output.decode().strip()
    except subprocess.CalledProcessError:
        print(f"{bcolors.FAIL}There seams to be an error with {filename}{bcolors.ENDC}")
        return False
    return output

def convert(oldfilename, newfilename, codec = "x265"):
    oldsize = get_size(oldfilename)
    resolution = get_resolution(oldfilename)
    
    print(f"{bcolors.OKGREEN}Starting conversion of {oldfilename}{bcolors.OKCYAN}({oldsize}mb)({resolution[0]}p){bcolors.OKGREEN} from {bcolors.OKCYAN}{get_codec(oldfilename)}{bcolors.OKGREEN} to {bcolors.OKCYAN}{codec}{bcolors.OKGREEN}...{bcolors.ENDC}")

    # Preparing ffmpeg command and input file
    args = ['ffmpeg', '-i', oldfilename]

    # conversion options
    if codec == "av1":
        args += ['-c:v', 'libaom-av1', '-strict', 'experimental']
    else:
        args += ['-c:v', 'libx265']
        args += ['-max_muxing_queue_size', '1000']

    # conversion output
    args += [newfilename]

    #args = ['ffmpeg', '-i', oldfilename, newfilename]
    try:
        if "-verbose" in sys.argv:
            subprocess.call(args)
        else:
            txt = subprocess.check_output(args, stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        print(f"{bcolors.FAIL}Conversion failed {e}{bcolors.ENDC}")
        return False
    else:
        newsize = get_size(newfilename)
        oldfilename = str(oldfilename)[str(oldfilename).rindex("/") + 1:]
        newfilename = str(newfilename)[str(newfilename).rindex("/") + 1:]
        print(f"{bcolors.OKGREEN}Converted {oldfilename}{bcolors.OKCYAN}({oldsize}mb){bcolors.OKGREEN} to {newfilename}{bcolors.OKCYAN}({newsize}mb){bcolors.OKGREEN} successfully{bcolors.ENDC}")
        return True

def delete(filename):
    try:
        os.remove(filename)
    except OSError:
        print(f"{bcolors.FAIL}Error deleting {filename}{bcolors.ENDC}")
        return False

    print(f"{bcolors.OKGREEN}Deleted {filename}{bcolors.ENDC}")
    return True

def detect_ffmpeg():
    try:
        txt = subprocess.check_output(['ffmpeg', '-version'], stderr=subprocess.STDOUT).decode()
        return txt.partition('\n')[0]
    except:
        return False

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
if __name__ == '__main__':
    main()
