========
Warnings
========

Before using the delete feature please run a few dry runs to get acquainted with MediaCurator as you it can irrirreparably damage your media library when not used properly.

When using the -del flag here is the expected behavior:

To delete all non-hd videos in a folder:

.. code-block:: bash

    ./curator.py list -del -filters:lowres  -dir/-files:"/mnt/media/"

To delete all videos in a folder with encoding errors:

.. code-block:: bash

    ./curator.py list -del -filters:fferror  -dir/-files:"/mnt/media/"

To convert (repair) then delete all videos in a folder with encoding errors:

.. code-block:: bash

    ./curator.py convert -del -filters:fferror  -dir/-files:"/mnt/media/"

To delete all videos in a folder:

.. code-block:: bash

    ./curator.py list -del -filters:lowres  -dir/-files:"/mnt/media/"

All these commands can have valuable use but are irrecoverable if done unintended.

Again, please run a few dry runs until you are acquainted with MediaCurator.