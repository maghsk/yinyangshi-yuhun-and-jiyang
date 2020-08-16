# import cv2

from config import *
from utils import *
from tqdm import tqdm
import time
import random
from screenshot import do_screen_shot
import sys
import json
from multiprocessing import Process

shi_shen = [
    (309/1822, 826/1025),
    (497/1822, 827/1025),
    (694/1822, 823/1025),
    (881/1822, 808/1025),
    (1073/1822, 831/1025),
    (1269/1822, 817/1025)
]

pixels = [
    (942/1822, 453/1025),  # 中间那个点
    (92/1822, 924/1025),  # 选择类别
    (244/1822, 465/1025),  # 选择N
    shi_shen[5],  # 选择第六个式神
    (695/1205, 511/678)    # 确认寄养
]

t_list = [5, 2, 2, 2, 2]


def work(wname, due_time, start_time):
    sleep_time = due_time - start_time
    if sleep_time < 0:
        sleep_time = 0.5 + random.random() * 0.1
    i = int(sleep_time)
    print("%s: %02d:%02d:%02d   due: %f" % (wname, i//3600, (i//60) % 60, i % 60, due_time))
    time.sleep(sleep_time)
    fa_hwnd = win32gui.FindWindow(0, wname)
    hwnd_list = []
    win32gui.EnumChildWindows(fa_hwnd, call_back, hwnd_list)
    hwnd = hwnd_list[0]

    do_screen_shot("screenshots\\{0}-0.bmp".format(wname), hWnd=hwnd)
    x1, y1, x2, y2 = win32gui.GetWindowRect(hwnd)
    dx = x2-x1
    dy = y2-y1
    for i, (t, (fx, fy)) in enumerate(zip(t_list, pixels)):
        x, y = dx*fx, dy*fy
        doClick(hwnd, int(round(x)), int(round(y)))
        time.sleep(random.random()+t)
        do_screen_shot(
            "screenshots\\{0}-{1}.bmp".format(wname, i+1), hWnd=hwnd)

    win32gui.PostMessage(fa_hwnd, win32con.WM_CLOSE, 0, 0)


def main(argv):
    try:
        file_name = argv[1]
        with open('jiejie_info.json', 'r', encoding='utf-8') as fp:
            info = json.load(fp)
    except:
        print('usage: python {0} <*.json>'.format(argv[0]))
        return
    p_list = []
    for job in info:
        print(job)
        start_time = time.time()
        if job['mode'] == 'remain':
            h, m, s = map(int, job['time'].split(':'))
            p = Process(target=work, args=(job['wname'], start_time+s+m*60+h*3600+random.random(), start_time))
        elif job['mode'] == 'due':
            p = Process(target=work, args=(job['wname'], job['time'], start_time))
        p_list.append(p)
        p.start()
        time.sleep(0.005)
    
    for p in p_list:
        p.join()


if __name__ == "__main__":
    main(sys.argv)
