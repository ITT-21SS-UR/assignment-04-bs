# UInput is used to create a virtual input device
from evdev import UInput, ecodes as e
import time

# specify capabilities for our virtual input device
capabilities = {
    e.EV_REL : (e.REL_X, e.REL_Y), 
    e.EV_KEY : (e.BTN_LEFT, e.BTN_RIGHT),
}

delay = 0.1     # time between clicks
hold_time = 0.1 # time the button is held down

with UInput(capabilities) as device:
    while(True):
        # click
        device.write(e.EV_KEY, e.BTN_LEFT, 1)
        device.syn()

        time.sleep(hold_time)
        
        # release
        device.write(e.EV_KEY, e.BTN_LEFT, 0)
        device.syn()

        time.sleep(delay)
