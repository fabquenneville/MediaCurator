=========
Use cases
=========

The main reasons to use MediaCurator would be the following:

* :ref:`list_cmd` on a video library such as:
    - How many videos of the lot are in HD vs standard or substandard definitions
    - What videos are in older codecs
    - Are there videos in the library with encoding or corruption errors
* :ref:`purge` selected videos in a media library
* :ref:`fferror` on selected videos in a media library
* :ref:`convert` videos from an old codec to `High Efficiency Video Coding <https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding>`_

.. _list_cmd:

Print information
-----------------

List all videos with old codec in formated format

.. code-block:: bash

    ./curator.py list -filters:old -dirs:/mnt/media/

List all videos with substandard definitions with a formated output

.. code-block:: bash

    ./curator.py list -filters:subsd -print:formated -dirs:/mnt/media/


.. _purge:

Purge
-----

Please see :doc:`warnings`

List and delete all videos using the `Windows Media Video <https://en.wikipedia.org/wiki/Windows_Media_Video>`_ codecs

.. code-block:: bash

    ./curator.py list -del -filters:wmv -dirs:/mnt/media/

List and delete all videos using an `Audio Video Interleave <https://en.wikipedia.org/wiki/Audio_Video_Interleave>`_

.. code-block:: bash

    ./curator.py list -del -in:avi -dirs:/mnt/media/

List and delete any videos with encoding errors

.. code-block:: bash

    ./curator.py list -del -filters:fferror -dirs:/mnt/media/



.. _fferror:

Batch repair encoding errors
----------------------------

List all videos with encoding errors

.. code-block:: bash

    ./curator.py list -filters:fferror -dirs:/mnt/media/

List and delete any videos with encoding errors

.. code-block:: bash

    ./curator.py list -del -filters:fferror -dirs:/mnt/media/
    
Convert all videos with encoding errors to `High Efficiency Video Coding <https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding>`_ and the delete the originals

.. code-block:: bash

    ./curator.py convert -del -filters:fferror -dirs:"/mnt/media/Movies/"


.. _convert:

Batch re-encode
---------------

Convert all videos with old codecs to `High Efficiency Video Coding <https://en.wikipedia.org/wiki/High_Efficiency_Video_Coding>`_ to save space and delete the originals

.. code-block:: bash

    ./curator.py convert -del -filters:old -dirs:"/mnt/media/Movies/"
    
Convert all videos with the codec mpeg4 to an mkv container using the av1 video codec

.. code-block:: bash

    ./curator.py convert -filters:mpeg4 -out:av1,mkv -dirs:"/mnt/media/Movies/"
    
Convert any video with avi or mpg extensions, print formated text including ffmpeg's output and then delete the originals

.. code-block:: bash

    ./curator.py convert -del -in:avi,mpg -print:formated,verbose -dirs:/mnt/media/