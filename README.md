# MediaCurator

MediaCurator is a Python command line tool to manage a media database. 
* List all the video's and their codecs with or without filters
* Batch recode videos to more modern codecs (x265 / AV1) based on filters: extentions, codecs ...

## Installation

This package will only work on Linux and requires FFMPEG installed. For now it will be distributed on [GitHub](https://github.com/fabquenneville/MediaCurator.git)

Installation:
```bash
git clone https://github.com/fabquenneville/MediaCurator.git
cd MediaCurator
pip install -r requirements.txt 

```

## Usage
./curator.py [list,convert] [-del] [-verbose] [-in:any,avi,mkv,wmv,mpg,mp4,m4v,flv,vid] [-filters:old,lowres,mpeg,mpeg4,x264,wmv3,wmv] [-out:mkv/mp4,x265/av1] [-dir/-file:"/mnt/media/",,"/mnt/media2/"]

> for multiple files or filenames use double comma separated values ",,"

default options are:
-in:any
-filters:
-out:mkv,x265

Examples:
```bash
./curator.py list -in:any -filters:old -dir:/mnt/media/ >> ../medlist.txt
./curator.py convert -del -in:any -filters:mpeg4 -out:x265,mkv -dir:"/mnt/media/Movies/"
./curator.py convert -del -verbose -in:avi,mpg -dir:/mnt/media/
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)