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

```bash
./converter.py list -any -old -dir /mnt/media/TV\ Shows/ >> ../medlist.txt
./converter.py convert -del -any -mpeg4 -dir "/mnt/media/Movies/"
./converter.py convert -del -all_avi -verbose -dir "/mnt/media/Movies/"
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)