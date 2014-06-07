"""Threading for camera live feeds

TODO: Figure out a way to do this with generic Python threading
      instead of relying on Qt threading so that this can be used in
      non-GUI environments.

"""

import time
import logging
import numpy as np
from PyQt4 import QtCore
from camera import Camera

class CameraThread(QtCore.QThread):
    """Thread class for producing live feed images from a camera.

    Attributes
    ----------
    running : bool
        True when the thread is running.
    abort : bool
        Set to True when stopping of the thread is requested.
    logger : Logger
        A Logger object for logging any important output from the
        thread.

    """

    running = False
    abort = False
    image_acquired = QtCore.pyqtSignal(np.ndarray)
    
    def __init__(self, cam, **kwargs):
        """Initialize the camera thread.

        Parameters
        ----------
        camera : Camera
            A camera instance for acquiring images.

        Keyword arguments
        -----------------
        logger : str
            Logger to use.

        """
        # Get and check kwargs.
        logger = kwargs.get('logger', 'Camera')
        assert isinstance(cam, Camera)
        assert isinstance(logger, str)

        # Initialize thread.
        self.cam = cam
        self.logger = logging.getLogger(logger)
        super(CameraThread, self).__init__()

    def stop(self):
        """Stop the thread."""
        self.abort = True
        while self.running:
            time.sleep(0.01)

    def run(self):
        """Run the thread until receiving a stop request. It is up to
        the user to properly setup acquisition and triggering modes
        prior to running the thread!

        """
        while not self.abort:
            try:
                image = self.cam.get_image()
                self.image_acquired.emit(image)
            except:
                # TODO: DTRT, have exception in case camera is busy
                #       changing settings or whatever
                import sys, traceback as tb
                e = sys.exc_info()
                print(e[1])
                tb.print_last()
                time.sleep(0.01)

