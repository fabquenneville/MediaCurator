======
Manual
======

Name
----

MediaCurator

Synopsis
--------

.. code-block:: bash

    ./curator.py [list,convert] [-del]
        [-in:any,avi,mkv,wmv,mpg,mp4,m4v,flv,vid]
        [-filters:fferror,old,lowres,hd,720p,1080p,uhd,mpeg,mpeg4,x264,wmv3,wmv]
        [-out:mkv/mp4,x265/av1]
        [-print:list,formated,verbose]
        [-dir/-files:"/mnt/media/",,"/mnt/media2/"]


**for multiple files or filenames use double comma separated values ",,"**

default options are:

.. code-block:: bash

    -in:any
    -filters:
    -out:mkv,x265
    -print:list

Description
-----------

MediaCurator is a Python command line tool to manage a media database.

* List all the video's and their information with or without filters
* Batch find and repair/convert videos with encoding errors
* Batch recode videos to more modern codecs (x265 / AV1) based on filters: extentions, codecs, resolutions ...

Options
-------

list
====
Search and list videos filtered by the parameters passed by the user.

convert
=======
Search and convert all videos filtered by the parameters passed by the user.

-del:
=====
Delete all original videos once selected operations have been done succefully.

See :doc:`warnings`

-in:
====
[**any**,avi,mkv,wmv,mpg,mp4,m4v,flv,vid]

Search all videos of the selected container **extensions** in the directories. By default it will include any file format.

-filters:
=========
[fferror,old,lowres,hd,720p,1080p,uhd,mpeg,mpeg4,x264,wmv3,wmv]

Filter the selected videos for parameters:

* fferror: Select all videos with encoding errors (See :doc:`errors`)
* old: Select all videos using old codecs (Everything except hevc or av1)
* hd: 720p, 1080p, uhd
* lowres: Everything not hd
* uhd: if width >= 2160 or height >= 2160
* 1080p: if less than uhd and width >= 1440 or height >= 1080
* 720p: if less than 1080p and width >= 1280 or height >= 720:
* sd: if less than 720p and if height >= 480
* subsd: Substandard definitions: Everything under 480p
* mpeg,mpeg4,x264,wmv3,wmv: Filter for videos encoded in the requested video codec

-out:
=====
[**mkv**/mp4,x265/av1]

Select the outputs for the video conversions

* mkv: (**Default**) Package the resulting video in a `Matroska <https://en.wikipedia.org/wiki/Matroska>`_ container.
* mp4: Package the resulting video in a  container.
* x265/hevc: (**Default**) Encode the video using the `x265 <https://en.wikipedia.org/wiki/X265>`_ compression format.
* av1: Encode the video using the `AOMedia Video 1 <https://en.wikipedia.org/wiki/AV1>`_ compression format. This will be used as default once the developpers at FFmpeg move it out of `experimental <https://trac.ffmpeg.org/wiki/Encode/AV1>`_ .

-print:
=======
[**list**,formated,verbose]

* list: (**Default**) Print the information about the videos on a single line

.. image:: ../_static/Screenshot-print_list-single.png
    :width: 600
    :alt: Deleting videos


* formated: Print the information 

.. image:: ../_static/Screenshot-print_formated-single.png
    :width: 400
    :alt: Deleting videos

-dir:
=====
["/mnt/media/",,"/mnt/media2/"]

The directories to scan as a **double comma** separated values list.


-files:
=======
["/mnt/media/video.avi",,"/mnt/media2/video2.mp4"]

Specific videos to include as a **double comma** separated values list.

Examples
--------

.. code-block:: bash

    # List all videos with old codec in formated format
    ./curator.py list -filters:old -print:formated -dir:/mnt/media/ >> ../medlist.txt
    # Convert all videos with the codec mpeg4 in a mp4 using the av1 video codec and the delete the originals
    ./curator.py convert -del -filters:mpeg4 -out:av1,mp4 -dir:"/mnt/media/Movies/"
    # Convert any video with avi or mpg extensions, print formated text including ffmpeg's output and then delete the originals
    ./curator.py convert -del -in:avi,mpg -print:formated,verbose -dir:/mnt/media/

More examples in :doc:`use_cases`

See Also
--------

`FFmpeg <https://ffmpeg.org/>`_

Author
------

Fabrice Quenneville
