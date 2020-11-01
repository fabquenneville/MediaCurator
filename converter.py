#!/usr/bin/env python3
'''Its a script!
    ./converter.py list -dir "/"
    ./converter.py convert -del -dir "/mnt/media/"

'''

import sys
import os
from pathlib import Path
from pprint import pprint
from hurry.filesize import size

from subprocess import check_output, STDOUT, CalledProcessError



def main():
    if len(sys.argv) >= 2:
        if sys.argv[1] == "list":
            if "-file" in sys.argv:
                pass
            elif "-dir" in sys.argv:
                directory = sys.argv[sys.argv.index("-dir") + 1]
                videolist = get_videolist(directory)
                for video in videolist:
                    print(f"{get_codec(video)} - {video}")
            else:
                print("Missing directory: ")
        elif sys.argv[1] == "test":
            if "-file" in sys.argv:
                pass
            elif "-dir" in sys.argv:
                directory = sys.argv[sys.argv.index("-dir") + 1]
                videolist = get_videolist(directory)
                video = videolist[0]

                folder = str(video)[:str(video).rindex("/") + 1]
                oldfilename = str(video)[str(video).rindex("/") + 1:]
                newfilename = oldfilename[:-4] + ".mkv"

                if convert(folder + oldfilename, folder + newfilename):
                    if "-del" in sys.argv:
                        delete(folder + oldfilename)
            else:
                print("Missing directory: ")

            
        elif sys.argv[1] == "convert":
            if "-file" in sys.argv:
                video = sys.argv[sys.argv.index("-file") + 1]
                folder = str(video)[:str(video).rindex("/") + 1]
                oldfilename = str(video)[str(video).rindex("/") + 1:]
                newfilename = oldfilename[:-4] + ".mkv"
                if oldfilename == newfilename:
                    newfilename = oldfilename[:-4] + "[HEVC]"
                
                print(f"***********   converting {oldfilename} to {newfilename}   ***********")
                try:
                    if convert(folder + oldfilename, folder + newfilename):
                        if "-del" in sys.argv:
                            delete(folder + oldfilename)
                except:
                    delete(folder + newfilename)
                    return False
            elif "-dir" in sys.argv:
                directory = sys.argv[sys.argv.index("-dir") + 1]
                videolist = get_videolist(directory)
                counter = 0
                for video in videolist:
                    folder = str(video)[:str(video).rindex("/") + 1]
                    oldfilename = str(video)[str(video).rindex("/") + 1:]
                    newfilename = oldfilename[:-4] + ".mkv"
                    if oldfilename == newfilename:
                        newfilename = oldfilename[:-4] + "[HEVC]"

                    counter += 1
                    print(f"***********   convert {counter} of {len(videolist)}   ***********")
                    try:
                        if convert(folder + oldfilename, folder + newfilename):
                            if "-del" in sys.argv:
                                delete(folder + oldfilename)
                    except:
                        delete(folder + newfilename)
                        return False


def get_wmv_list(path):
    return list(path.rglob("*.[wW][mM][vV]"))

def get_avi_list(path):
    return list(path.rglob("*.[aA][vV][iI]"))

def get_mkv_list(path):
    return list(path.rglob("*.[mM][kK][vV]"))

def get_mp4_list(path):
    return list(path.rglob("*.[mM][pP]4"))

def get_videolist(parentdir):
    videolist = []
    path = Path(parentdir)
    if "-all_wmv" in sys.argv or "-any" in sys.argv:
        videolist += get_wmv_list(path)
    if "-all_avi" in sys.argv or "-any" in sys.argv:
        videolist += get_avi_list(path)
    if "-all_mkv" in sys.argv or "-any" in sys.argv:
        videolist += get_mkv_list(path)
    if "-all_mp4" in sys.argv or "-any" in sys.argv:
        videolist += get_mp4_list(path)
    
    videolist_tmp = videolist
    videolist = [video for video in videolist_tmp if video.is_file()]

    if "-old" in sys.argv:
        videolist = get_old(videolist)
        
    return videolist

def get_old(videolist_temp):
    return [video for video in videolist_temp if get_codec(video) not in ["hevc", "av1"]]

def get_codec(filename):
    try:
        args = ["/usr/bin/ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", str(filename)]
        output = check_output(args, stderr=STDOUT)
    except CalledProcessError:
        print(f"There seams to be an error with {filename}")
        return False
    return output.decode().strip()

def convert(oldfilename, newfilename):
    oldsize = size(Path(oldfilename).stat().st_size)
    print(f"Starting conversion of {oldfilename}({oldsize}) from {get_codec(oldfilename)} ...")

    # Preparing ffmpeg command and input file
    args = ['/usr/bin/ffmpeg', '-i', oldfilename]

    # conversion options
    args += ['-c:v', 'libx265']
    args += ['-max_muxing_queue_size', '1000']

    # conversion output
    args += [newfilename]

    #args = ['/usr/bin/ffmpeg', '-i', oldfilename, newfilename]
    try:
        txt = check_output(args, stderr=STDOUT)
    except CalledProcessError as e:
        print(f"Conversion failed {e}")
        return False
    else:
        newsize = size(Path(newfilename).stat().st_size)
        oldfilename = str(oldfilename)[str(oldfilename).rindex("/") + 1:]
        newfilename = str(newfilename)[str(newfilename).rindex("/") + 1:]
        print(f"Converted {oldfilename}({oldsize}) to {newfilename}({newsize}) successfully")
        return True

def delete(filename):
    try:
        os.remove(filename)
    except OSError:
        print(f"Error deleting {filename}")
        return False

    print(f"Deleted {filename}")
    return True

if __name__ == '__main__':
    main()
