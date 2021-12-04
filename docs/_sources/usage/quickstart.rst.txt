==========
Quickstart
==========

.. code-block:: bash

    mediacurator [list,convert] [-del]
        [-in:any,avi,mkv,wmv,mpg,mp4,m4v,flv,vid,divx,ogm]
        [-filters:fferror,old,lowres,hd,720p,1080p,uhd,mpeg,mpeg4,x264,wmv3,wmv]
        [-out:mkv/mp4,x265/av1]
        [-print:list,formated,verbose]
        [-dirs/-files:"/mnt/media/",,"/mnt/media2/"]

**for multiple files or filenames use double comma separated values ",,"**

default options are:

.. code-block:: bash

    -in:any
    -filters:
    -out:mkv,x265
    -print:list

Examples:

.. code-block:: bash

    # List all videos with old codec in formated format
    mediacurator list -filters:old -print:formated -dirs:/mnt/media/ >> ../medlist.txt
    # Convert all videos with the codec mpeg4 in a mp4 using the av1 video codec and the delete the originals
    mediacurator convert -del -filters:mpeg4 -out:av1,mp4 -dirs:"/mnt/media/Movies/"
    # Convert any video with avi or mpg extensions, print formated text including ffmpeg's output and then delete the originals
    mediacurator convert -del -in:avi,mpg -print:formated,verbose -dirs:/mnt/media/

More examples in :doc:`use_cases`