#!/usr/bin/env python3
''' This module defines the MediaLibrary class, which manages information about the workspace and all videos in it.'''

from pathlib import Path

from .video import Video
from .tools import deletefile

# Import colorama for colored output
import colorama
colorama.init()

# Define color codes for colored output
cgreen = colorama.Fore.GREEN
creset = colorama.Fore.RESET

class MediaLibrary():
    '''This class manages information about the workspace and all videos in it.'''

    def __init__(self, files=False, directories=False, inputs=["any"], filters=[], verbose=False):
        '''
        Initializes a MediaLibrary instance with provided parameters.

        Args:
            files (list or False): A list of video files.
            directories (list or False): A list of directories containing videos directly or in subdirectories.
            inputs (list): A list of filters to keep when browsing the directories.
            filters (list): A list of filters to apply to the videos.
            verbose (bool): A flag to enable verbose output.
        '''

        if not files and not directories:
            return
        
        self.directories = None
        self.inputs = inputs
        self.filters = filters
        self.videos = dict()
        
        if files:
            for filepath in files:
                self.videos[filepath] = Video(filepath, verbose=verbose)

        if directories:
            self.directories = directories
            self.load_directories(verbose=verbose)
        
        self.filter_videos(verbose=verbose)

    def __str__(self):
        '''
        Returns a string representation of the MediaLibrary instance.

        Returns:
            str: Information about the MediaLibrary instance.
        '''

        text = ""
        if self.directories:
            text += f"MediaCurator is watching the following directories: "
            text += '\n    '.join(map(str, self.directories)) + '\n'
        text += f"MediaCurator is tracking {len(self.videos)} video files"
        return text

    def load_directories(self, verbose=False):
        '''
        Scans folders for video files respecting the inputs requested by the user and saves them to the videos dictionary.

        Args:
            verbose (bool): A flag to enable verbose output.
        '''

        print(f"{cgreen}Scanning files in {', '.join(map(str, self.directories))} for videos{creset}")
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
            if "mpeg" in self.inputs or "any" in self.inputs or len(self.inputs) < 1:
                videolist += list(path.rglob("*.[mM][pP][eE][gG]"))
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
        print(f"{cgreen}Analyzing {len(videolist)} videos in {', '.join(map(str, self.directories))}{creset}")
        iteration = 0
        for video in videolist:
            if verbose:
                iteration += 1
                print(f'{int((iteration / len(videolist) * 100))}% complete', end='\r')
            
            self.videos[video] = Video(video, verbose=verbose)

    def filter_videos(self, verbose=False):
        '''
        Marks videos for operation in the videos dictionary (default is not to operate).

        Args:
            verbose (bool): A flag to enable verbose output.
        '''

        print(f"{cgreen}Filtering {len(self.videos)} videos for the requested parameters{creset}")

        for filepath in self.videos:

            # Filter for filetypes
            if len([filtr for filtr in self.filters if filtr in ["old", "mpeg4", "mpeg", "wmv3", "wmv", "h264", "hevc", "x265", "av1"]]) > 0:
                operate = False
                if "old" in self.filters and self.videos[filepath].codec not in ["hevc", "av1"]:
                    operate = True
                if ("mpeg4" in self.filters or "mpeg" in self.filters) and self.videos[filepath].codec in ["mpeg4", "msmpeg4v3"]:
                    operate = True
                if "mpeg" in self.filters and self.videos[filepath].codec in ["mpeg1video"]:
                    operate = True
                if ("wmv3" in self.filters or "wmv" in self.filters) and self.videos[filepath].codec in ["wmv3"]:
                    operate = True
                if "h264" in self.filters and self.videos[filepath].codec in ["h264"]:
                    operate = True
                if ("hevc" in self.filters or "x265" in self.filters) and self.videos[filepath].codec in ["hevc"]:
                    operate = True
                if "av1" in self.filters and self.videos[filepath].codec in ["av1"]:
                    operate = True
                self.videos[filepath].operate = operate

            # Keep video for operation if specified resolution
            if self.videos[filepath].operate and len([filtr for filtr in self.filters if filtr in ["lowres", "hd", "subsd", "sd", "720p", "1080p", "uhd"]]) > 0:
                operate = False

                if "subsd" in self.filters and self.videos[filepath].definition in ["subsd"]:
                    operate = True
                if "sd" in self.filters and self.videos[filepath].definition in ["sd"]:
                    operate = True
                if "720p" in self.filters and self.videos[filepath].definition in ["720p"]:
                    operate = True
                if "1080p" in self.filters and self.videos[filepath].definition in ["1080p"]:
                    operate = True
                if "uhd" in self.filters and self.videos[filepath].definition in ["uhd"]:
                    operate = True
                if "lowres" in self.filters and self.videos[filepath].definition in ["subsd", "sd"]:
                    operate = True
                if "hd" in self.filters and self.videos[filepath].definition in ["720p", "1080p", "uhd"]:
                    operate = True
                self.videos[filepath].operate = operate

            # Keep video for operation if ffmpeg error exists
            if self.videos[filepath].operate and len([filtr for filtr in self.filters if filtr in ["fferror"]]) > 0:
                operate = False
                if self.videos[filepath].error:
                    operate = True
                self.videos[filepath].operate = operate
            
        print(f"{cgreen}Found {len([filepath for filepath in self.videos if self.videos[filepath].operate])} videos for the requested parameters{creset}")

    def unwatch(self, filepath, delete=False):
        '''
        Removes a video from the index and deletes it if requested.

        Args:
            filepath (str): The full filepath of the video.
            delete (bool): If True, delete the file as well as removing it from the library.

        Returns:
            bool: True if operation successful, False otherwise.
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
