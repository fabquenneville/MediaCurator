#!/usr/bin/env python3
'''Its a video!'''

from .tools import deletefile, findfreename
import subprocess
import os
import sys
import re


import colorama
colorama.init()

class Video():
    '''Contains the information and methods of a video file.'''

    '''
        path = str()
        filename_origin = str()
        filesize = int()
        filename_new = str()
        filename_tmp = str()
        useful = bool()
        codec= str()
        error = str()
        definition = str()
        width = int()
        height = int()
    '''
        

    def __init__(self, filepath, useful = True, verbose = False):
        ''' creates and analyse a video file '''
        
        #Breaking down the full path in its components
        if os.name == 'nt':
            self.path               = str(filepath)[:str(filepath).rindex("\\") + 1]
            self.filename_origin    = str(filepath)[str(filepath).rindex("\\") + 1:]
        else:
            self.path               = str(filepath)[:str(filepath).rindex("/") + 1]
            self.filename_origin    = str(filepath)[str(filepath).rindex("/") + 1:]

        if not os.path.exists(filepath):
            self.error              = f"FileNotFoundError: [Errno 2] No such file or directory: '{filepath}'"
            self.useful             = useful

        else:
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
            print(f"{colorama.Fore.RED}There seams to be an error with \"{filepath}\"{colorama.Fore.RESET}")
            print(f"{colorama.Fore.RED}    {self.error}{colorama.Fore.RESET}")

    def __str__(self):
        '''Returns a short formated string about the video'''

        if type(self.error) is str and "FileNotFoundError" in self.error:
            return self.error
        
        text = f"{self.codec} - "

        # If the first character of the definition is not a number (ie UHD and not 720p) upper it
        if self.definition and self.definition[0] and not self.definition[0].isnumeric():
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
            text += f"{colorama.Fore.RED}\nErrors:{colorama.Fore.RESET}"
            for err in self.error.splitlines():
                text += f"{colorama.Fore.RED}\n    {err}{colorama.Fore.RESET}"
        

        return text


    __repr__ = __str__

    def fprint(self):
        '''Returns a long formated string about the video '''


        if type(self.error) is str and "FileNotFoundError" in self.error:
            return self.error
        
        text = f"{self.path + self.filename_origin}\n"
        #text += f"    Useful:         {self.useful}\n"

        # If the first character of the definition is not a number (ie UHD and not 720p) upper it
        if self.definition and self.definition[0] and not self.definition[0].isnumeric():
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
            text += f"{colorama.Fore.RED}\n    Errors:{colorama.Fore.RESET}"
            for err in self.error.splitlines():
                text += f"{colorama.Fore.RED}\n        {err}{colorama.Fore.RESET}"
        

        return text


    def convert(self, vcodec = "x265", acodec = False, extension = "mkv", verbose = False):
        '''
            Convert to original file to the requested format / codec
            verbose will print ffmpeg's output
        '''

        # Setting new filename
        if "mp4" in extension:
            newfilename = self.filename_origin[:-4] + ".mp4"
            if os.path.exists(self.path + newfilename):
                newfilename = findfreename(self.path + newfilename)
                if os.name == 'nt':
                    newfilename = str(newfilename)[str(newfilename).rindex("\\") + 1:]
                else:
                    newfilename = str(newfilename)[str(newfilename).rindex("/") + 1:]
        else:
            newfilename = self.filename_origin[:-4] + ".mkv"
            if os.path.exists(self.path + newfilename):
                newfilename = findfreename(self.path + newfilename)
                if os.name == 'nt':
                    newfilename = str(newfilename)[str(newfilename).rindex("\\") + 1:]
                else:
                    newfilename = str(newfilename)[str(newfilename).rindex("/") + 1:]

        self.filename_tmp =  newfilename

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
            print(f"{colorama.Fore.RED}Conversion failed {e}{colorama.Fore.RESET}")
            return False
        except KeyboardInterrupt:
            print(f"{colorama.Fore.YELLOW}Conversion cancelled, cleaning up...{colorama.Fore.RESET}")
            deletefile(self.path + self.filename_tmp)
            self.filename_tmp = ""
            exit()
        else:
            try:
                os.chmod(f"{self.path}{self.filename_tmp}", 0o777)
            except PermissionError:
                print(f"{colorama.Fore.RED}PermissionError on: '{self.path}{self.filename_tmp}'{colorama.Fore.RESET}")
            self.filename_new = self.filename_tmp
            self.filename_tmp = ""
            return True

    @staticmethod
    def detect_fferror(filepath):
        '''Returns a string with the detected errors'''
        try:
            args = ["ffprobe","-v","error",str(filepath)]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            output = output.decode().strip()
            if len(output) > 0:
                return output
        except (subprocess.CalledProcessError, IndexError):
            return f'{colorama.Fore.RED}There seams to be a "subprocess.CalledProcessError" error with \"{filepath}\"{colorama.Fore.RESET}'
        return False


    @staticmethod
    def detect_codec(filepath):
        '''Returns a string with the detected codec'''
        try:
            args = ["ffprobe", "-v", "quiet", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", str(filepath)]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            
            # decoding from binary, stripping whitespace, keep only last line
            # in case ffmprobe added error messages over the requested information
            output = output.decode().strip()
        except (subprocess.CalledProcessError, IndexError):
            return False
        return output


    @staticmethod
    def detect_resolution(filepath):
        '''Returns a list with the detected width(0) and height(1)'''
        try:
            args = ["ffprobe","-v","quiet","-select_streams","v:0", "-show_entries","stream=width,height","-of","csv=s=x:p=0",str(filepath)]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            
            # decoding from binary, stripping whitespace, keep only last line
            # in case ffmprobe added error messages over the requested information
            output = output.decode().strip()

            # See if we got convertable data
            output = [int(output.split("x")[0]), int(output.split("x")[1])]
        except (subprocess.CalledProcessError, IndexError):
            return False
        return output[0], output[1]

    @staticmethod
    def detect_definition(filepath = False, width = False, height = False):
        '''Returns a string with the detected definition corrected for dead space'''
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
        elif height >= 480:
            return "sd"
        return "subsd"

    @staticmethod
    def detect_filesize(filepath):
        '''Returns an integer with size in mb'''
        try:
            size = int(os.path.getsize(filepath) / 1024 / 1024)
        except subprocess.CalledProcessError:
            return False
        return size
