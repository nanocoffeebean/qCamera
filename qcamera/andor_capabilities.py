"""Utilities for determining Andor properties"""

import ctypes
_ulong = ctypes.c_ulong

constants = {
    "AC_ACQMODE_ACCUMULATE": 4, 
    "AC_ACQMODE_FASTKINETICS": 32, 
    "AC_ACQMODE_FRAMETRANSFER": 16, 
    "AC_ACQMODE_KINETIC": 8, 
    "AC_ACQMODE_OVERLAP": 64, 
    "AC_ACQMODE_SINGLE": 1, 
    "AC_ACQMODE_VIDEO": 2, 
    "AC_CAMERATYPE_CCD": 4, 
    "AC_CAMERATYPE_CLARA": 17, 
    "AC_CAMERATYPE_EMCCD": 3, 
    "AC_CAMERATYPE_ICCD": 2, 
    "AC_CAMERATYPE_IDUS": 7, 
    "AC_CAMERATYPE_IKON": 13, 
    "AC_CAMERATYPE_INGAAS": 14, 
    "AC_CAMERATYPE_ISTAR": 5, 
    "AC_CAMERATYPE_IVAC": 15, 
    "AC_CAMERATYPE_IVACULTRA": 23, 
    "AC_CAMERATYPE_IXON": 1, 
    "AC_CAMERATYPE_IXONULTRA": 21, 
    "AC_CAMERATYPE_LUCA": 11, 
    "AC_CAMERATYPE_NEO": 20, 
    "AC_CAMERATYPE_NEWTON": 8, 
    "AC_CAMERATYPE_PDA": 0, 
    "AC_CAMERATYPE_RESERVED": 12, 
    "AC_CAMERATYPE_SIMCAM": 19, 
    "AC_CAMERATYPE_SURCAM": 9, 
    "AC_CAMERATYPE_UNPROGRAMMED": 16, 
    "AC_CAMERATYPE_USBICCD": 10, 
    "AC_CAMERATYPE_USBISTAR": 18, 
    "AC_CAMERATYPE_VIDEO": 6, 
    "AC_CAMERATYPE_VOLMOS": 22, 
    "AC_EMGAIN_12BIT": 2, 
    "AC_EMGAIN_8BIT": 1, 
    "AC_EMGAIN_LINEAR12": 4, 
    "AC_EMGAIN_REAL12": 8, 
    "AC_FEATURES_CAMERALINK": 134217728, 
    "AC_FEATURES_COUNTCONVERT": 262144, 
    "AC_FEATURES_DACCONTROL": 16384, 
    "AC_FEATURES_DDGLITE": 2048, 
    "AC_FEATURES_DEFECT_CORRECTION": 16777216, 
    "AC_FEATURES_DUALMODE": 524288, 
    "AC_FEATURES_DUALPREAMPGAIN": 8388608, 
    "AC_FEATURES_ENDOFEXPOSURE_EVENT": 67108864, 
    "AC_FEATURES_EVENTS": 2, 
    "AC_FEATURES_EXTERNAL_I2C": 32, 
    "AC_FEATURES_FANCONTROL": 128, 
    "AC_FEATURES_FTEXTERNALEXPOSURE": 4096, 
    "AC_FEATURES_IOCONTROL": 65536, 
    "AC_FEATURES_KEEPCLEANCONTROL": 1024, 
    "AC_FEATURES_KINETICEXTERNALEXPOSURE": 8192, 
    "AC_FEATURES_METADATA": 32768, 
    "AC_FEATURES_MIDFANCONTROL": 256, 
    "AC_FEATURES_OPTACQUIRE": 1048576, 
    "AC_FEATURES_PHOTONCOUNTING": 131072, 
    "AC_FEATURES_POLLING": 1, 
    "AC_FEATURES_POSTPROCESSSPURIOUSNOISEFILTER": 4194304, 
    "AC_FEATURES_REALTIMESPURIOUSNOISEFILTER": 2097152, 
    "AC_FEATURES_SATURATIONEVENT": 64, 
    "AC_FEATURES_SHUTTER": 8, 
    "AC_FEATURES_SHUTTEREX": 16, 
    "AC_FEATURES_SPOOLING": 4, 
    "AC_FEATURES_STARTOFEXPOSURE_EVENT": 33554432, 
    "AC_FEATURES_TEMPERATUREDURINGACQUISITION": 512, 
    "AC_GETFUNCTION_BASELINECLAMP": 32768, 
    "AC_GETFUNCTION_DDGTIMES": 256, 
    "AC_GETFUNCTION_DETECTORSIZE": 8, 
    "AC_GETFUNCTION_EMCCDGAIN": 32, 
    "AC_GETFUNCTION_GAIN": 16, 
    "AC_GETFUNCTION_GATEDELAYSTEP": 4096, 
    "AC_GETFUNCTION_GATEMODE": 128, 
    "AC_GETFUNCTION_GATESTEP": 4096, 
    "AC_GETFUNCTION_GATEWIDTHSTEP": 65536, 
    "AC_GETFUNCTION_HVFLAG": 64, 
    "AC_GETFUNCTION_ICCDGAIN": 16, 
    "AC_GETFUNCTION_INSERTION_DELAY": 2048, 
    "AC_GETFUNCTION_INTELLIGATE": 1024, 
    "AC_GETFUNCTION_IOC": 512, 
    "AC_GETFUNCTION_MCPGAIN": 16, 
    "AC_GETFUNCTION_MCPGAINTABLE": 16384, 
    "AC_GETFUNCTION_PHOSPHORSTATUS": 8192, 
    "AC_GETFUNCTION_TARGETTEMPERATURE": 2, 
    "AC_GETFUNCTION_TEMPERATURE": 1, 
    "AC_GETFUNCTION_TEMPERATURERANGE": 4, 
    "AC_PIXELMODE_14BIT": 2, 
    "AC_PIXELMODE_16BIT": 4, 
    "AC_PIXELMODE_32BIT": 8, 
    "AC_PIXELMODE_8BIT": 1, 
    "AC_PIXELMODE_CMY": 131072, 
    "AC_PIXELMODE_MONO": 0, 
    "AC_PIXELMODE_RGB": 65536, 
    "AC_READMODE_FULLIMAGE": 1, 
    "AC_READMODE_FVB": 8, 
    "AC_READMODE_MULTITRACK": 16, 
    "AC_READMODE_MULTITRACKSCAN": 64, 
    "AC_READMODE_RANDOMTRACK": 32, 
    "AC_READMODE_SINGLETRACK": 4, 
    "AC_READMODE_SUBIMAGE": 2, 
    "AC_SETFUNCTION_BASELINECLAMP": 32, 
    "AC_SETFUNCTION_BASELINEOFFSET": 256, 
    "AC_SETFUNCTION_CROPMODE": 1024, 
    "AC_SETFUNCTION_DDGTIMES": 131072, 
    "AC_SETFUNCTION_DMAPARAMETERS": 2048, 
    "AC_SETFUNCTION_EMADVANCED": 32768, 
    "AC_SETFUNCTION_EMCCDGAIN": 16, 
    "AC_SETFUNCTION_EXTENDEDNIR": 8388608, 
    "AC_SETFUNCTION_EXTENDED_CROP_MODE": 268435456, 
    "AC_SETFUNCTION_GAIN": 8, 
    "AC_SETFUNCTION_GATEDELAYSTEP": 2097152, 
    "AC_SETFUNCTION_GATEMODE": 65536, 
    "AC_SETFUNCTION_GATESTEP": 2097152, 
    "AC_SETFUNCTION_GATEWIDTHSTEP": 134217728, 
    "AC_SETFUNCTION_HIGHCAPACITY": 128, 
    "AC_SETFUNCTION_HORIZONTALBIN": 4096, 
    "AC_SETFUNCTION_HREADOUT": 2, 
    "AC_SETFUNCTION_ICCDGAIN": 8, 
    "AC_SETFUNCTION_INSERTION_DELAY": 1048576, 
    "AC_SETFUNCTION_INTELLIGATE": 524288, 
    "AC_SETFUNCTION_IOC": 262144, 
    "AC_SETFUNCTION_MCPGAIN": 8, 
    "AC_SETFUNCTION_MULTITRACKHRANGE": 8192, 
    "AC_SETFUNCTION_PREAMPGAIN": 512, 
    "AC_SETFUNCTION_PRESCANS": 67108864, 
    "AC_SETFUNCTION_RANDOMTRACKNOGAPS": 16384, 
    "AC_SETFUNCTION_REGISTERPACK": 33554432, 
    "AC_SETFUNCTION_SPOOLTHREADCOUNT": 16777216, 
    "AC_SETFUNCTION_TEMPERATURE": 4, 
    "AC_SETFUNCTION_TRIGGERTERMINATION": 4194304, 
    "AC_SETFUNCTION_VREADOUT": 1, 
    "AC_SETFUNCTION_VSAMPLITUDE": 64, 
    "AC_TRIGGERMODE_BULB": 32, 
    "AC_TRIGGERMODE_CONTINUOUS": 8, 
    "AC_TRIGGERMODE_EXTERNAL": 2, 
    "AC_TRIGGERMODE_EXTERNALEXPOSURE": 32, 
    "AC_TRIGGERMODE_EXTERNALSTART": 16, 
    "AC_TRIGGERMODE_EXTERNAL_CHARGESHIFTING": 128, 
    "AC_TRIGGERMODE_EXTERNAL_FVB_EM": 4, 
    "AC_TRIGGERMODE_INTERNAL": 1, 
    "AC_TRIGGERMODE_INVERTED": 64
}

class AndorCapabilities(ctypes.Structure):
    _fields_ = [
        ("ulSize", _ulong),
        ("ulAcqModes", _ulong),
        ("ulReadModes", _ulong),
        ("ulTriggerModes", _ulong),
        ("ulCameraType", _ulong),
        ("ulPixelMode", _ulong),
        ("ulSetFunctions", _ulong),
        ("ulGetFunctions", _ulong),
        ("ulFeatures", _ulong),
        ("ulPCICard", _ulong),
        ("ulEMGainCapability", _ulong),
        ("ulFTReadModes", _ulong)
    ]

    def __str__(self):
        attrs = dir(self)
        out = ''
        for attr in attrs:
            if attr[:2] == 'ul':
                out += "%s = %i\n" % (attr, getattr(self, attr))
        return out
        