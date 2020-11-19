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

from library.bcolors import BColors
from library.video import Video
from library.medialibrary import MediaLibrary
from library.tools import detect_ffmpeg, user_confirm

def main():
    '''
        MediaCurator's main function
    '''

    # confirm that the command has enough parameters
    if len(sys.argv) < 2:
        print(f"{BColors.FAIL}ERROR: Command not understood, please see documentation.{BColors.ENDC}")

    # confirm that ffmpeg in indeed installed
    ffmpeg_version = detect_ffmpeg()
    if not ffmpeg_version:
        print(f"{BColors.FAIL}No ffmpeg version detected{BColors.ENDC}")
        exit()
    print(f"{BColors.OKBLUE}ffmpeg detected: {ffmpeg_version}{BColors.ENDC}")

    # Get/load command parameters
    directories = []
    files = []
    inputs = []
    filters = []
    outputs = []

    for arg in sys.argv:
        # Confirm with the user that he selected to delete found files
        if "-del" in arg:
            print(f"{BColors.WARNING}WARNING: Delete option selected!{BColors.ENDC}")
            if not user_confirm(f"{BColors.WARNING}Are you sure you wish to delete all found results after selected operations are succesfull ? [Y/N] ?{BColors.ENDC}"):
                print(f"{BColors.OKGREEN}Exiting!{BColors.ENDC}")
                exit()
        elif "-in:" in arg:
            inputs += arg[4:].split(",")
        elif "-filters:" in arg:
            filters += arg[9:].split(",")
        elif "-out:" in arg:
            outputs += arg[5:].split(",")
        elif "-files:" in arg:
            files += arg[7:].split(",,")
        elif "-dir:" in arg:
            directories += arg[5:].split(",,")

    # Loading the media library
    if len(files) > 0:
        medialibrary = MediaLibrary(files = files, inputs = inputs, filters = filters)
    elif len(directories) > 0:
        medialibrary = MediaLibrary(directories = directories, inputs = inputs, filters = filters)
    else:
        print(f"{BColors.FAIL}ERROR: No files or directories selected.{BColors.FAIL}")
        

    # Actions
    if sys.argv[1] == "list":
        for filepath in medialibrary.videos:
            if medialibrary.videos[filepath].useful:
                print(medialibrary.videos[filepath])
            # TODO delete file when -del
    elif sys.argv[1] == "test":
        print(medialibrary)
        exit()
        
    elif sys.argv[1] == "convert":
        counter = 0
        nbuseful = len([filepath for filepath in medialibrary.videos if medialibrary.videos[filepath].useful])
        for filepath in medialibrary.videos:
            if medialibrary.videos[filepath].useful:
                counter += 1
                # Setting required variables
                if "av1" in outputs:
                    vcodec = "av1"
                else:
                    vcodec = "x265"

                # Verbosing
                print(f"{BColors.OKCYAN}******  Starting conversion {counter} of {nbuseful}: '{BColors.OKGREEN}{medialibrary.videos[filepath].filename_origin}{BColors.OKCYAN}' from {BColors.OKGREEN}{medialibrary.videos[filepath].codec}{BColors.OKCYAN} to {BColors.OKGREEN}{vcodec}{BColors.OKCYAN}...{BColors.ENDC}")
                print(f"{BColors.OKGREEN}Original file:{BColors.ENDC}")
                print(medialibrary.videos[filepath])
                print(f"{BColors.OKGREEN}Converting please wait...{BColors.ENDC}")

                # Converting
                if medialibrary.videos[filepath].convert():
                    newvid = Video(medialibrary.videos[filepath].path + medialibrary.videos[filepath].filename_new)
                    print(f"{BColors.OKGREEN}Converted {medialibrary.videos[filepath].filename_origin}{BColors.OKCYAN}({medialibrary.videos[filepath].filesize}mb){BColors.OKGREEN} to {newvid.filename_origin}{BColors.OKCYAN}({newvid.filesize}mb){BColors.OKGREEN} successfully, new file:{BColors.ENDC}")
                    print(newvid)

            # TODO delete file when -del
        


if __name__ == '__main__':
    main()