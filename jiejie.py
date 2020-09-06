# import cv2

from config import *
from utils import *
from tqdm import tqdm
import time
import random
from screenshot import do_screen_shot
import sys
import os
import json
from multiprocessing import Process, Manager

shi_shen = [
    (309/1822, 826/1025),
    (497/1822, 827/1025),
    (694/1822, 823/1025),
    (881/1822, 808/1025),
    (1073/1822, 831/1025),
    (1026/1280, 572/720)
]

pixels = [
    (642/1205, 377/678),  # 中间那个点
    (92/1822, 924/1025),  # 选择类别
    (170/1280, 326/720),  # 选择N
    shi_shen[5],  # 选择第六个式神
    (734/1280, 546/720)    # 确认寄养
]

pre_pixels = [
    (401/1205, 317/678), # 启动 40
    (569/1205, 397/678), # 跳过动画 20
    (597/1205, 585/678), # 进入服务器 40

    (1133/1205, 600/678), # 卷轴 5
    (452/1205, 594/678), #寮 5
    (1133/1205, 600/678), #重复一下 5
    (452/1205, 594/678), #重复一下 5

    (918/1205, 615/678), # 结界 10
    (642/1205, 377/678), # 式神育成 10
    (1113/1205, 86/678), # 右上角 5
    (692/1205, 484/678), # 前往查看 10
]

pre_t_list = [40, 20, 40, 5,5,5,5, 10, 10, 5, 10]

t_list = [5, 2, 2, 2, 2]


def seconds_to_02d_str(secs):
    return "%02d:%02d:%02d" % (secs//3600, (secs//60) % 60, secs % 60)


def print_time(wname, due_time):
    sleep_time = int(max(0, due_time - time.time()))
    iso_due_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(due_time))
    print("%s: 剩余 %s 至 %s ,  float: %f" %
          (wname, seconds_to_02d_str(sleep_time), iso_due_time, due_time))


def work(info, cmd, wname, due_time, client):
    sleep_time = due_time - time.time()
    if sleep_time < 0:
        sleep_time = 0.5 + random.random()
    print_time(wname, due_time)

    time.sleep(max(0.05, sleep_time - 600))

    hwnd = getHWND(wname, cmd, client)

    time.sleep(max(0.05, due_time - time.time()))

    do_screen_shot("screenshots\\{0}-0.bmp".format(wname), hWnd=hwnd)
    for i, (t, (fx, fy)) in enumerate(zip(t_list, pixels)):
        x, y = dx*fx, dy*fy
        doClick(hwnd, int(round(x)), int(round(y)))
        time.sleep(random.random()+t)
        do_screen_shot(
            "screenshots\\{0}-{1}.bmp".format(wname, i+1), hWnd=hwnd)

    win32gui.PostMessage(fa_hwnd, win32con.WM_CLOSE, 0, 0)
    ed_dtime = time.time() + 3600.0 * 6.0 + 10 + random.random()
    print_time("何时结束？" + wname + "：", ed_dtime)
    info.append({
        'wname': wname,
        'time': ed_dtime,
        'mode': 'due',
        'cmd': cmd
    })


def main(argv):
    try:
        file_name = argv[1]
        with open(file_name, 'r', encoding='utf-8') as fp:
            info = json.load(fp)
    except:
        print('usage: python {0} <*.json>'.format(argv[0]))
        return
    manager = Manager()

    for i in range(1000):
        return_info = manager.list()
        p_list = []
        for job in info:
            print(job)
            start_time = time.time()
            client = job['client']
            if job['mode'] == 'remain':
                h, m, s = map(int, job['time'].split(':'))
                due_time = start_time+s+m*60+h*3600+random.random()
            elif job['mode'] == 'due':
                due_time = job['time']

            p = Process(target=work, args=(return_info, job['cmd'], job['wname'], due_time, client))
            p_list.append(p)
            p.start()
            time.sleep(0.005)

        for p in p_list:
            p.join()
            
        for p in p_list:
            p.close()
        
        print(return_info)

        info = list(return_info)
        with open('jiejie_info.json', 'w', encoding='utf-8') as fp:
            json.dump(info, fp, ensure_ascii=False)


if __name__ == "__main__":
    print("        mode: due, remain")
    print("  due format: %f")
    print("float format: %02d:%02d:%02d")
    main(sys.argv)
