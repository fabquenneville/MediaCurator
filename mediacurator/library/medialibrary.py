#!/usr/bin/env python3
'''
    This is the container for all the videos found in the folders passed by the user
'''

from pathlib import Path

from .bcolors import BColors
from .video import Video

class MediaLibrary():
    '''
        Contains the information and methods of a video file.
    '''

    size = int()
    videos = dict()
    directories = list()
    inputs = []
    filters = []

    def __init__(self, files = False, directories = False, inputs = ["any"], filters = []):
        '''
            This is the library object who holds the information about the workspace and all the videos in it.
        '''
        if files:
            pass
            # self.files = files
        elif directories:
            self.directories    = directories
        else:
            return
        
        self.inputs             = inputs
        self.filters            = filters
        
        self.load_videos()

        self.filter_videos()

        for filepath in self.videos:
            # if self.videos[filepath].useful:
            #     print(self.videos[filepath])
            print(self.videos[filepath])


        


    def __str__(self):
        ''' print '''
        text = f"MediaCurator watching: "
        if self.directories:
            text += f"{', '.join(map(str, self.directories))}"
        return text

    def load_videos(self):
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
            iteration += 1
            #print(int(iteration / len(videolist)))
            #print(f'{iteration} / {len(videolist)}% complete    {int(iteration / len(videolist))}% complete', end='\r')
            print(f'{int((iteration / len(videolist )* 100))}% complete', end='\r')
            self.videos[video] = Video(video)

    def filter_videos(self):
        '''
            Mark useless videos in the videos dictionary
        '''
        
        print(f"{BColors.OKGREEN}Filtering {len(self.videos)} videos for the requested parameters{BColors.ENDC}")

        iteration = 0
        for filepath in self.videos:
            iteration += 1
            print(f'{int((iteration / len(self.videos)* 100))}% complete', end='\r')

            # Filter for codecs if codec filter passed by user
            if len([filt for filt in self.filters if filt not in ["lowres", "hd", "720p", "1080p", "uhd", "fferror"]]) > 0:
                useful = False
                if "old" in self.filters and self.videos[filepath].codec not in ["hevc", "av1"]:
                    useful = True

                if ("mpeg4" in self.filters or "mpeg" in self.filters) and self.videos[filepath].codec in ["mpeg4", "msmpeg4v3"]:
                    useful = True

                if "mpeg" in self.filters and self.videos[filepath].codec in ["mpeg1video"]:
                    useful = True

                if ("wmv3" in self.filters or "wmv" in self.filters) and self.videos[filepath].codec in ["wmv3"]:
                    useful = True

                if "x264" in self.filters and self.videos[filepath].codec in ["x264"]:
                    useful = True
                
                self.videos[filepath].useful = useful





