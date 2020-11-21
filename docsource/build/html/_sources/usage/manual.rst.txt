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

Description
-----------

Options
-------

list

convert

-del:

-in:
    [any,avi,mkv,wmv,mpg,mp4,m4v,flv,vid]
-filters:
    [fferror,old,lowres,hd,720p,1080p,uhd,mpeg,mpeg4,x264,wmv3,wmv]
-out:
    [mkv/mp4,x265/av1]
-print:
    [list,formated,verbose]
-dir:
    ["/mnt/media/",,"/mnt/media2/"]
-files:
    ["/mnt/media/video.avi",,"/mnt/media2/video2.mp4"]

Examples
--------


See Also
--------

Author
------

Fabrice Quenneville






**for multiple files or filenames use double comma separated values ",,"**

default options are:

.. code-block:: bash

    -in:any
    -filters:
    -out:mkv,x265
    -print:list

Examples:

.. code-block:: bash

    ./curator.py list -filters:old -print:formated -dir:/mnt/media/ >> ../medlist.txt
    ./curator.py convert -del -filters:mpeg4 -out:av1,mp4 -dir:"/mnt/media/Movies/"
    ./curator.py convert -del -in:avi,mpg -print:formated,verbose -dir:/mnt/media/



Synopsis



Description


