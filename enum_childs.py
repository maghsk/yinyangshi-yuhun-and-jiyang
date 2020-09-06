import win32gui, win32api, win32con, json
import time, random
from screenshot import do_screen_shot
import win32com.client, os
def cb(hwnd, param):
    param.append((hwnd, win32gui.GetWindowText(hwnd)))
if __name__ == "__main__":
    hwnd = win32gui.FindWindow(0, u'阴阳师-网易游戏')
    lst = []
    win32gui.EnumChildWindows(hwnd, cb, lst)
    print(lst)
    