# import cv2

from config import *
from utils import *
from tqdm import tqdm
import time
import random
from PIL import ImageGrab
import win32ui


def mul_factor(x):
    return int(x*FACTOR)


def do_screen_shot(file_name, hWnd):
    x1, y1, x2, y2 = map(mul_factor, win32gui.GetWindowRect(hWnd))
    print("screenshot at", x1, y1, x2, y2)
    dx = x2-x1
    dy = y2-y1
    #返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
    hWndDC = win32gui.GetWindowDC(hWnd)
    #创建设备描述表
    mfcDC = win32ui.CreateDCFromHandle(hWndDC)
    #创建内存设备描述表
    saveDC = mfcDC.CreateCompatibleDC()
    #创建位图对象准备保存图片
    saveBitMap = win32ui.CreateBitmap()
    #为bitmap开辟存储空间
    saveBitMap.CreateCompatibleBitmap(mfcDC,dx,dy)
    #将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    #保存bitmap到内存设备描述表
    saveDC.BitBlt((0,0), (dx,dy), mfcDC, (0, 0), win32con.SRCCOPY)

    saveBitMap.SaveBitmapFile(saveDC,file_name)
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hWnd,hWndDC)

def main():
    do_screen_shot("test.bmp")


if __name__ == "__main__":
    main()
