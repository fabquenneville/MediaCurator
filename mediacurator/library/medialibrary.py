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
            self.directories = directories
        else:
            return
        
        self.inputs = inputs
        self.filters = filters
        
        self.load_videolist()
        


    def __str__(self):
        ''' print '''
        text = f"MediaCurator watching: "
        if self.directories:
            text += f"{', '.join(map(str, self.directories))}"
        return text


    def load_videolist(self):
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

        video = Video(videolist[0])





        #videolist = list(dict.fromkeys(videolist))
        print(video)
        exit()



        
        # # Filter the list for specific codecs
        # videolist_tmp = videolist
        # print(f"{BColors.OKGREEN}Filtering {len(videolist)} videos for the requested parameters{BColors.ENDC}")
        # if len([filt for filt in self.filters if filt not in ["lowres", "hd", "720p", "1080p", "uhd", "fferror"]]) > 0:
        #     videolist = []

        #     if "old" in self.filters:
        #         videolist += [video for video in videolist_tmp if get_codec(video) not in ["hevc", "av1"]]

        #     if "mpeg4" in self.filters or "mpeg" in self.filters:
        #         videolist += [video for video in videolist_tmp if get_codec(video) in ["mpeg4", "msmpeg4v3"]]

        #     if "mpeg" in self.filters:
        #         videolist += [video for video in videolist_tmp if get_codec(video) in ["mpeg1video"]]

        #     if "wmv3" in self.filters or "wmv" in self.filters:
        #         videolist += [video for video in videolist_tmp if get_codec(video) in ["wmv3"]]

        #     if "x264" in self.filters:
        #         videolist += [video for video in videolist_tmp if get_codec(video) in ["x264"]]
            
        # if len(self.filters) > 0 and "lowres" in self.filters:
        #     videolist_tmp = videolist
        #     videolist = [video for video in videolist_tmp if get_resolution(video)[1] < 1280 or get_resolution(video)[0] <= 480]
        # elif len(self.filters) > 0 and "hd" in self.filters:
        #     videolist_tmp = videolist
        #     videolist = [video for video in videolist_tmp if get_resolution(video)[1] >= 1280 or get_resolution(video)[0] >= 720]
        # elif len(self.filters) > 0 and "720p" in self.filters:
        #     videolist_tmp = videolist
        #     videolist = [video for video in videolist_tmp if get_resolution(video)[1] >= 1280 or get_resolution(video)[0] == 720]
        # elif len(self.filters) > 0 and "1080p" in self.filters:
        #     videolist_tmp = videolist
        #     videolist = [video for video in videolist_tmp if (get_resolution(video)[1] >= 1440 and get_resolution(video)[1] < 3840) or get_resolution(video)[0] == 1080]
        # elif len(self.filters) > 0 and "uhd" in self.filters:
        #     videolist_tmp = videolist
        #     videolist = [video for video in videolist_tmp if get_resolution(video)[1] >= 3840 or get_resolution(video)[0] >= 2160]

        # if len(self.filters) > 0 and "fferror" in self.filters:
        #     videolist_tmp = videolist
        #     videolist = [video for video in videolist_tmp if get_fferror(video)]

        # print(f"{BColors.OKGREEN}Found {len(videolist)} videos for the requested parameters{BColors.ENDC}")

        # # remove doubles and return
        # return list(dict.fromkeys(videolist))

