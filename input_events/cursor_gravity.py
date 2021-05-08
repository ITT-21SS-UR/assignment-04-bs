# UInput is used to create a virtual input device
from evdev import UInput, ecodes as e
import time

# specify capabilities for our virtual input device
capabilities = {
    e.EV_REL : (e.REL_X, e.REL_Y), 
    e.EV_KEY : (e.BTN_LEFT, e.BTN_RIGHT),
}

with UInput(capabilities) as device:
    while(True):
        # move the mouse cursor down
        device.write(e.EV_REL, e.REL_X, 2)
        device.write(e.EV_REL, e.REL_Y, 2)
        # separator between events
        device.syn()
        time.sleep(0.01)
