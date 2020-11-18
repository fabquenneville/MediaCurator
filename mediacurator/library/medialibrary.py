#!/usr/bin/env python3
'''
    This is the container for all the videos found in the folders passed by the user
'''

from .bcolors import BColors

class MediaLibrary():
    '''
        Contains the information and methods of a video file.
    '''

    size = int()
    videos = dict()
    directories = list()

    def __init__(self, files = False, directories = False):
        '''
        '''
        if files:
            pass
            # self.files = files
        elif directories:
            self.directories = directories


    def __str__(self):
        ''' print '''
        if self.directories:
            return f"MediaCurator watching: {', '.join(map(str, self.directories))}"

    # def delete(filename):
    #     try:
    #         os.remove(filename)
    #     except OSError:
    #         print(f"{BColors.FAIL}Error deleting {filename}{BColors.ENDC}")
    #         return False

    #     print(f"{BColors.OKGREEN}Deleted {filename}{BColors.ENDC}")
    #     return True


    # def get_videolist(parentdir, inputs = ["any"], filters = []):
    #     print(f"{BColors.OKGREEN}Scanning files in {parentdir} for videos{BColors.ENDC}")
    #     videolist = []

    #     path = Path(parentdir)
    #     if "wmv" in inputs or "any" in inputs or len(inputs) < 1:
    #         videolist += list(path.rglob("*.[wW][mM][vV]"))
    #     if "avi" in inputs or "any" in inputs or len(inputs) < 1:
    #         videolist += list(path.rglob("*.[aA][vV][iI]"))
    #     if "mkv" in inputs or "any" in inputs or len(inputs) < 1:
    #         videolist += list(path.rglob("*.[mM][kK][vV]"))
    #     if "mp4" in inputs or "any" in inputs or len(inputs) < 1:
    #         videolist += list(path.rglob("*.[mM][pP]4"))
    #     if "m4v" in inputs or "any" in inputs or len(inputs) < 1:
    #         videolist += list(path.rglob("*.[mM]4[vV]"))
    #     if "flv" in inputs or "any" in inputs or len(inputs) < 1:
    #         videolist += list(path.rglob("*.[fF][lL][vV]"))
    #     if "mpg" in inputs or "any" in inputs or len(inputs) < 1:
    #         videolist += list(path.rglob("*.[mM][pP][gG]"))
    #     if "vid" in inputs or "any" in inputs or len(inputs) < 1:
    #         videolist += list(path.rglob("*.[vV][iI][dD]"))
        
        
    #     # Remove folders
    #     videolist_tmp = videolist
    #     videolist = [video for video in videolist_tmp if video.is_file()]
        
    #     # Filter the list for specific codecs
    #     videolist_tmp = videolist
    #     print(f"{BColors.OKGREEN}Filtering {len(videolist)} videos for the requested parameters{BColors.ENDC}")
    #     if len([filt for filt in filters if filt not in ["lowres", "hd", "720p", "1080p", "uhd", "fferror"]]) > 0:
    #         videolist = []

    #         if "old" in filters:
    #             videolist += [video for video in videolist_tmp if get_codec(video) not in ["hevc", "av1"]]

    #         if "mpeg4" in filters or "mpeg" in filters:
    #             videolist += [video for video in videolist_tmp if get_codec(video) in ["mpeg4", "msmpeg4v3"]]

    #         if "mpeg" in filters:
    #             videolist += [video for video in videolist_tmp if get_codec(video) in ["mpeg1video"]]

    #         if "wmv3" in filters or "wmv" in filters:
    #             videolist += [video for video in videolist_tmp if get_codec(video) in ["wmv3"]]

    #         if "x264" in filters:
    #             videolist += [video for video in videolist_tmp if get_codec(video) in ["x264"]]
            
    #     if len(filters) > 0 and "lowres" in filters:
    #         videolist_tmp = videolist
    #         videolist = [video for video in videolist_tmp if get_resolution(video)[1] < 1280 or get_resolution(video)[0] <= 480]
    #     elif len(filters) > 0 and "hd" in filters:
    #         videolist_tmp = videolist
    #         videolist = [video for video in videolist_tmp if get_resolution(video)[1] >= 1280 or get_resolution(video)[0] >= 720]
    #     elif len(filters) > 0 and "720p" in filters:
    #         videolist_tmp = videolist
    #         videolist = [video for video in videolist_tmp if get_resolution(video)[1] >= 1280 or get_resolution(video)[0] == 720]
    #     elif len(filters) > 0 and "1080p" in filters:
    #         videolist_tmp = videolist
    #         videolist = [video for video in videolist_tmp if (get_resolution(video)[1] >= 1440 and get_resolution(video)[1] < 3840) or get_resolution(video)[0] == 1080]
    #     elif len(filters) > 0 and "uhd" in filters:
    #         videolist_tmp = videolist
    #         videolist = [video for video in videolist_tmp if get_resolution(video)[1] >= 3840 or get_resolution(video)[0] >= 2160]

    #     if len(filters) > 0 and "fferror" in filters:
    #         videolist_tmp = videolist
    #         videolist = [video for video in videolist_tmp if get_fferror(video)]

    #     print(f"{BColors.OKGREEN}Found {len(videolist)} videos for the requested parameters{BColors.ENDC}")

    #     # remove doubles and return
    #     return list(dict.fromkeys(videolist))

