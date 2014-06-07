"""Sensicam interface

Much of this was adapted from the older sensicam module written
primarily by Magnus and Gregers.

"""

from __future__ import print_function
import logging
import ctypes
import numpy as np
import camera
from camera_errors import SensicamError
from sensicam_status_codes import *

class CAMTYPE(ctypes.Structure):
    _pack_ = 0
    _fields_ = [("gain", ctypes.c_bool*2),
                ("CCDtype", ctypes.c_bool*2),
                ("Cameratype", ctypes.c_bool*2),
                ("sensicam", ctypes.c_bool*3),
                ("CCDcolor", ctypes.c_bool),
                ("Shutter", ctypes.c_bool*2),
                ("temp_reg", ctypes.c_bool*1),
                ("reserved", ctypes.c_bool*5)]

class MODE(ctypes.Structure):
    _pack_ = 0
    _fields_ = [("mode", ctypes.c_int8),
                ("submode", ctypes.c_int8)]

class Sensicam(camera.Camera):
    """Class for controlling PCO Sensicam cameras."""

    # COC gain modes. See p. 24 of the API documentation.
    _coc_gain_modes = {
        "normal": 0,
        "extended": 1}

    # COC submodes. See p. 24 of the API documentation.
    # This sets specifics for exposure modes. For example, 'single'
    # means one trigger yields one exposure and 'double' means one
    # trigger yields two exposures.
    _coc_submodes = {
        "single": 0, # single trigger mode (DPSINGLE)
        "multi": 1,  # multi trigger mode (DPMULTI)
        "double": 2  # double trigger mode (DPDOUBLE)
    }

    # Valid trigger modes.
    _trigger_modes = {
        "software": 0,
        "rising": 1,
        "falling": 2
    }

    def _chk(self, code):
        """Check the return code of a command. The error messages are
        complicated 32 bit strings which are described in detail in
        the SDK manual. In short, to quote the manual:

        * Bits 0-11 are used to indicate the error number.
        * Bits 12-15 shows the layer of the error source.
        * Bits 16-23 reflect the error source.
        * Bits 24-28 are not used.
        * Bit 29 is the common error group flag. This flag is used to lookup
        * the error text inside the correct array.
        * Bit 31 indicates an error.
        * Bit 30 is set in addition to bit 31 and indicates a warning. 

        """
        code = code & 0xFFFFFFFF # convert the negative integer to the proper hex representation
        hex_ = lambda x: "0x%0.8X" % code
        if code != 0:
            logging.error("Entering error check mode.")
            if not (code & SENSICAM_CODES['PCO_ERROR_IS_WARNING']):
                # Get the offending device and layer.
                #device = code & SENSICAM_CODES['PCO_ERROR_DEVICE_MASK']
                layer = code & SENSICAM_CODES['PCO_ERROR_LAYER_MASK']
                index = code & SENSICAM_CODES['PCO_ERROR_CODE_MASK']

                # Evaluate errors.
                error_text = ''
                if code & SENSICAM_CODES['PCO_ERROR_IS_COMMON']:
                    error_text = PCO_ERROR_COMMON_TXT[index]
                else:
                    if layer == SENSICAM_CODES['PCO_ERROR_FIRMWARE']:
                        error_text = PCO_ERROR_FIRMWARE_TXT[index]
                    elif layer == SENSICAM_CODES['PCO_ERROR_DRIVER']:
                        error_text = PCO_ERROR_DRIVER_TXT[index]
                    elif layer == SENSICAM_CODES['PCO_ERROR_SDKDLL']:
                        error_text = PCO_ERROR_SDKDLL_TXT[index]
                    elif layer == SENSICAM_CODES['PCO_ERROR_APPLICATION']:
                        error_text = PCO_ERROR_APPLICATION_TXT[index]
                    else:
                        error_text = "Unknown error???"
                logging.error(error_text)
                logging.debug("code: " + hex_(code))
                raise SensicamError("Camera error code " + error_text)
            else:
                logging.warn("Sensicam warning: TODO")
    
    # Setup and shutdown
    # ------------------

    def __init__(self, bins=None, crop=None, real=True):
        """Initialize a PCO Sensicam.

        Keyword arguments
        -----------------
        bins : int or None
            Specifies the number of binned pixels to use.
        crop : tuple or None
            A tuple of the form [x, y, width, height] specifying the
            cropped portion of the sensor to use. If None, use the
            full sensor.
        real : bool
            If False, the camera will be simulated.
        
        """
        
        # Check if using a real or simulated camera.
        super(Sensicam, self).__init__(real=real)
        if not self.real_camera:
            return
        self.clib = ctypes.windll.LoadLibrary("sen_cam.dll")

        # Initalize the camera.
        self.filehandle = ctypes.c_int()
        self._chk(self.clib.INITBOARD(0, ctypes.pointer(self.filehandle)))
        self._chk(self.clib.SETUP_CAMERA(self.filehandle))
        self.mode = (0, 0) # Long exposure, normal analog gain

        # Get the "actual" sizes and bits per pixel.
        # Presumably this takes into account hardware cropping and
        # binning, but the documentation is not terribly clear.
        x, y = ctypes.c_int(), ctypes.c_int()
        x_actual = ctypes.c_int()
        y_actual = ctypes.c_int()
        bit_pix = ctypes.c_int()
        self.clib.GETSIZES(
            self.filehandle,
            ctypes.pointer(x), ctypes.pointer(y),
            ctypes.pointer(x_actual), ctypes.pointer(y_actual),
            ctypes.pointer(bit_pix))
        self.x_actual = x_actual.value
        self.y_actual = y_actual.value
        self.bit_pix = bit_pix.value
        self.shape = (x.value, y.value)

        # Write camera settings to the hardware
        self._update_coc()

        # Buffer allocation.
        self.address = ctypes.c_void_p()
        self.buffer_number = ctypes.c_int(-1)
        self.buffer_size = ctypes.c_int(int(self.x_actual*self.y_actual*((self.bit_pix + 7)/8)))
        self._chk(self.clib.ALLOCATE_BUFFER(
            self.filehandle, ctypes.pointer(self.buffer_number),
            ctypes.pointer(self.buffer_size)))
        self._chk(self.clib.MAP_BUFFER(
            self.filehandle, self.buffer_number, self.buffer_size, 0,
            ctypes.pointer(self.address)))
        self._chk(self.clib.SETBUFFER_EVENT(
            self.filehandle, self.buffer_number,
            ctypes.pointer(ctypes.c_int(-1))))

    def _test_coc(self, mode, trigger, crop, bins, delay, t_exp):
        """Test the parameters to give to the SDK SET_COC
        function. This will modify the values using the SDK TEST_COC
        function to the nearest acceptable values.

        The arguments are the same as the kwargs given to
        :func:`_update_coc.`.

        """
        # Prepare C data
        _ptr = lambda x: ctypes.pointer(x)
        logging.debug(
            "Trying the following values for TEST_COC:\n" + \
            "\tmode: %i, %i\n" % (mode[0], mode[1]) + \
            "\ttrigger: %i\n" % trigger + \
            "\tcrop: %i, %i, %i, %i\n" % (crop[0], crop[1], crop[2], crop[3]) + \
            "\tbins: %i\n" % bins + \
            "\ttiming: %i, %i" % (delay, t_exp))
        c_mode = ctypes.c_int(0) #MODE(mode[0], mode[1])
        c_trigger = ctypes.c_int(trigger)
        c_crop_x1 = ctypes.c_int(crop[0])
        c_crop_x2 = ctypes.c_int(crop[1])
        c_crop_y1 = ctypes.c_int(crop[2])
        c_crop_y2 = ctypes.c_int(crop[3])
        xbins, ybins = ctypes.c_int(bins), ctypes.c_int(bins)
        timing = "%i,%i" % (delay, t_exp)
        c_timing = ctypes.c_char_p(timing)
        self._chk(self.clib.TEST_COC(
            self.filehandle, _ptr(c_mode), _ptr(c_trigger),
            _ptr(c_crop_x1), _ptr(c_crop_x2), _ptr(c_crop_y1), _ptr(c_crop_y2),
            _ptr(xbins), _ptr(ybins),
            c_timing, _ptr(ctypes.c_int(len(timing)))))

        # Update values if there are differences
        # TODO: fix mode check
        #if c_mode.value != mode:
        #    logging.debug(
        #        "Desired mode not accepted by TEST_COC, adjusting: %i -> %i" \
        #        % (mode, c_mode.value))
        if c_trigger.value != trigger:
            logging.debug(
                "Desired trigger not accepted by TEST_COC, adjusting: %i -> %i" \
                % (trigger, c_trigger.value))
            trigger = c_trigger.value
        new_crop = [c_crop_x1.value, c_crop_x2.value,
                    c_crop_y1.value, c_crop_y2.value]
        for i, x in enumerate(new_crop):
            if x != crop[i]:
                logging.debug(
                    "Invalid crop parameter from TEST_COC: " + \
                    "Changing crop[%i] = %i -> %i" % (i, crop[i], new_crop[i]))
                crop[i] = x
        if xbins.value != bins or ybins.value != bins:
            logging.debug(
                "Invalid bin argument in TEST_COC. Changing %i -> %i" \
                % (bins, xbins.value))
            bins = xbins
        # TODO: add timing check

        # Return new parameters
        return mode, trigger, crop, bins, delay, t_exp
        
    def _update_coc(self, **kwargs):
        """Update the 'camera operation code', i.e., set everything
        from acquisition modes to triggering to binning. This function
        is intended to be called internally, hence the leading
        underscore. Only keyword arguments that are passed are
        updated.

        TODO: Proper documentation
        TODO: Proper testing

        Keyword arguments
        -----------------
        mode : tuple
            Length 2 tuple describing the camera operation type and
            analog gain. See p. 12 of the manual.
        trigger : int
        crop : tuple
            Length 4 tuple specifying the new region of interest.
        bins : int
            Binning to use.
        delay : int
        t_exp : int
            Exposure time in ms.

        """
        
        # Update mode.
        mode = kwargs.get('mode', (0, 0))
        if len(mode) != 2:
            raise SensicamError("mode must be a length 2 tuple.")
        c_mode = MODE(mode[0], mode[1])

        # Update trigger.
        trigger = kwargs.get('trigger', self._trigger_modes[self.trigger_mode])
        if trigger not in range(2):
            raise SensicamError("trigger_mode most be one of 0, 1, 2.")

        # Update crop
        # NOTE: In the SDK, this is referred to as the ROI, but in our
        # usage, the ROI is set in software. Also, for some reason it
        # wants units of 32 pixels.
        # TODO: clean this up with list comprehension
        crop = kwargs.get('crop', self.crop)
        if len(crop) != 4:
            raise SensicamError("crop must be a length 4 tuple.")
        sensi_crop = [0, 0, 0, 0]
        for i in range(4):
            rem = crop[i] % 32
            if rem != 0:
                sensi_crop[i] = crop[i] + 32*rem
            else:
                sensi_crop[i] = crop[i]
            sensi_crop[i] = sensi_crop[i]/32
        self.crop = crop
        crop = sensi_crop
        
        # Update bins.
        bins = kwargs.get('bins', self.bins)
        if bins not in [2**x for x in range(5)]:
            raise SensicamError("bins must be a power of 2 and <= 16.")

        # Update timing.
        delay = kwargs.get('delay', 0)
        if not 0 <= delay <= 1000000:
            raise SensicamError("delay must be between 0 and 1E6 ms.")
        t_exp = kwargs.get('t_exp', self.t_ms)
        if not 1 <= t_exp <= 1000000:
            raise SensicamError("t_exp must be between 1 and 1E6 ms.")
        timing = ctypes.c_char_p("%i,%i" % (delay, t_exp))

        # Test new values and update class attributes.
        mode, trigger, crop, bins, delay, t_exp = \
            self._test_coc(mode, trigger, crop, bins, delay, t_exp)
        self.crop = crop
        self.bins = bins
        self.t_ms = t_exp

        # Log and update settings.
        logging.debug(
            "Updating Sensicam COC:\n" + \
            "\tmode: %i, %i\n" % (mode[0], mode[1]) + \
            "\ttrigger: %i\n" % trigger + \
            "\tcrop: %i, %i, %i, %i\n" % (crop[0], crop[1], crop[2], crop[3]) + \
            "\tbins: %i\n" % bins + \
            "\ttiming: %i, %i" % (delay, t_exp))
        if not self.real_camera:
             return
        self._chk(self.clib.STOP_COC(self.filehandle, 0))
        self._chk(self.clib.SET_COC(
            self.filehandle, c_mode, trigger,
            crop[0], crop[1], crop[2], crop[3],
            bins, bins, timing))
    
        # TODO: Update x/y_actual more sensibly. Or handle the
        # variable better.
        dummy = ctypes.pointer(ctypes.c_int(-1))
        x_actual = ctypes.c_int(0)
        y_actual = ctypes.c_int(0)
        self.clib.GETSIZES(
            self.filehandle, dummy, dummy,
            ctypes.pointer(x_actual), ctypes.pointer(y_actual), dummy)
        self.x_actual = x_actual.value
        self.y_actual = y_actual.value

        # Re-start the camera.
        # 0 indicates continuous triggering (4 for single trigger).
        # TODO: This should really go somewhere else.
        self._chk(self.clib.RUN_COC(self.filehandle, 0))

    def close(self):
        """Close the camera safely. Anything necessary for doing so
        should be defined here.

        """
        if not self.real_camera:
            return
        self._chk(self.clib.REMOVE_ALL_BUFFERS_FROM_LIST(self.filehandle))
        self._chk(self.clib.FREE_BUFFER(self.filehandle, self.buffer_number))
        self._chk(self.clib.CLOSEBOARD(ctypes.pointer(self.filehandle)))
        
    # Image acquisition
    # -----------------

    def set_acquisition_mode(self, mode):
        """Set the image acquisition mode."""
        super(Sensicam, self).set_acquisition_mode(mode)
        if not self.real_camera:
            return
        # TODO
        logging.warn("No action: set_acquisition_mode not yet implemented.")
        #self._update_coc()

    def acquire_image_data(self):
        """Acquire the current image from the camera."""
        # *2 because the camera returns 16 bit data
        bytes_to_read = self.x_actual*self.y_actual*2
        self._chk(self.clib.READ_IMAGE_12BIT(
            self.filehandle, 0, self.x_actual, self.y_actual, self.address))
        img = np.fromstring(
            ctypes.string_at(self.address, bytes_to_read), dtype=np.uint16)
        shape = (self.crop[1]*32, self.crop[3]*32)[::-1]
        img.shape = shape
        return img
        
    # Triggering
    # ----------

    def get_trigger_mode(self):
        """Query the current trigger mode."""

    def set_trigger_mode(self, mode):
        """Setup trigger mode."""
        super(Sensicam, self).set_trigger_mode(mode)
        if not self.real_camera:
            return
        # TODO
        logging.warn("No action. set_trigger_mode not yet implemented.")
        #self._update_coc() 

    def trigger(self):
        """Send a software trigger to take an image immediately."""
        
    # Shutter control
    # ---------------

    def open_shutter(self):
        """Open the shutter."""
        super(Sensicam, self).open_shutter()
        
    def close_shutter(self):
        """Close the shutter."""
        super(Sensicam, self).close_shutter()

    # Gain and exposure time
    # ----------------------

    def get_exposure_time(self):
        """Query for the current exposure time."""

    def set_exposure_time(self, t, units='ms'):
        """Set the exposure time."""
        super(Sensicam, self).set_exposure_time(t, units)
        if not self.real_camera:
            return
        self._update_coc(t_exp=self.t_ms)

    def get_gain(self):
        """Query the current gain settings."""

    def set_gain(self, gain, **kwargs):
        """Set the camera gain."""
        super(Sensicam, self).set_gain(gain, kwargs)
        if not self.real_camera:
            return
        # TODO
        logging.warn("No action. set_gain not yet implemented.")
        #self._update_coc()

    # ROI, cropping, and binning
    # --------------------------

    def set_roi(self, roi):
        """Define the region of interest."""
        super(Sensicam, self).set_roi(roi)
        # TODO
        
    def get_crop(self):
        """Get the current CCD crop settings."""

    def set_crop(self, crop):
        """
        Define the portion of the CCD to actually collect data
        from. Using a reduced sensor area typically allows for faster
        readout.

        """
        super(Sensicam, self).set_crop(self, crop)
        logging.info("Setting crop to: %s" % repr(self.crop))
        self._update_coc()
        
    def get_bins(self):
        """Query the current binning."""

    def set_bins(self, bins):
        """Set binning to bins x bins."""
        super(Sensicam, self).set_bins(bins)
        logging.info("Setting bins to: %i" % self.bins)
        self._update_coc() 

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    logging.basicConfig(level=logging.DEBUG)
    with Sensicam(real=True) as cam:
        #cam.set_crop([1, 1376, 1, 1040]) # TODO: FIXME
        img = cam.get_image()
        print(img.shape)
        plt.imshow(img, interpolation='none')
        plt.show()
        