"""Camera threads for continuous acquisition."""

from __future__ import print_function
import sys
import time
import traceback
from Queue import Queue
import numpy as np
from PyQt4 import QtCore

class CameraThread(QtCore.QThread):
    """Thread class for producing live feed images from a camera."""

    abort = False
    paused = True
    mode = 'software'
    queue = Queue()
    image_signal = QtCore.pyqtSignal(np.ndarray)
    
    def __init__(self, camera):
        super(CameraThread, self).__init__()
        self.cam = camera

    def stop(self):
        """Stop the thread."""
        self.abort = True

    def start_live_feed(self):
        """Continuously gather and emit images, i.e., run in
        preview/software triggering mode.

        """
        self.mode = 'software'
        self.cam.set_trigger_mode(self.mode)
        self.paused = False

    def start_hardware_triggered_acquisition(self):
        """Start gathering images in hardware triggered mode, i.e.,
        run in the mode for actual data collection.

        """
        self.mode = 'hardware'
        self.cam.set_trigger_mode(self.mode)
        self.paused = False

    def run(self):
        """Run the thread until receiving a stop request."""
        self.paused = True
        while not self.abort:
            # Check from the main thread if we need to pause
            # (e.g., if a hardware update is happening).
            if not self.queue.empty():
                msg = self.queue.get()
                if msg == 'pause':
                    self.paused = True
                    self.cam._stop()
                elif msg == 'unpause':
                    self.paused = False
                    self.cam._start()

            # Acquire data.
            if not self.paused:
                try:
                    img_data = self.cam.get_image()
                    self.image_signal.emit(img_data)
                except:
                    e = sys.exc_info()
                    print(e)
                    traceback.format_exc()
                    time.sleep(0.01)
            else:
                time.sleep(0.01)