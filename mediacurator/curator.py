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
        pass
        # if "av1" in outputs:
        #     codec = "av1"
        # else:
        #     codec = "x265"
        # if any("-files" in argv for argv in sys.argv):
        #     video = sys.argv[sys.argv.index("-files") + 1]
        #     folder = str(video)[:str(video).rindex("/") + 1]
        #     oldfilename = str(video)[str(video).rindex("/") + 1:]

        #     # Setting new filename
        #     if "mp4" in outputs:
        #         newfilename = oldfilename[:-4] + ".mp4"
        #         if oldfilename == newfilename:
        #             newfilename = oldfilename[:-4] + "[HEVC]" + ".mp4"
        #     else:
        #         newfilename = oldfilename[:-4] + ".mkv"
        #         if oldfilename == newfilename:
        #             newfilename = oldfilename[:-4] + "[HEVC]" + ".mkv"
            

            
        #     print(f"{BColors.OKCYAN}***********   converting {oldfilename} to {newfilename} ({codec})  ***********{BColors.ENDC}")
        #     try:
        #         if convert(folder + oldfilename, folder + newfilename, codec):
        #             #subprocess.call(['chown', f"{getuser()}:{getuser()}", folder + newfilename])
        #             subprocess.call(['chmod', '777', folder + newfilename])
        #             if "-del" in sys.argv:
        #                 delete(folder + oldfilename)
        #         else:
        #             delete(folder + newfilename)
        #             return False
        #     except:
        #         delete(folder + newfilename)
        #         return False
        # elif any("-dir" in argv for argv in sys.argv):
        #     videolist = []
        #     for directory in directories:
        #         videolist += get_videolist(directory, inputs, filters)
        #     videolist.sort()
        #     counter = 0
        #     for video in videolist:
        #         folder = str(video)[:str(video).rindex("/") + 1]
        #         oldfilename = str(video)[str(video).rindex("/") + 1:]

        #         if "mp4" in outputs:
        #             newfilename = oldfilename[:-4] + ".mp4"
        #             if oldfilename == newfilename:
        #                 newfilename = oldfilename[:-4] + "[HEVC]" + ".mp4"
        #         else:
        #             newfilename = oldfilename[:-4] + ".mkv"
        #             if oldfilename == newfilename:
        #                 newfilename = oldfilename[:-4] + "[HEVC]" + ".mkv"

        #         counter += 1
        #         print(f"{BColors.OKCYAN}***********   convert {counter} of {len(videolist)}   ***********{BColors.ENDC}")
        #         try:
        #             if convert(folder + oldfilename, folder + newfilename, codec):
        #                 #output = (['chown', f"{getuser()}:{getuser()}", folder + newfilename], stderr=subprocess.STDOUT)
        #                 #output = (['chown', f"{getuser()}:{getuser()}", folder + newfilename], stderr=subprocess.STDOUT)
        #                 subprocess.call(['chmod', '777', folder + newfilename])
        #                 if "-del" in sys.argv:
        #                     delete(folder + oldfilename)
        #         except:
        #             delete(folder + newfilename)
        #             return False
    
if __name__ == '__main__':
    main()