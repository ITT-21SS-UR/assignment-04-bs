from evdev import InputDevice

# open an input device
device = InputDevice('/dev/input/event4')

print(device)

# read events and print them
for event in device.read_loop():
    print(event)
