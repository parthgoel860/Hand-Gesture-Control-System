import numpy as np
import screen_brightness_control as sbc

# ----------- VOLUME CONTROL -----------

from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_,
    CLSCTX_ALL,
    None
)

volume = cast(interface, POINTER(IAudioEndpointVolume))


def set_volume(distance):
    vol = np.interp(distance, [20, 200], [-65, 0])
    volume.SetMasterVolumeLevel(vol, None)


# ----------- BRIGHTNESS CONTROL -----------
def set_brightness(distance):
    bright = np.interp(distance, [20, 200], [0, 100])
    sbc.set_brightness(int(bright))