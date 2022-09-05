#!/usr/bin/env python3
''' This is the library object who holds the information about the workspace and all the videos in it.'''

from pathlib import Path

from .video import Video
from .tools import deletefile

import colorama
colorama.init()

class MediaLibrary():
    ''' This is the library object who holds the information about the workspace and all the videos in it. '''
    
    def __init__(self, files = False, directories = False, inputs = ["any"], filters = [], verbose = False):
        '''
            This is the library object who holds the information about the workspace and all the videos in it.

        Args:
            files = False       : A list of video files
            directories = False : A list of directories containing videos directly or in the subdirectories
            inputs = ["any"]    : A list of filters to keep when browsing the directories
            filters = []        : A list of filters to apply to the videos
            verbose = False     : A list of print options
        Returns:
        '''

        if not files and not directories:
            return
        
        self.directories    = None
        self.inputs         = inputs
        self.filters        = filters
        self.videos         = dict()
        
        if files:
            for filepath in files:
                self.videos[filepath] = Video(filepath, verbose = verbose)

        if directories:
            self.directories    = directories
            self.load_directories(verbose = verbose)
        
        self.filter_videos(verbose = verbose)

    def __str__(self):
        ''' Returns a sting representations about the current instance of the MediaLibrary object

        Args:

        Returns:
            String      :   Information about what the MediaLibrary is tracking
        '''

        if self.directories:
            text = f"MediaCurator is watching the following directories: "
            text += '\n    '.join(map(str, self.directories)) + '\n'
        text += f"MediaCurator is tracking {len(self.videos)} video files"
        return text

    def load_directories(self, verbose = False):
        '''
            Scan folders for video files respecting the inputs requested by the user
            Save them to the videos dictionary

        Args:
            verbose = False     : A list of print options
        
        Returns:
        '''

        print(f"{colorama.Fore.GREEN}Scanning files in {', '.join(map(str, self.directories))} for videos{colorama.Fore.RESET}")
        videolist = []
        
        for directory in self.directories:
            path = Path(directory)
            # get all video filetypes
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
            if "vob" in self.inputs or "any" in self.inputs or len(self.inputs) < 1:
                videolist += list(path.rglob("*.[vV][oO][bB]"))
            if "divx" in self.inputs or "any" in self.inputs or len(self.inputs) < 1:
                videolist += list(path.rglob("*.[dD][iI][vV][xX]"))
            if "ogm" in self.inputs or "any" in self.inputs or len(self.inputs) < 1:
                videolist += list(path.rglob("*.[oO][gG][mM]"))
            if "webm" in self.inputs or "any" in self.inputs or len(self.inputs) < 1:
                videolist += list(path.rglob("*.[wW][eE][bB][mM]"))
        
        # Remove folders
        videolist_tmp = videolist
        videolist = [video for video in videolist_tmp if video.is_file()]

        # Map it all to the videos dictionary as initiated Video objects
        print(f"{colorama.Fore.GREEN}Analazing {len(videolist)} videos in {', '.join(map(str, self.directories))}{colorama.Fore.RESET}")
        iteration = 0
        for video in videolist:
            if verbose:
                iteration += 1
                print(f'{int((iteration / len(videolist )* 100))}% complete', end='\r')
            
            self.videos[video] = Video(video, verbose = verbose)

    def filter_videos(self, verbose = False):
        ''' Mark useless videos in the videos dictionary (default is useful)

        Args:
            verbose = False     : A list of print options
        
        Returns:
        '''

        print(f"{colorama.Fore.GREEN}Filtering {len(self.videos)} videos for the requested parameters{colorama.Fore.RESET}")

        for filepath in self.videos:

            # filter for filetypes
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
            if self.videos[filepath].useful and len([filtr for filtr in self.filters if filtr in ["lowres", "hd", "subsd", "sd", "720p", "1080p", "uhd"]]) > 0:
                useful = False

                if "subsd" in self.filters and self.videos[filepath].definition in ["subsd"]:
                    useful = True
                if "sd" in self.filters and self.videos[filepath].definition in ["sd"]:
                    useful = True
                if "720p" in self.filters and self.videos[filepath].definition in ["720p"]:
                    useful = True
                if "1080p" in self.filters and self.videos[filepath].definition in ["1080p"]:
                    useful = True
                if "uhd" in self.filters and self.videos[filepath].definition in ["uhd"]:
                    useful = True
                if "lowres" in self.filters and self.videos[filepath].definition in ["subsd", "sd"]:
                    useful = True
                if "hd" in self.filters and self.videos[filepath].definition in ["720p", "1080p", "uhd"]:
                    useful = True
                self.videos[filepath].useful = useful

            # keep video if useful and user wants to also filter when there is an ffmpeg errors
            if self.videos[filepath].useful and len([filtr for filtr in self.filters if filtr in ["fferror"]]) > 0:
                useful = False
                if self.videos[filepath].error:
                    useful = True
                self.videos[filepath].useful = useful

            
        print(f"{colorama.Fore.GREEN}Found {len([filepath for filepath in self.videos if self.videos[filepath].useful])} videos for the requested parameters{colorama.Fore.RESET}")

    def unwatch(self, filepath, delete = False):
        ''' remove a video from the index and delete it if requested

        Args:
            filepath            :    A string containing the full filepath
            delete = False      :    Delete the file as well as removing it from the library
        
        Returns:
            boolean             :   Operation success
        '''
        
        if delete:
            deletefile(filepath)
        try:
            video = self.videos.pop(filepath)
            if video:
                return video
        except KeyError:
            pass
        return False