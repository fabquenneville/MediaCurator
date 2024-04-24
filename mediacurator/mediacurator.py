#!/usr/bin/env python3
'''
    MediaCurator is a Python command line tool to manage a media database.
        * List all the video's and their codecs with or without filters
        * Batch recode videos to more modern codecs (x265 / AV1) based on filters: extentions, codecs ...
    ex:
    mediacurator list -in:any -filters:old -dirs:/mnt/media/ >> ../medlist.txt
    mediacurator convert -del -in:any -filters:mpeg4 -out:x265,mkv -dirs:"/mnt/media/Movies/"
    mediacurator convert -del  -in:avi,mpg -dirs:/mnt/media/
'''

import sys

# Normal import
try:
    from mediacurator.library.video import Video
    from mediacurator.library.medialibrary import MediaLibrary
    from mediacurator.library.tools import detect_ffmpeg, user_confirm, load_arguments
# Allow local import for development purposes
except ModuleNotFoundError:
    from library.video import Video
    from library.medialibrary import MediaLibrary
    from library.tools import detect_ffmpeg, user_confirm, load_arguments

# Import colorama for colored output
import colorama
colorama.init()

# Define color codes for colored output
ccyan = colorama.Fore.CYAN
cblue = colorama.Fore.BLUE
cgreen = colorama.Fore.GREEN
cred = colorama.Fore.RED
creset = colorama.Fore.RESET

def main():
    '''
    MediaCurator's main function
    
    Returns:
    '''

    print(f"{colorama.Style.BRIGHT}")

    # confirm that the command has enough parameters
    if len(sys.argv) < 2:
        print(f"{cred}ERROR: Command not understood, please see documentation.{creset}")

    # confirm that ffmpeg in indeed installed
    ffmpeg_version = detect_ffmpeg()
    if not ffmpeg_version:
        print(f"{cred}No ffmpeg version detected{creset}")
        exit()
    print(f"{cblue}ffmpeg version detected: {ffmpeg_version}{creset}")

    # Get/load command parameters
    arguments = load_arguments()

    # Loading the media library
    if len(arguments["files"]) > 0:
        medialibrary = MediaLibrary(files = arguments["files"], inputs = arguments["inputs"], filters = arguments["filters"])
    elif len(arguments["directories"]) > 0:
        medialibrary = MediaLibrary(directories = arguments["directories"], inputs = arguments["inputs"], filters = arguments["filters"])
    else:
        print(f"{cred}ERROR: No files or directories selected.{creset}")
        return

    # Actions
    if sys.argv[1] == "list":
        # Pulling list of marked videos / original keys for the medialibrary.videos dictionary
        keylist = [filepath for filepath in medialibrary.videos if medialibrary.videos[filepath].operate]
        keylist.sort()

        for filepath in keylist:
            if medialibrary.videos[filepath].operate:
                if "formated" in arguments["printop"] or "verbose" in arguments["printop"]:
                    if medialibrary.videos[filepath].error:
                        print(f"{cred}{medialibrary.videos[filepath].fprint()}{creset}")
                    else:
                        print(medialibrary.videos[filepath].fprint())
                else:
                    if medialibrary.videos[filepath].error:
                        print(f"{cred}{medialibrary.videos[filepath]}{creset}")
                    else:
                        print(medialibrary.videos[filepath])

                # if marked for deletion delete and unwatch the video
                if "-del" in sys.argv:
                    medialibrary.unwatch(filepath, delete = True)
    elif sys.argv[1] == "test":
        # Pulling list of marked videos / original keys for the medialibrary.videos dictionary
        keylist = [filepath for filepath in medialibrary.videos if medialibrary.videos[filepath].operate]
        keylist.sort()

        for filepath in keylist:
            if medialibrary.videos[filepath].operate:
                if "formated" in arguments["printop"] or "verbose" in arguments["printop"]:
                    if medialibrary.videos[filepath].error:
                        print(f"{cred}{medialibrary.videos[filepath].fprint()}{creset}")
                    else:
                        print(medialibrary.videos[filepath].fprint())
                else:
                    if medialibrary.videos[filepath].error:
                        print(f"{cred}{medialibrary.videos[filepath]}{creset}")
                    else:
                        print(medialibrary.videos[filepath])

                # if marked for deletion delete and unwatch the video
                if "-del" in sys.argv:
                    medialibrary.unwatch(filepath, delete = True)
        
    elif sys.argv[1] == "convert":
        counter = 0

        # Pulling list of marked videos / original keys for the medialibrary.videos dictionary
        keylist = [filepath for filepath in medialibrary.videos if medialibrary.videos[filepath].operate]
        keylist.sort()

        for filepath in keylist:
            counter += 1
            # Setting required variables
            if "av1" in arguments["outputs"]:
                vcodec = "av1"
            else:
                vcodec = "x265"

            # Verbosing
            print(f"{cgreen}******  Starting conversion {counter} of {len(keylist)}: '{ccyan}{medialibrary.videos[filepath].filename_origin}{cgreen}' from {ccyan}{medialibrary.videos[filepath].codec}{cgreen} to {ccyan}{vcodec}{cgreen}...{creset}")
            print(f"{ccyan}Original file:{creset}")
            if "formated" in arguments["printop"] or "verbose" in arguments["printop"]:
                print(medialibrary.videos[filepath].fprint())
            else:
                print(medialibrary.videos[filepath])

            print(f"{cgreen}Converting please wait...{creset}", end="\r")

            # Converting
            if medialibrary.videos[filepath].convert(verbose = "verbose" in arguments["printop"]):
                # Mark the job as done
                medialibrary.videos[filepath].operate = False

                # Scan the new video
                newfpath = medialibrary.videos[filepath].path + medialibrary.videos[filepath].filename_new
                
                medialibrary.videos[newfpath] = Video(newfpath, verbose = "verbose" in arguments["printop"])

                # Verbose
                print(f"{cgreen}Successfully converted '{medialibrary.videos[filepath].filename_origin}'{ccyan}({medialibrary.videos[filepath].filesize}mb){cgreen} to '{medialibrary.videos[newfpath].filename_origin}'{ccyan}({medialibrary.videos[newfpath].filesize}mb){cgreen}, {ccyan}new file:{creset}")

                if "formated" in arguments["printop"] or "verbose" in arguments["printop"]:
                    if medialibrary.videos[newfpath].error:
                        print(f"{cred}{medialibrary.videos[newfpath].fprint()}{creset}")
                    else:
                        print(medialibrary.videos[newfpath].fprint())
                else:
                    if medialibrary.videos[newfpath].error:
                        print(f"{cred}{medialibrary.videos[newfpath]}{creset}")
                    else:
                        print(medialibrary.videos[newfpath])

                # if marked for deletion delete and unwatch the video
                if "-del" in sys.argv:
                    medialibrary.unwatch(filepath, delete = True)

if __name__ == '__main__':
    main()
