========
Warnings
========

Before using the delete feature please try a few dry runs to get acquainted with MediaCurator as it can irreparably damage your media library when not used properly.

When using the -del flag here is the expected behavior:

To delete all non-hd videos in a folder:

.. code-block:: bash

    ./curator.py list -del -filters:lowres  -dirs/-files:"/mnt/media/"

To delete all substandard videos in a folder:

.. code-block:: bash

    ./curator.py list -del -filters:subsd  -dirs/-files:"/mnt/media/"

.. image:: ../_static/Screenshot-delete.png
    :width: 600
    :alt: Deleting videos

To delete all videos in a folder with encoding errors:

.. code-block:: bash

    ./curator.py list -del -filters:fferror  -dirs/-files:"/mnt/media/"

To convert (repair) then delete all videos in a folder with encoding errors:

.. code-block:: bash

    ./curator.py convert -del -filters:fferror  -dirs/-files:"/mnt/media/"

To delete all videos in a folder:

.. code-block:: bash

    ./curator.py list -del -filters:lowres  -dirs/-files:"/mnt/media/"

All these commands can have valuable use but are irrecoverable if done unintended.

Again, please try a few dry runs without -del until you are acquainted with MediaCurator.