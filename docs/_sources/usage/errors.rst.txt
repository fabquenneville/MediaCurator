
======
Errors
======

FFmpeg can detect quite a few errors in the encoding of your source video's encoding. It can also be used to repair errors.

Repairable encoding errors
--------------------------

Here are some example errors that mediacurator will print and can possibly repair by re-encoding:

* "Referenced QT chapter track not found"
* "Error, header damaged or not MPEG-4 header"
* "Header missing"
* "SEI type"
* "no frame!"
* "Error while decoding MPEG audio frame."
* "big_values too big"
* ...

FFmpeg issues
-------------

While using FFmpeg depending on your version you may also face other errors like segfaults. MediaCurator will also print information when that occurs and move on to the next video after cleaning up after failure.

If that happens there are a few steps you can take:


* `Update FFmpeg <https://ffmpeg.org/download.html>`_ to its latest version as it is a very active project and most distributions serve old versions in their repositories
* Run MediaCurator with the verbose print option wich will print the raw FFmpeg output
* Try again: In my experience some errors don't necessarly recur...

Other bugs
----------

If you face other bugs, issues or want to suggest features feel free to open a bug report on `GitHub <https://github.com/fabquenneville/MediaCurator/issues>`_