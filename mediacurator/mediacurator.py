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


import colorama
colorama.init()

def main():
    '''
        MediaCurator's main function

    Args:

    Returns:
    '''

    print(f"{colorama.Style.BRIGHT}")

    # confirm that the command has enough parameters
    if len(sys.argv) < 2:
        print(f"{colorama.Fore.RED}ERROR: Command not understood, please see documentation.{colorama.Fore.RESET}")

    # confirm that ffmpeg in indeed installed
    ffmpeg_version = detect_ffmpeg()
    if not ffmpeg_version:
        print(f"{colorama.Fore.RED}No ffmpeg version detected{colorama.Fore.RESET}")
        exit()
    print(f"{colorama.Fore.BLUE}ffmpeg version detected: {ffmpeg_version}{colorama.Fore.RESET}")

    # Get/load command parameters
    arguments = load_arguments()

    # Loading the media library
    if len(arguments["files"]) > 0:
        medialibrary = MediaLibrary(files = arguments["files"], inputs = arguments["inputs"], filters = arguments["filters"])
    elif len(arguments["directories"]) > 0:
        medialibrary = MediaLibrary(directories = arguments["directories"], inputs = arguments["inputs"], filters = arguments["filters"])
    else:
        print(f"{colorama.Fore.RED}ERROR: No files or directories selected.{colorama.Fore.RESET}")
        return
        

    # Actions
    if sys.argv[1] == "list":

        # Pulling list of marked videos / original keys for the medialibrary.videos dictionary
        keylist = [filepath for filepath in medialibrary.videos if medialibrary.videos[filepath].useful]
        keylist.sort()

        for filepath in keylist:
            if medialibrary.videos[filepath].useful:
                if "formated" in arguments["printop"] or "verbose" in arguments["printop"]:
                    if medialibrary.videos[filepath].error:
                        print(f"{colorama.Fore.RED}{medialibrary.videos[filepath].fprint()}{colorama.Fore.RESET}")
                    else:
                        print(medialibrary.videos[filepath].fprint())
                else:
                    if medialibrary.videos[filepath].error:
                        print(f"{colorama.Fore.RED}{medialibrary.videos[filepath]}{colorama.Fore.RESET}")
                    else:
                        print(medialibrary.videos[filepath])

                # if marked for deletion delete and unwatch the video
                if "-del" in sys.argv:
                    medialibrary.unwatch(filepath, delete = True)
    elif sys.argv[1] == "test":

        # Pulling list of marked videos / original keys for the medialibrary.videos dictionary
        keylist = [filepath for filepath in medialibrary.videos if medialibrary.videos[filepath].useful]
        keylist.sort()

        for filepath in keylist:
            if medialibrary.videos[filepath].useful:
                if "formated" in arguments["printop"] or "verbose" in arguments["printop"]:
                    if medialibrary.videos[filepath].error:
                        print(f"{colorama.Fore.RED}{medialibrary.videos[filepath].fprint()}{colorama.Fore.RESET}")
                    else:
                        print(medialibrary.videos[filepath].fprint())
                else:
                    if medialibrary.videos[filepath].error:
                        print(f"{colorama.Fore.RED}{medialibrary.videos[filepath]}{colorama.Fore.RESET}")
                    else:
                        print(medialibrary.videos[filepath])

                # if marked for deletion delete and unwatch the video
                if "-del" in sys.argv:
                    medialibrary.unwatch(filepath, delete = True)
        
    elif sys.argv[1] == "convert":
        counter = 0

        # Pulling list of marked videos / original keys for the medialibrary.videos dictionary
        keylist = [filepath for filepath in medialibrary.videos if medialibrary.videos[filepath].useful]
        keylist.sort()

        for filepath in keylist:
            counter += 1
            # Setting required variables
            if "av1" in arguments["outputs"]:
                vcodec = "av1"
            else:
                vcodec = "x265"

            # Verbosing
            print(f"{colorama.Fore.GREEN}******  Starting conversion {counter} of {len(keylist)}: '{colorama.Fore.CYAN}{medialibrary.videos[filepath].filename_origin}{colorama.Fore.GREEN}' from {colorama.Fore.CYAN}{medialibrary.videos[filepath].codec}{colorama.Fore.GREEN} to {colorama.Fore.CYAN}{vcodec}{colorama.Fore.GREEN}...{colorama.Fore.RESET}")
            print(f"{colorama.Fore.CYAN}Original file:{colorama.Fore.RESET}")
            if "formated" in arguments["printop"] or "verbose" in arguments["printop"]:
                print(medialibrary.videos[filepath].fprint())
            else:
                print(medialibrary.videos[filepath])

            print(f"{colorama.Fore.GREEN}Converting please wait...{colorama.Fore.RESET}", end="\r")

            # Converting
            if medialibrary.videos[filepath].convert(verbose = "verbose" in arguments["printop"]):
                # Mark the job as done
                medialibrary.videos[filepath].useful = False

                # Scan the new video
                newfpath = medialibrary.videos[filepath].path + medialibrary.videos[filepath].filename_new
                
                medialibrary.videos[newfpath] = Video(newfpath, verbose = "verbose" in arguments["printop"])

                # Verbose
                print(f"{colorama.Fore.GREEN}Successfully converted '{medialibrary.videos[filepath].filename_origin}'{colorama.Fore.CYAN}({medialibrary.videos[filepath].filesize}mb){colorama.Fore.GREEN} to '{medialibrary.videos[newfpath].filename_origin}'{colorama.Fore.CYAN}({medialibrary.videos[newfpath].filesize}mb){colorama.Fore.GREEN}, {colorama.Fore.CYAN}new file:{colorama.Fore.RESET}")


                if "formated" in arguments["printop"] or "verbose" in arguments["printop"]:
                    if medialibrary.videos[newfpath].error:
                        print(f"{colorama.Fore.RED}{medialibrary.videos[newfpath].fprint()}{colorama.Fore.RESET}")
                    else:
                        print(medialibrary.videos[newfpath].fprint())
                else:
                    if medialibrary.videos[newfpath].error:
                        print(f"{colorama.Fore.RED}{medialibrary.videos[newfpath]}{colorama.Fore.RESET}")
                    else:
                        print(medialibrary.videos[newfpath])

                # if marked for deletion delete and unwatch the video
                if "-del" in sys.argv:
                    medialibrary.unwatch(filepath, delete = True)


        


if __name__ == '__main__':
    main()