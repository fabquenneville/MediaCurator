#!/usr/bin/env python3
'''Its a video!'''

from .bcolors import BColors
from .tools import deletefile
import subprocess
import os
import sys

class Video():
    '''
        Contains the information and methods of a video file.
    '''

    path = ""
    filename_origin = ""
    filesize = ""
    filename_new = ""
    filename_tmp = ""
    useful = True
    codec= ""
    error = ""
    definition = ""
    width = int()
    height = int()

        

    def __init__(self, filepath, useful = True, verbose = False):
        '''
        '''

        #Breaking down the full path in its components
        self.path               = str(filepath)[:str(filepath).rindex("/") + 1]
        self.filename_origin    = str(filepath)[str(filepath).rindex("/") + 1:]

        # Marking useful is user manually set it.
        self.useful             = useful

        #Gathering information on the video
        self.filesize    = self.detect_filesize(filepath)
        self.error              = self.detect_fferror(filepath)
        self.codec              = self.detect_codec(filepath)
        try:
            self.width, self.height = self.detect_resolution(filepath)
            self.definition         = self.detect_definition(
                                            width = self.width, 
                                            height = self.height )
        except:
            self.width, self.height = False, False
            self.definition         = False
        
        if self.error and verbose:
            print(f"{BColors.FAIL}There seams to be an error with \"{filepath}\"{BColors.ENDC}")
            print(f"{BColors.FAIL}    {self.error}{BColors.ENDC}")

    def __str__(self):
        '''
            Building and returning formated information about the video file
        '''
        text = f"{self.codec} - "

        # If the first character of the definition is not a number (ie UHD and not 720p) upper it
        if self.definition[0] and not self.definition[0].isnumeric():
            text += f"{self.definition.upper()}: ({self.width}x{self.height}) - "
        else:
            text += f"{self.definition}: ({self.width}x{self.height}) - "

        # Return the size in mb or gb if more than 1024 mb
        if self.filesize >= 1024:
            text += f"{self.filesize / 1024 :.2f} gb - "
        else:
            text += f"{self.filesize} mb - "
        
        text += f"'{self.path + self.filename_origin}'"


        if self.error:
            text += f"{BColors.FAIL}\nErrors:{BColors.ENDC}"
            for err in self.error.splitlines():
                text += f"{BColors.FAIL}\n    {err}{BColors.ENDC}"
        

        return text


    __repr__ = __str__

    def fprint(self):
        '''
            Building and returning formated information about the video file
        '''

        text = f"{self.path + self.filename_origin}\n"
        #text += f"    Useful:         {self.useful}\n"

        # If the first character of the definition is not a number (ie UHD and not 720p) upper it
        if self.definition[0] and not self.definition[0].isnumeric():
            text += f"    Definition:     {self.definition.upper()}: ({self.width}x{self.height})\n"
        else:
            text += f"    Definition:     {self.definition}: ({self.width}x{self.height})\n"

        text += f"    Codec:          {self.codec}\n"

        # Return the size in mb or gb if more than 1024 mb
        if self.filesize >= 1024:
            text += f"    size:           {self.filesize / 1024 :.2f} gb"
        else:
            text += f"    size:           {self.filesize} mb"

        if self.error:
            text += f"{BColors.FAIL}\n    Errors:{BColors.ENDC}"
            for err in self.error.splitlines():
                text += f"{BColors.FAIL}\n        {err}{BColors.ENDC}"
        

        return text


    def convert(self, vcodec = "x265", acodec = False, extension = "mkv", verbose = False):
        '''
            Convert to original file to the requested format / codec
        '''


        # Setting new filename
        if "mp4" in extension:
            newfilename = self.filename_origin[:-4] + ".mp4"
            if self.filename_origin == newfilename:
                newfilename = self.filename_origin[:-4] + "[HEVC]" + ".mp4"
        else:
            newfilename = self.filename_origin[:-4] + ".mkv"
            if self.filename_origin == newfilename:
                newfilename = self.filename_origin[:-4] + "[HEVC]" + ".mkv"
        self.filename_tmp = newfilename



        # Settting ffmpeg
        args = ['ffmpeg', '-i', self.path + self.filename_origin]

        # conversion options
        if vcodec == "av1":
            args += ['-c:v', 'libaom-av1', '-strict', 'experimental']
        elif vcodec == "x265" or vcodec == "hevc":
            args += ['-c:v', 'libx265']
            args += ['-max_muxing_queue_size', '1000']
        # conversion output
        args += [self.path + self.filename_tmp]


        
        try:
            if verbose:
                subprocess.call(args)
            else:
                txt = subprocess.check_output(args, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            deletefile(self.path + self.filename_tmp)
            self.filename_tmp = ""
            print(f"{BColors.FAIL}Conversion failed {e}{BColors.ENDC}")
            return False
        except KeyboardInterrupt:
            print(f"{BColors.WARNING}Conversion cancelled, cleaning up...{BColors.ENDC}")
            deletefile(self.path + self.filename_tmp)
            self.filename_tmp = ""
            exit()
        else:
            subprocess.call(['chmod', '777', self.path + self.filename_tmp])
            self.filename_new = self.filename_tmp
            self.filename_tmp = ""
            return True







    @staticmethod
    def detect_codec(filepath):
        try:
            args = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", str(filepath)]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            
            # decoding from binary, stripping whitespace, keep only last line
            # in case ffmprobe added error messages over the requested information
            output = output.decode().strip().splitlines()[-1]
        except (subprocess.CalledProcessError, IndexError):
            return False
        return output


    @staticmethod
    def detect_fferror(filepath):
        try:
            args = ["ffprobe","-v","error",str(filepath)]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            output = output.decode().strip()
            if len(output) > 0:
                return output
        except (subprocess.CalledProcessError, IndexError):
            return f'{BColors.FAIL}There seams to be a "subprocess.CalledProcessError" error with \"{filepath}\"{BColors.ENDC}'
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
        except (subprocess.CalledProcessError, IndexError):
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
            return False
        return size
