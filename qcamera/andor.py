"""Andor camera interface"""

from __future__ import print_function
import time
import warnings
import ctypes
import numpy as np
import camera
from camera_errors import AndorError, AndorWarning
from andor_status_codes import *

# TODO: make gain a class member

def _int_ptr(val=0):
    """Utility function to create integer pointers."""
    return ctypes.pointer(ctypes.c_int(val))
    
def _warn(msg):
    """Warn with an AndorWarning."""
    # TODO: fix warning messages (says None now)
    warnings.warn(msg, AndorWarning)

def _chk(status):
    """Checks the error status of an Andor DLL function call. If
    something catastrophic happened, an AndorError exception is
    raised. In non-critical cases, warnings are given.

    Parameters
    ----------
    status : int
        The return code from an Andor DLL function.

    Raises
    ------
    AndorError
        Whenever something very bad happens. Generally, this should
        hopefully only be whenever the user is trying to do something
        stupid.

    """
    if status == ANDOR_STATUS['DRV_ACQUIRING']:
        _warn("Action not completed when data acquisition is in progress!")
    elif status == ANDOR_STATUS['DRV_TEMPERATURE_OFF']:
        #_warn("Temperature control is off.")
        pass
    elif status == ANDOR_STATUS['DRV_TEMPERATURE_NOT_REACHED']:
        _warn("Temperature set point not yet reached.")
    elif status == ANDOR_STATUS['DRV_TEMPERATURE_DRIFT']:
        _warn("Temperature is drifting.")
    elif status == ANDOR_STATUS['DRV_TEMP_NOT_STABILIZED']:
        _warn("Temperature set point reached but not yet stable.")
    elif status == ANDOR_STATUS['DRV_TEMPERATURE_STABILIZED']:
        pass
    elif status != ANDOR_STATUS['DRV_SUCCESS']:
        raise AndorError(
            "Andor returned the status message " + \
            ANDOR_CODES[status])

