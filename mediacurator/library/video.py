#!/usr/bin/env python3
'''Its a video!'''

from .bcolors import BColors
import subprocess
import os

class Video():
    '''
        Contains the information and methods of a video file.
    '''

    path = ""
    filename_origin = ""
    filesize_origin = ""
    filename_new = ""
    filename_tmp = ""
    useful = True
    codec= ""
    error = ""
    definition = ""
    width = int()
    height = int()

    def __init__(self, filepath, useful = True):
        '''
        '''

        #Breaking down the full path in its components
        self.path               = str(filepath)[:str(filepath).rindex("/") + 1]
        self.filename_origin    = str(filepath)[str(filepath).rindex("/") + 1:]

        # Marking useful is user manually set it.
        self.useful             = useful

        #Gathering information on the video
        self.filesize_origin    = self.detect_filesize(filepath)
        self.error              = self.detect_fferror(filepath)
        self.codec              = self.detect_codec(filepath)
        self.width, self.height = self.detect_resolution(filepath)
        self.definition         = self.detect_definition(
                                        width = self.width, 
                                        height = self.height )

    def __str__(self):
        '''
            Building and returning formated information about the video file
        '''

        text = f"{self.path + self.filename_origin}\n"

        # If the first character of the definition is not a number (ie UHD and not 720p) upper it
        if self.definition[0] and not self.definition[0].isnumeric():
            text += f"    Definition:     {self.definition.upper()}: ({self.width}x{self.height})\n"
        else:
            text += f"    Definition:     {self.definition}: ({self.width}x{self.height})\n"

        text += f"    Codec:          {self.codec}\n"

        # Return the size in mb or gb if more than 1024 mb
        if self.filesize_origin >= 1024:
            text += f"    size:           {self.filesize_origin / 1024 :.2f} gb"
        else:
            text += f"    size:           {self.filesize_origin} mb"

        if self.error:
            text += f"\n    Errors:         {self.error}"
        
        text += f"\n    Useful:         {self.useful}"

        return text


    __repr__ = __str__

    @staticmethod
    def detect_codec(filepath):
        try:
            args = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", str(filepath)]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            
            # decoding from binary, stripping whitespace, keep only last line
            # in case ffmprobe added error messages over the requested information
            output = output.decode().strip().splitlines()[-1]
        except subprocess.CalledProcessError:
            print(f"{BColors.FAIL}There seams to be an error with {filepath}{BColors.ENDC}")
            return False
        return output


    @staticmethod
    def detect_fferror(filepath):
        try:
            args = ["ffprobe","-v","error","-select_streams","v:0", "-show_entries","stream=width,height","-of","csv=s=x:p=0",str(filepath)]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            output = output.decode().strip().splitlines()
            if len(output) > 1:
                return output[0:-1]
        except subprocess.CalledProcessError:
            return f'{BColors.FAIL}There seams to be a "subprocess.CalledProcessError" error with {filepath}{BColors.ENDC}'
        return False


    @staticmethod
    def detect_resolution(filepath):
        try:
            args = ["ffprobe","-v","error","-select_streams","v:0", "-show_entries","stream=width,height","-of","csv=s=x:p=0",str(filepath)]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            
            # decoding from binary, stripping whitespace, keep only last line
            # in case ffmprobe added error messages over the requested information
            output = output.decode().strip().splitlines()[-1]

            # See if we got convertable data
            output = [int(output.split("x")[0]), int(output.split("x")[1])]
        except subprocess.CalledProcessError:
            print(f"{BColors.FAIL}There seams to be an error with {filepath}{BColors.ENDC}")
            return False
        return output[0], output[1]

    @staticmethod
    def detect_definition(filepath = False, width = False, height = False):
        if filepath:
            width, height = Video.detect_resolution(filepath)
        if not width and not height:
            return False
        
        if width >= 2160 or height >= 2160:
            return "uhd"
        elif width >= 1440 or height >= 1080:
            return "1080p"
        elif width >= 1280 or height >= 720:
            return "720p"
        return "sd"

    @staticmethod
    def detect_filesize(filepath):
        try:
            size = int(os.path.getsize(filepath) / 1024 / 1024)
        except subprocess.CalledProcessError:
            print(f"{BColors.FAIL}There seams to be an error with {filepath}{BColors.ENDC}")
            return False
        return size

    # @staticmethod
    # def convert(oldfilename, newfilename, codec = "x265"):
    #     oldsize = get_size(oldfilename)
    #     print(f"{BColors.OKGREEN}Starting conversion of {oldfilename}{BColors.OKCYAN}({oldsize}mb)({get_print_resolution(oldfilename)}){BColors.OKGREEN} from {BColors.OKCYAN}{get_codec(oldfilename)}{BColors.OKGREEN} to {BColors.OKCYAN}{codec}{BColors.OKGREEN}...{BColors.ENDC}")

    #     # Preparing ffmpeg command and input file
    #     args = ['ffmpeg', '-i', oldfilename]

    #     # conversion options
    #     if codec == "av1":
    #         args += ['-c:v', 'libaom-av1', '-strict', 'experimental']
    #     else:
    #         args += ['-c:v', 'libx265']
    #         args += ['-max_muxing_queue_size', '1000']

    #     # conversion output
    #     args += [newfilename]

    #     #args = ['ffmpeg', '-i', oldfilename, newfilename]
    #     try:
    #         if "-verbose" in sys.argv:
    #             subprocess.call(args)
    #         else:
    #             txt = subprocess.check_output(args, stderr=subprocess.STDOUT)
    #     except subprocess.CalledProcessError as e:
    #         print(f"{BColors.FAIL}Conversion failed {e}{BColors.ENDC}")
    #         return False
    #     else:
    #         newsize = get_size(newfilename)
    #         oldfilename = str(oldfilename)[str(oldfilename).rindex("/") + 1:]
    #         newfilename = str(newfilename)[str(newfilename).rindex("/") + 1:]
    #         print(f"{BColors.OKGREEN}Converted {oldfilename}{BColors.OKCYAN}({oldsize}mb){BColors.OKGREEN} to {newfilename}{BColors.OKCYAN}({newsize}mb){BColors.OKGREEN} successfully{BColors.ENDC}")
    #         return True