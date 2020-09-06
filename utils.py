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
    # cx,cy = win32gui.ScreenToClient(hwnd, (cx, cy))
    long_position = win32api.MAKELONG(cx, cy)  # 模拟鼠标指针 传送到指定坐标
    # win32gui.PostMessage(hwnd, win32con.WM_ACTIVATE,win32con.WA_ACTIVE,0)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN,
                         win32con.MK_LBUTTON, long_position)  # 模拟鼠标按下
    time.sleep(0.01)
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
    print(win32gui.GetWindowText(hwnd))
    if win32gui.GetWindowText(hwnd) == CLASSNAME_IN_NOX:
        param.append(hwnd)


def tqdm_sleep(secs):
    mx = int(secs)
    for i in tqdm(range(mx)):
        secs -= 1
        time.sleep(1)
    time.sleep(secs)


def getHWND(wname, cmd, client):
    if client == 'pc':
        hwnd = win32gui.FindWindow(0, wname)
        if hwnd == 0:
            os.system('start "" ' + cmd)
            time.sleep(20)
            hwnd = win32gui.FindWindow(0, wname)
            pass
    elif client == 'nox':
        fa_hwnd = win32gui.FindWindow(0, wname)
        if fa_hwnd == 0:
            os.system('start "" ' + cmd)
            time.sleep(100)
            fa_hwnd = win32gui.FindWindow(0, wname)
            hwnd_list = []
            win32gui.EnumChildWindows(fa_hwnd, call_back, hwnd_list)
            hwnd = hwnd_list[0]
            x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
            dx = x2-x1
            dy = y2-y1

            do_screen_shot("screenshots\\{0}-pre-0.bmp".format(wname), hWnd=hwnd)
            for i, (t, (fx, fy)) in enumerate(zip(pre_t_list, pre_pixels)):
                x, y = dx*fx, dy*fy
                doClick(hwnd, int(round(x)), int(round(y)))
                time.sleep(t)
                do_screen_shot(
                    "screenshots\\{0}-pre-{1}.bmp".format(wname, i+1), hWnd=hwnd)
        else:
            hwnd_list = []
            win32gui.EnumChildWindows(fa_hwnd, call_back, hwnd_list)
            hwnd = hwnd_list[0]
            x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
            dx = x2-x1
            dy = y2-y1
    return hwnd


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
