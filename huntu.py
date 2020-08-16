# import cv2

from config import *
from utils import *
from tqdm import tqdm


def main():
    total_times = int(input(u'请输入刷多少体力的魂土：').strip()) // 8
    print("一共要刷 {0} 次！".format(total_times))
    print()
    hwnd_list = []
    sleep_time = SLEEP_TIME_DICT['huntu'] + random.random()

    for father_name in FATHER_WINDOW_NAMES:
        father_hwnd = win32gui.FindWindow(0, father_name)
        win32gui.EnumChildWindows(father_hwnd, call_back, hwnd_list)

    start = time.time()

    for i in range(total_times):
        print("第 {0}/{1} 次来过~".format(i+1, total_times))
        cur = time.time()
        x, y = rect_norm_rand_gen((2280 + 5, 680 + 5), (2360 - 5, 760 - 5))
        x, y = (x + y) / 2, (x - y) / 2
        doClick(hwnd_list[0], int(x), int(y))

        slt = sleep_time + random.random() * 2
        print("开打，休眠 {0} 秒...".format(slt))
        tqdm_sleep(slt)

        do_series(hwnd_list, ENDING_PIXELS)
        time.sleep(random.random() * 0.5 + 2.3)
        now = time.time()
        print("完成！本次用时 {0} 秒，累计用时 {1} 秒，平均用时 {2} 秒，预计剩余 {3} 秒。".format(
            now - cur, now - start, (now - start) / (i + 1), (now - start) / (i + 1) * (total_times - i - 1)))
        # hwnd1 = win32gui.FindWindowEx(hwnd, None,'类名称', None) # 目标子句柄
        # windowRec = win32gui.GetWindowRect(hwnd1) # 目标子句柄窗口的坐标

    print("关闭掉落加成中...")
    do_series(hwnd_list, DROP_BONUS_PIXELS, a=0.3, b=0.8)
    do_series(hwnd_list, [EXIT_PIXEL], a=0.5, b=0.5)
    end = time.time()
    print("全部完成。共用时 {0} 秒。".format(end - start))


if __name__ == "__main__":
    main()
