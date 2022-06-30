import time
import board
import touchio
import usb_hid

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

pins = (board.A3, board.A4)
pressed = []
keycodes = [ Keycode.SPACE, Keycode.KEYPAD_ZERO ]
keyboard = Keyboard(usb_hid.devices)

touch_keys = []
last_value = []
for x, pin in enumerate(pins):
    touch_keys.append(touchio.TouchIn(pin))
    pressed.append("0")

last_time = time.monotonic()
count = 0
u_count = 0

update_time = 0

while True:
    touch_raw = []
    if (time.monotonic() - update_time) >= 0.001: 
        u_count += 1
        update_time = time.monotonic()
        for x, key in enumerate(touch_keys):
            touch_raw.append(key.raw_value)
            if (key.raw_value > 2500) and not pressed[x]:
                print(x, "pressed.")
                keyboard.press(keycodes[x])
                pressed[x] = 1
            if (key.raw_value < 2000) and pressed[x]:
                print(x, "released.")
                keyboard.release(keycodes[x])
                pressed[x] = 0
    # print(touch_raw)
    # print(touch_keys)

    count+=1
    if (time.monotonic() - last_time) > 1: 
        last_time = time.monotonic()
        print(count, "+", u_count)
        count = 0
        u_count = 0
