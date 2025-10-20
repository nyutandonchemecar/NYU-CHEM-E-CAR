# pip install pyautogui
import pyautogui
import time

# Wait a few seconds before starting (so you can click into a text box)
time.sleep(3)

# Type the word "hello"
pyautogui.typewrite("hello", interval=0.2)
