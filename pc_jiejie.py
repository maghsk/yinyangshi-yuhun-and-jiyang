import win32gui, win32api, win32con, json
import time, random
from screenshot import do_screen_shot
import win32com.client, os
import ctypes, sys

lst_1 = [
    (25/1136, 25/640, 10.0, "cg"),
    (572/1136, 377/640, 3.0, "login"),
    (663/1136, 342/640, 3.0, "android"),
    (570/1136, 547/640, 12.0, "enter the game"),
    (1062/1136, 564/640, 1.6, "scroll"),
    (449/1136, 549/640, 1.6, "阴阳寮"),
    (870/1136, 586/640, 4.0, "结界"),
    (583/1136, 325/640, 1.8, "式神育成1"),
    (1055/1136, 83/640, 1.5, "右上角"),
    (656/1136, 460/640, 4, "前往查看"),
]
lst_2 = [
    (583/1136, 325/640, 1.5, "式神育成2"),
    (55/1136, 575/640, 1.5, "全部"),
    (148/1136, 291/640, 1.5, "N"),
    (792/1136, 499/640, 1.5, "选择式神"),
    (656/1136, 483/640, 1.0, "确认寄养"),
]


def seconds_to_02d_str(secs):
    return "%02d:%02d:%02d" % (secs//3600, (secs//60) % 60, secs % 60)

def print_time(name, due_time):
    sleep_time = int(max(0, due_time - time.time()))
    iso_due_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(due_time))
    print("%s: 剩余 %s 至 %s ,  float: %f" %
          (name, seconds_to_02d_str(sleep_time), iso_due_time, due_time))

def leftClick():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    pass

def doClick(hwnd, fx, fy):
    _,_, width, height = win32gui.GetClientRect(hwnd)
    cx = int(round(fx * width))
    cy = int(round(fy * height))
    long_position = win32api.MAKELONG(cx, cy)  # 模拟鼠标指针 传送到指定坐标
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, long_position)  # 模拟鼠标按下
    time.sleep(0.03 + random.random()*0.01)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, long_position)  # 模拟鼠标弹起


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    file_name = 'jiejie_info.json'
    with open(file_name, 'r', encoding='utf-8') as fp:
        info = json.load(fp)
    wname = info['wname']
    cmd = info['cmd']
    end_time = info['time']
    uuid = info['uuid']
    for i in range(10000):
        if not os.path.exists(os.path.join('screenshots', uuid)):
            os.mkdir(os.path.join('screenshots', uuid))
        print_time(uuid, end_time)
        time.sleep(max(0.5, end_time - time.time() - 360))

        hwnd = win32gui.FindWindow(0, wname)
        need_pre = False
        if hwnd == 0:
            os.system('start "" ' + cmd)
            time.sleep(20)
            hwnd = win32gui.FindWindow(0, wname)
            need_pre = True
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys('%')
        if need_pre:
            for i, (x, y, st, text) in enumerate(lst_1):
                print('clicking', text)
                if text == 'login':
                    doClick(win32gui.FindWindow(0, u'登录'), 181/360, 271/400)
                else:
                    doClick(hwnd, x, y)
                time.sleep(st + random.random())
                do_screen_shot(os.path.join('screenshots', uuid, 'pre-{0}-{1}.bmp'.format(i, text)), hwnd)
        time.sleep(max(0.5, end_time - time.time()))
        for i, (x, y, st, text) in enumerate(lst_2):
            print('clicking', text)
            doClick(hwnd, x, y)
            time.sleep(st + random.random())
            do_screen_shot(os.path.join('screenshots', uuid, '{0}-{1}.bmp'.format(i, text)), hwnd)
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        time.sleep(1)
        msgbox_hwnd = win32gui.FindWindow(0, '退出游戏')
        win32gui.PostMessage(msgbox_hwnd, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
        win32gui.PostMessage(msgbox_hwnd, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
        end_time = time.time() + 3600*6 + 10 + random.random()
        print(end_time)
        info['time'] = end_time
        with open(file_name, 'w', encoding='utf-8') as fp:
            json.dump(info, fp, ensure_ascii=False)
    
if __name__ == "__main__":
    if is_admin():
        main()
    else:
        # Re-run the program with admin rights
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