class AndorCamera(camera.Camera):
    """Class for controlling Andor cameras. This is designed
    specifically with the iXon series cameras, but the Andor API is
    rather generic so should work with most or all of their
    cameras.

    """

    # Valid acquisition modes.
    _acq_modes = {
        "single": 1,
        "accumulate": 2,
        "kinetics": 3,
        "fast kinetics": 4,
        "run till abort": 5}

    # Valid trigger modes.
    # There are more that are not implemented here, some of which are
    # only valid on particular camera models.
    _trigger_modes = {
        "internal": 0,
        "external": 1,
        "external start": 6,
        "software": 10}

    # Setup and shutdown
    # ------------------

    def __init__(self, temperature=-50, bins=None, crop=None, real=True):
        """Initialize the Andor camera.

        Keyword arguments
        -----------------
        temperature : int
            Temperature in Celsius to set the TEC to.
        bins : int or None
            Specifies the number of binned pixels to use.
        crop : tuple or None
            A tuple of the form [x, y, width, height] specifying the
            cropped portion of the sensor to use. If None, use the
            full sensor.
        real : bool
            If False, the camera will be simulated.

        """
        # Check if we are simulating a camera or using a real one
        super(AndorCamera, self).__init__(real=real)
        if not self.real_camera:
            return
        
        # Try to load the Andor DLL
        self.clib = ctypes.windll.LoadLibrary("atmcd32d.dll")

        # Initialize the camera and get the detector size
        # TODO: directory to Initialize?
        _chk(self.clib.Initialize("."))
        xpx, ypx = _int_ptr(), _int_ptr()
        _chk(self.clib.GetDetector(xpx, ypx))
        self.shape = [xpx.contents.value, ypx.contents.value]

        # Configure binning and cropping
        if bins is None:
            bins = self.bins
        if crop is None:
            crop = [1, self.shape[0], 1, self.shape[1]]
        self.set_bins(bins)
        self.set_crop(crop)

        # TODO: Get hardware and software information?

        # Enable temperature control
        T_min, T_max = _int_ptr(), _int_ptr()
        _chk(self.clib.GetTemperatureRange(T_min, T_max))
        self.T_min = T_min.contents.value
        self.T_max = T_max.contents.value
        self.set_cooler_temperature(temperature)
        self.cooler_on()

    def close(self):
        """Turn off temperature regulation and safely shutdown the
        camera.

        The Andor SDK guide indicates that for classic and ICCD
        systems, it is best to wait until the temperature is above -20
        degrees C before shutting down, so this will wait until that
        condition is met.

        """
        self.cooler_off()
        self.close_shutter()
        while True:
            temp = self.get_cooler_temperature()
            if temp > -20:
                break
            else:
                time.sleep(1)
        _chk(self.clib.ShutDown())
        
    # Image acquisition
    # -----------------
        
    def set_acquisition_mode(self, mode):
        """Set the image acquisition mode."""
        if mode not in self._acq_modes:
            raise AndorError(
                "Acquisition mode must be one of " + repr(self._acq_modes))
        self.acq_mode = mode
        if not self.real_camera:
            return
        _chk(self.clib.SetAcquisitionMode(
            ctypes.c_int(self._acq_modes[mode])))
    
    def acquire_image_data(self):
        """Acquire the most recent image data from the camera. This
        will work best in single image acquisition mode.

        """
        # Abort if not in single image acquisition mode.
        if self.acq_mode != "single":
            _warn("Not in single acquisition mode!")
            
        # Wait for acquisition to finish
        self.clib.WaitForAcquisition()
            
        # Get the image
        img_size = self.shape[0]*self.shape[1]/self.bins**2
        c_array = ctypes.c_long*img_size
        c_img = c_array()
        _chk(self.clib.GetMostRecentImage(ctypes.pointer(c_img), ctypes.c_ulong(img_size)))
        img_array = np.frombuffer(c_img, dtype=ctypes.c_long)
        img_array.shape = np.array(self.shape)/self.bins
        return img_array
        
    # Triggering
    # ----------

    def get_trigger_mode(self):
        """Query the current trigger mode."""

    def set_trigger_mode(self, mode):
        """Setup trigger mode.

        Parameters
        ----------
        mode : str
            Specifies the mode to use and must be one of the (non-case
            sensitive) strings found in self._trigger_modes.

        """
        mode = mode.lower()
        if mode not in self._trigger_modes:
            raise AndorError("Invalid trigger mode: " + mode)
        if self.real_camera:
            _chk(self.clib.SetTriggerMode(self._trigger_modes[mode]))
        
    def trigger(self):
        """Send a software trigger to take an image immediately."""
        # TODO: only work if in software trigger mode
        if self.real_camera:
            _chk(self.clib.StartAcquisition())
        
    # Shutter control
    # ---------------

    def open_shutter(self):
        """Open the shutter."""
        super(AndorCamera, self).open_shutter()
        if self.real_camera:
            _chk(self.clib.SetShutter(1, 1, 20, 20))
        
    def close_shutter(self):
        """Close the shutter."""
        super(AndorCamera, self).close_shutter()
        if self.real_camera:
            _chk(self.clib.SetShutter(1, 2, 20, 20))

    # Gain and exposure time
    # ----------------------

    def get_exposure_time(self):
        """Query for the current exposure time."""
        return self.t_ms

    def set_exposure_time(self, t, units='ms'):
        """Set the exposure time."""
        super(AndorCamera, self).set_exposure_time(t, units)
        t_s = self.t_ms*1000
        _chk(self.clib.SetExposureTime(t_s))

    def get_gain(self):
        """Query the current gain settings."""
        if self.real_camera:
            gain = _int_ptr()
            _chk(self.clib.GetEMCCDGain(gain))
            return gain.contents.value
        else:
            return 1

    def set_gain(self, gain, **kwargs):
        """Set the camera gain and mode.

        Parameters
        ----------
        gain : float
            Gain for the camera. The acceptable values depend on the
            mode.

        Keyword arguments
        -----------------
        em_gain : bool
            When True, enable EM gain. The gain parameter is then
            setting the gain value for EM gain rather than
            conventional gain.

        Raises
        ------
        ValueError

        """
        em_gain = kwargs.get('em_gain', False)
        if em_gain:
            _chk(self.clib.SetEMGainMode(0)) # gain is 0-255
            if gain < 0 or gain > 255:
                raise ValueError("gain must be in the range [0, 255].")
            _chk(self.clib.SetEMCCDGain(ctypes.c_int(gain)))
        else:
            # TODO
            pass

    # Cooling
    # -------

    def cooler_on(self):
        """Turn on the TEC."""
        if self.real_camera:
            _chk(self.clib.CoolerON())

    def cooler_off(self):
        """Turn off the TEC."""
        if self.real_camera:
            _chk(self.clib.CoolerOFF())

    def get_cooler_temperature(self):
        """Check the TEC temperature."""
        # TODO: make this work better with simulated cameras
        if not self.real_camera:
            return 20
        temp = _int_ptr()
        _chk(self.clib.GetTemperature(temp))
        return temp.contents.value

    def set_cooler_temperature(self, temp):
        """Set the cooler temperature to temp."""
        # TODO: make this work better with simulated cameras
        if not self.real_camera:
            pass
        if temp > self.T_max or temp < self.T_min:
            raise ValueError(
                "Set point temperature must be between " + \
                repr(self.T_min) + " and " + repr(self.T_max) + ".")
        _chk(self.clib.SetTemperature(temp))

    # ROI, cropping, and binning
    # --------------------------

    def set_roi(self, roi):
        """Define the region of interest."""
        super(AndorCamera, self).set_roi(roi)
        
    def get_crop(self):
        """Get the current CCD crop settings."""
        # TODO

    def set_crop(self, crop):
        """Define the portion of the CCD to actually collect data
        from. Using a reduced sensor area typically allows for faster
        readout.

        """
        super(AndorCamera, self).set_crop(crop)
        _chk(self.clib.SetImage(self.bins, self.bins,
                                self.crop[0], self.crop[1], self.crop[2], self.crop[3]))
        
    def get_bins(self):
        """Query the current binning."""
        # TODO

    def set_bins(self, bins):
        """Set binning to bins x bins."""
        self.bins = bins
        print(self.bins)
        print(self.crop)
        _chk(self.clib.SetImage(self.bins, self.bins,
                                self.crop[0], self.crop[1], self.crop[2], self.crop[3]))
        
if __name__ == "__main__":
    import matplotlib.pyplot as plt
    print("Connecting to camera...")
    with AndorCamera(temperature=10) as cam:
        print("Setting acquisition mode to single.")
        cam.set_acquisition_mode('single')
        print("Setting exposure time to 10 ms")
        cam.set_exposure_time(10)
        print("Opening shutter")
        cam.open_shutter()
        for i in range(2):
            print("Triggering")
            cam.trigger()
            print("Acquiring image")
            img = cam.get_image()
            plt.figure()
            plt.gray()
            plt.imshow(img, interpolation='none')
            time.sleep(.2)
        plt.show()