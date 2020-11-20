#!/usr/bin/env python3
'''
    This is the container for all the videos found in the folders passed by the user
'''

from pathlib import Path
import sys

from .bcolors import BColors
from .video import Video
from .tools import deletefile

class MediaLibrary():
    '''
        Contains the information and methods of a video file.
    '''

    size = int()
    videos = dict()
    directories = list()
    inputs = []
    filters = []

    def __init__(self, files = False, directories = False, inputs = ["any"], filters = [], verbose = False):
        '''
            This is the library object who holds the information about the workspace and all the videos in it.
        '''
        if files:
            for filepath in files:
                self.videos[filepath] = Video(filepath, verbose = verbose)

        elif directories:
            self.directories    = directories
        else:
            return
        
        self.inputs             = inputs
        self.filters            = filters
        
        self.load_videos(verbose = verbose)

        self.filter_videos()


        


    def __str__(self):
        ''' print '''
        if self.directories:
            text = f"MediaCurator is watching the following directories: "
            text += '\n    '.join(map(str, self.directories)) + '\n'
        text += f"MediaCurator is tracking {len(self.videos)} video files"

        return text

    def load_videos(self, verbose = False):
        '''
            Scan folders for video files respecting the inputs requested by the user
            Save them to the videos dictionary
        '''

        print(f"{BColors.OKGREEN}Scanning files in {', '.join(map(str, self.directories))} for videos{BColors.ENDC}")
        videolist = []
        
        for directory in self.directories:
            path = Path(directory)
            if "wmv" in self.inputs or "any" in self.inputs or len(self.inputs) < 1:
                videolist += list(path.rglob("*.[wW][mM][vV]"))
            if "avi" in self.inputs or "any" in self.inputs or len(self.inputs) < 1:
                videolist += list(path.rglob("*.[aA][vV][iI]"))
            if "mkv" in self.inputs or "any" in self.inputs or len(self.inputs) < 1:
                videolist += list(path.rglob("*.[mM][kK][vV]"))
            if "mp4" in self.inputs or "any" in self.inputs or len(self.inputs) < 1:
                videolist += list(path.rglob("*.[mM][pP]4"))
            if "m4v" in self.inputs or "any" in self.inputs or len(self.inputs) < 1:
                videolist += list(path.rglob("*.[mM]4[vV]"))
            if "flv" in self.inputs or "any" in self.inputs or len(self.inputs) < 1:
                videolist += list(path.rglob("*.[fF][lL][vV]"))
            if "mpg" in self.inputs or "any" in self.inputs or len(self.inputs) < 1:
                videolist += list(path.rglob("*.[mM][pP][gG]"))
            if "vid" in self.inputs or "any" in self.inputs or len(self.inputs) < 1:
                videolist += list(path.rglob("*.[vV][iI][dD]"))
        
        # Remove folders
        videolist_tmp = videolist
        videolist = [video for video in videolist_tmp if video.is_file()]

        # Map it all to the videos dictionary as initiated Video objects
        print(f"{BColors.OKGREEN}Analazing {len(videolist)} videos in {', '.join(map(str, self.directories))}{BColors.ENDC}")
        iteration = 0
        for video in videolist:
            if "-verbose" in sys.argv:
                iteration += 1
                print(f'{int((iteration / len(videolist )* 100))}% complete', end='\r')
            
            self.videos[video] = Video(video, verbose = verbose)

    def filter_videos(self):
        '''
            Mark useless videos in the videos dictionary
        '''
        
        print(f"{BColors.OKGREEN}Filtering {len(self.videos)} videos for the requested parameters{BColors.ENDC}")


        iteration = 0
        for filepath in self.videos:
            if "-verbose" in sys.argv:
                iteration += 1
                print(f'{int((iteration / len(self.videos)* 100))}% complete', end='\r')


            if len([filtr for filtr in self.filters if filtr in ["old", "mpeg4", "mpeg", "wmv3", "wmv", "h264", "hevc", "x265", "av1"]]) > 0:
                useful = False

                if "old" in self.filters and self.videos[filepath].codec not in ["hevc", "av1"]:
                    useful = True

                if ("mpeg4" in self.filters or "mpeg" in self.filters) and self.videos[filepath].codec in ["mpeg4", "msmpeg4v3"]:
                    useful = True


                if "mpeg" in self.filters and self.videos[filepath].codec in ["mpeg1video"]:
                    useful = True

                if ("wmv3" in self.filters or "wmv" in self.filters) and self.videos[filepath].codec in ["wmv3"]:
                    useful = True

                if "h264" in self.filters and self.videos[filepath].codec in ["h264"]:
                    useful = True

                if ("hevc" in self.filters or "x265" in self.filters) and self.videos[filepath].codec in ["hevc"]:
                    useful = True

                if "av1" in self.filters and self.videos[filepath].codec in ["av1"]:
                    useful = True
                
                self.videos[filepath].useful = useful
            
            

            # keep video if useful and user wants to also filter by selected resolutions
            if self.videos[filepath].useful and len([filtr for filtr in self.filters if filtr in ["lowres", "hd", "720p", "1080p", "uhd"]]) > 0:
                useful = False

                if "lowres" in self.filters and self.videos[filepath].definition in ["sd"]:
                    useful = True
                if "hd" in self.filters and self.videos[filepath].definition in ["720p", "1080p", "uhd"]:
                    useful = True
                if "720p" in self.filters and self.videos[filepath].definition in ["720p"]:
                    useful = True
                if "1080p" in self.filters and self.videos[filepath].definition in ["1080p"]:
                    useful = True
                if "uhd" in self.filters and self.videos[filepath].definition in ["uhd"]:
                    useful = True

                self.videos[filepath].useful = useful

            # keep video if useful and user wants to also filter when there is an ffmpeg errors
            if self.videos[filepath].useful and len([filtr for filtr in self.filters if filtr in ["fferror"]]) > 0:
                
                useful = False

                if self.videos[filepath].error:
                    useful = True

                self.videos[filepath].useful = useful

            
        print(f"{BColors.OKGREEN}Found {len([filepath for filepath in self.videos if self.videos[filepath].useful])} videos for the requested parameters{BColors.ENDC}")

    def unwatch(self, filepath, delete = False):
        ''' remove a video from the index and delete it if requested'''
        # If the user wanted to delete the film and 
        if delete:
            deletefile(filepath)
        try:
            video = self.videos.pop(filepath)
            if video:
                return video
        except KeyError:
            pass
        return False