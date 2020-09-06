# import cv2

from config import *
from utils import *
from tqdm import tqdm
import time
import sys


def main(argv):
    father_hwnd = win32gui.FindWindow(0, argv[1])
    try:
        hwnd_list = []
        win32gui.EnumChildWindows(father_hwnd, call_back, hwnd_list)
        hwnd = hwnd_list[0]
    except:
        hwnd = father_hwnd
        print("NOTFOUND NOX")
    while True:
        mx, my = win32api.GetCursorPos()
        x1, y1, x2, y2 = win32gui.GetClientRect(hwnd)
        # x1, y1 = win32gui.ClientToScreen(hwnd, (x1,y1))
        # x2, y2 = win32gui.ClientToScreen(hwnd, (x2,y2))
        mx, my = win32gui.ScreenToClient(hwnd, (mx, my))
        print("{0}/{1}, {2}/{3}      {4},{5}".format(mx - x1, x2 - x1, my-y1, y2-y1, (mx - x1)/(x2-x1), (my-y1)/(y2-y1)))
        time.sleep(0.5)

if __name__ == "__main__":
    main(sys.argv)
