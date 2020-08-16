# import cv2

from config import *
from utils import *
from tqdm import tqdm
import time
import sys


def main(argv):
    if len(argv) == 1:
        wname = u'阴阳师-网易游戏'
    else:
        wname = argv[1]
    father_hwnd = win32gui.FindWindow(0, wname)
    print(father_hwnd)
    while True:
        mx, my = win32api.GetCursorPos()
        wx, wy, ex, ey = win32gui.GetWindowRect(father_hwnd)
        print("{0},{1} / {2},{3}      {4},{5}".format(mx - wx, my - wy, ex-wx, ey-wy, (mx - wx)/(ex-wx), (my-wy)/(ey-wy)))
        time.sleep(0.5)

if __name__ == "__main__":
    main(sys.argv)
