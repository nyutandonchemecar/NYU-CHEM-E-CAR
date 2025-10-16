import pyautogui
import time

# Move mouse 20 pixels right, wait 1 second, then 20 pixels down
# on terminal type: pip install pyautogui
for i in range(5):  # repeat 5 times; change or remove loop as desired
    pyautogui.moveRel(20, 0, duration=1)   # move right by 20 pixels in 1 second
    pyautogui.moveRel(0, 20, duration=1)   # move down by 20 pixels in 1 second
