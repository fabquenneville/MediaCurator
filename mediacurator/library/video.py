#!/usr/bin/env python3
'''This module defines the Video class, which contains information and methods for video files.'''

from .tools import deletefile, findfreename
import subprocess
import os

# Import colorama for colored output
import colorama
colorama.init()

# Define color codes for colored output
cyellow = colorama.Fore.YELLOW
cred = colorama.Fore.RED
creset = colorama.Fore.RESET

class Video():
    '''Contains the information and methods of a video file.'''        

    def __init__(self, filepath, operate=True, verbose=False):
        '''Initializes a Video instance with provided parameters.

        Args:
            filepath (str): The full filepath of the video.
            operate (bool): A flag indicating if the video is to be operated on.
            verbose (bool): A flag indicating whether to enable verbose output.
        '''

        # Initialize attributes
        self.path = None
        self.filename_origin = None
        self.filesize = None
        self.filename_new = None
        self.filename_tmp = None
        self.operate = None
        self.codec = None
        self.error = None
        self.definition = None
        self.width = None
        self.height = None
        
        # Break down the full path into its components
        if os.name == 'nt':
            self.path = str(filepath)[:str(filepath).rindex("\\") + 1]
            self.filename_origin = str(filepath)[str(filepath).rindex("\\") + 1:]
        else:
            self.path = str(filepath)[:str(filepath).rindex("/") + 1]
            self.filename_origin = str(filepath)[str(filepath).rindex("/") + 1:]

        if not os.path.exists(filepath):
            self.error = f"FileNotFoundError: [Errno 2] No such file or directory: '{filepath}'"
            self.operate = operate
        else:
            # Mark the video for operation if specified manually by the user
            self.operate = operate

            # Gather information on the video
            self.filesize = self.detect_filesize(filepath)
            self.error = self.detect_fferror(filepath)
            self.codec = self.detect_codec(filepath)
            try:
                self.width, self.height = self.detect_resolution(filepath)
                self.definition = self.detect_definition(
                    width=self.width, 
                    height=self.height
                )
            except:
                self.width, self.height = False, False
                self.definition = False
        
        if self.error and verbose:
            print(f"{cred}There seems to be an error with \"{filepath}\"{creset}")
            print(f"{cred}    {self.error}{creset}")

    def __str__(self):
        '''Returns a short formatted string about the video.

        Returns:
            str: A short formatted string about the video.
        '''

        if type(self.error) is str and "FileNotFoundError" in self.error:
            return self.error
        
        text = f"{self.codec} - "

        # If the first character of the definition is not a number (e.g., UHD and not 720p), upper it
        if self.definition and self.definition[0] and not self.definition[0].isnumeric():
            text += f"{self.definition.upper()}: ({self.width}x{self.height}) - "
        else:
            text += f"{self.definition}: ({self.width}x{self.height}) - "

        # Return the size in MB or GB if more than 1024 MB
        if self.filesize >= 1024:
            text += f"{self.filesize / 1024 :.2f} GB - "
        else:
            text += f"{self.filesize} MB - "
        
        text += f"'{self.path + self.filename_origin}'"

        if self.error:
            text += f"{cred}\nErrors:{creset}"
            for err in self.error.splitlines():
                text += f"{cred}\n    {err}{creset}"

        return text

    __repr__ = __str__

    def fprint(self):
        '''Returns a long formatted string about the video.

        Returns:
            str: A long formatted string about the video.
        '''

        if type(self.error) is str and "FileNotFoundError" in self.error:
            return self.error
        
        text = f"{self.path + self.filename_origin}\n"

        if self.definition and self.definition[0] and not self.definition[0].isnumeric():
            text += f"    Definition:     {self.definition.upper()}: ({self.width}x{self.height})\n"
        else:
            text += f"    Definition:     {self.definition}: ({self.width}x{self.height})\n"

        text += f"    Codec:          {self.codec}\n"

        # Return the size in MB or GB if more than 1024 MB
        if self.filesize >= 1024:
            text += f"    Size:           {self.filesize / 1024 :.2f} GB"
        else:
            text += f"    Size:           {self.filesize} MB"

        if self.error:
            text += f"{cred}\n    Errors:{creset}"
            for err in self.error.splitlines():
                text += f"{cred}\n        {err}{creset}"

        return text

    def convert(self, vcodec="x265", acodec=False, extension="mkv", verbose=False):
        '''
        Converts the original file to the requested format / codec.

        Args:
            vcodec (str): The new video codec, supports av1 or x265.
            acodec (bool): Currently not enabled, will be for audio codecs.
            extension (str): The new video container format and file extension.
            verbose (bool): A flag enabling verbosity.

        Returns:
            bool: True if operation successful, False otherwise.
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

        self.filename_tmp = newfilename

        # Setting ffmpeg
        args = ['ffmpeg', '-i', self.path + self.filename_origin]

        # Conversion options
        if vcodec == "av1":
            args += ['-c:v', 'libaom-av1', '-strict', 'experimental']
        elif vcodec == "x265" or vcodec == "hevc":
            args += ['-c:v', 'libx265']
            args += ['-max_muxing_queue_size', '1000']
        # Conversion output
        args += [self.path + self.filename_tmp]
        
        try:
            if verbose:
                subprocess.call(args)
            else:
                txt = subprocess.check_output(args, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            deletefile(self.path + self.filename_tmp)
            self.filename_tmp = ""
            print(f"{cred}Conversion failed {e}{creset}")
            return False
        except KeyboardInterrupt:
            print(f"{cyellow}Conversion cancelled, cleaning up...{creset}")
            deletefile(self.path + self.filename_tmp)
            self.filename_tmp = ""
            exit()
        else:
            try:
                os.chmod(f"{self.path}{self.filename_tmp}", 0o777)
            except PermissionError:
                print(f"{cred}PermissionError on: '{self.path}{self.filename_tmp}'{creset}")
            self.filename_new = self.filename_tmp
            self.filename_tmp = ""
            return True

    @staticmethod
    def detect_fferror(filepath):
        '''Returns a string with the detected errors.

        Args:
            filepath (str): The full filepath of the video.

        Returns:
            str: The errors that have been found/happened.
            False: The lack of errors.
        '''
        try:
            args = ["ffprobe", "-v", "error", str(filepath)]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            output = output.decode().strip()
            if len(output) > 0:
                return output
        except (subprocess.CalledProcessError, IndexError):
            return f'{cred}There seems to be a "subprocess.CalledProcessError" error with \"{filepath}\"{creset}'
        return False

    @staticmethod
    def detect_codec(filepath):
        '''Returns a string with the detected codec.

        Args:
            filepath (str): The full filepath of the video.

        Returns:
            str: The codec that has been detected.
            False: An error in the codec fetching process.
        '''
        output = False
        try:
            args = ["ffprobe", "-v", "quiet", "-select_streams", "v:0", "-show_entries", "stream=codec_name", "-of", "default=noprint_wrappers=1:nokey=1", str(filepath)]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            # Decoding from binary, stripping whitespace, keep only last line
            # in case ffprobe added error messages over the requested information
            output = output.decode().strip()
        except (subprocess.CalledProcessError, IndexError):
            return False
        return output

    @staticmethod
    def detect_resolution(filepath):
        '''Returns a list with the detected width(0) and height(1).

        Args:
            filepath (str): The full filepath of the video.

        Returns:
            List: The detected width(0) and height(1).
            False: An error in the resolution fetching process.
        '''
        try:
            args = ["ffprobe", "-v", "quiet", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=s=x:p=0", str(filepath)]
            output = subprocess.check_output(args, stderr=subprocess.STDOUT)
            # Decoding from binary, stripping whitespace, keep only last line
            # in case ffprobe added error messages over the requested information
            output = output.decode().strip()
            # See if we got convertible data
            output = [int(output.split("x")[0]), int(output.split("x")[1])]
        except (subprocess.CalledProcessError, IndexError):
            return False
        return output[0], output[1]

    @staticmethod
    def detect_definition(filepath=False, width=False, height=False):
        '''Returns a string with the detected definition corrected for dead space.

        Args:
            filepath (str): A string containing the full filepath.
            width (int): The width of the video.
            height (int): The height of the video.

        Returns:
            str: The classified definition in width(0) and height(1).
            False: An error in the process.
        '''
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
        '''Returns an integer with size in MB.

        Args:
            filepath (str): A string containing the full filepath.

        Returns:
            int: The filesize in MB.
            False: An error in the process.
        '''
        try:
            size = int(os.path.getsize(filepath) / 1024 / 1024)
        except subprocess.CalledProcessError:
            return False
        return size
