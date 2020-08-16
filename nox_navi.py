# import cv2

from config import *
from utils import *
from tqdm import tqdm
import time
import sys


def main(argv):
    father_hwnd = win32gui.FindWindow(0, u'司机')
    hwnd_list = []
    win32gui.EnumChildWindows(father_hwnd, call_back, hwnd_list)
    hwnd = hwnd_list[0]
    while True:
        mx, my = win32api.GetCursorPos()
        wx, wy, ex, ey = win32gui.GetWindowRect(hwnd)
        print("{0}/{2}, {1}/{3}      {4},{5}".format(mx - wx, my - wy, ex-wx, ey-wy, (mx - wx)/(ex-wx), (my-wy)/(ey-wy)))
        time.sleep(0.5)

if __name__ == "__main__":
    main(sys.argv)
