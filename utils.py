import os
import random

import win32gui
import win32api
import win32con
import time
import numpy
from tqdm import tqdm
from config import FACTOR, CLASSNAME_IN_NOX


def range_norm_rand_gen(mu, sigma, LR, factor):
    ret = None
    while ret is None or ret < LR[0] or ret > LR[1]:
        ret = numpy.random.normal(mu, sigma)
    return ret * factor


def doClick(hwnd, cx, cy, verbose=True):
    if verbose:
        print("点击了 ({0}, {1})".format(cx, cy))
        pass
    long_position = win32api.MAKELONG(cx, cy)  # 模拟鼠标指针 传送到指定坐标
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN,
                         win32con.MK_LBUTTON, long_position)  # 模拟鼠标按下
    time.sleep(0.05)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP,
                         0, long_position)  # 模拟鼠标弹起


def do_series(hwnd_list, pixels, a=0.25, b=0.41):
    for pix in pixels:
        for hwnd in hwnd_list:
            x, y = rect_norm_rand_gen(*pix)
            doClick(hwnd, int(x), int(y))
        time.sleep(random.random() * a + b)
    pass


def rect_norm_rand_gen(lu, rd, factor=1.0/FACTOR):
    return tuple(range_norm_rand_gen((l + r) / 2, (r - l) / 3, (l, r), factor=factor) for l, r in zip(lu, rd))


def call_back(hwnd, param):
    if win32gui.GetWindowText(hwnd) == CLASSNAME_IN_NOX:
        param.append(hwnd)


def tqdm_sleep(secs):
    mx = int(secs)
    for i in tqdm(range(mx)):
        secs -= 1
        time.sleep(1)
    time.sleep(secs)


# def doADBClick(x, y):
#     os.system(
#         "adb\\adb.exe -s 6UK9X19727001538 shell input tap {0} {1}".format(x, y))


# x+y: 2280~2360
# x-y: 680~760

# def match(small, large):
# 	    small = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
# 	    small = cv2.Canny(small, 50, 200)
#
# 	    large = cv2.cvtColor(large, cv2.COLOR_BGR2GRAY)
# 	    large = cv2.Canny(large, 50, 200)
# 	    result = cv2.matchTemplate(large, small, cv2.TM_CCOEFF)
# 	    _, max_value, _, max_loc = cv2.minMaxLoc(result)
# 	    return (max_value, max_loc, 1, result)
