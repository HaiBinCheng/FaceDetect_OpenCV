import cv2
import numpy as np
import win32gui
import win32ui
import win32con
import win32api
from PIL import ImageGrab, Image, ImageDraw
from ctypes import windll
import time
MAX = 10
hwnd, left, top, right, bottom = 0, 0, 0, 0, 0
loop_cnt = 0
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def get_Windows_hwnd(title): 
    # 定义
    global left, top, right, bottom
    global hwnd, loop_cnt
    # test
    print("title is title ", title)
    hwnd = win32gui.FindWindow(None, title)
    print("handle is ", hwnd)

    # 获取窗口标题
    title = win32gui.GetWindowText(hwnd)

    print("Windows Title is ",title)

    if hwnd != 0:
        # 尝试获取窗口信息
        for i in range(10):  # 最多重试10次
            try:
                # 发送一个 WM_NULL 消息，等待窗口处理完成
                win32gui.SendMessageTimeout(hwnd, win32con.WM_NULL, 0, 0, win32con.SMTO_ABORTIFHUNG, 1000)
                left, top, right, bottom = win32gui.GetClientRect(hwnd)
                print("Windows info l,t,r,b", left, top, right, bottom)
                print("Win Hwnd Success ++++++++!")
                break  # 获取成功，退出循环
            except:
                loop_cnt += 1
                print(f'获取窗口信息失败')
                time.sleep(0.1)  # 等待一段时间后重试
    else:
        print('未找到窗口')
        return -1
    return 0
    

def grab_screen(title):
    # left, top, right, bottom = 0, 0, 0, 0
    # 获取窗口句柄
    # hwnd = win32gui.FindWindow(None, title)
    # 获取窗口位置
    # left, top, right, bottom = win32gui.GetClientRect(hwnd)
    # 获取窗口DC
    hwndDC = win32gui.GetWindowDC(hwnd)
    # 创建DC
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    # 创建位图
    saveDC = mfcDC.CreateCompatibleDC()
    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, right - left, bottom - top)
    saveDC.SelectObject(saveBitMap)
    # 截图并保存到位图
    windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)
    # 转换为OpenCV格式
    signedIntsArray = saveBitMap.GetBitmapBits(True)

    img = ImageGrab.grab(bbox=(left, top, right, bottom))
    print(img.size)

    img = np.frombuffer(signedIntsArray, dtype='uint8')
    # 窗口数据异常会导致shape函数报错
    if bottom != top and right != left:
        img.shape = (bottom - top, right - left, 4)
    img = cv2.cvtColor(img, cv2.COLOR_RGBA2RGB)
    # 释放资源
    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    # 返回图像
    return img

# 延时函数
def delay_Detect(t):
    time.sleep(t)
    # print("Delay time", t)

# 绘制函数
def drawFaceinfo(hwnd_dc, rect):
    # 获取窗口DC
    dc = win32gui.GetDC(hwnd)

    # 设置背景模式为透明
    win32gui.SetBkMode(dc, win32con.TRANSPARENT)

    # 创建红色画笔
    # pen = win32gui.CreatePen(win32con.PS_SOLID, 1, win32api.RGB(255, 0, 0))

    # 创建透明画刷
    hbrush = win32gui.CreateSolidBrush(0)

    # 将画笔选入DC
    old_pen = win32gui.SelectObject(dc, hbrush)

    # Test draw face Frame
    rect = (10, 10, 100, 100)
    # 绘制矩形
    # color = (255, 0, 0, 0)  # 注意最后一位为 alpha 通道值，设为 0 表示完全透明
    win32gui.Rectangle(dc, *rect)

    # 恢复原来的画笔
    win32gui.SelectObject(dc, old_pen)

    # 释放DC
    win32gui.ReleaseDC(hwnd, dc)



    # # 创建一个 RGBA 的空白图像
    # width, height = right - left, bottom - top
    # img = Image.new('RGBA', (width, height), (255, 255, 255, 0))

    # # 创建一个 ImageDraw 对象，用于绘制矩形框
    # draw = ImageDraw.Draw(img)

    # # 绘制矩形框
    # # for (x, y, w, h) in faces:
    # draw.rectangle([(rect[0], rect[1]), (rect[2], rect[3])], outline=(255, 0, 0), width=2)

    # # 将图像转换为 Win32 位图格式，并获取 DC
    # # 下面的语法只能转换黑白图像
    # # bmp = img.convert('RGB').tobitmap()
    # img_gray = img.convert('L')
    # bmp = img_gray.tobitmap()
    # dc = win32gui.CreateCompatibleDC(None)
    # win32gui.SelectObject(dc, bmp)

    # # 将图像复制到屏幕上
    # win32gui.BitBlt(
    #     hwnd_dc, left, top, width, height, dc, 0, 0, win32con.SRCCOPY
    # )

    # # 释放资源
    # win32gui.DeleteDC(dc)
    # win32gui.DeleteObject(bmp)


# Main Fun++++++++++++++++++++++++++++++
# 指定窗口标题
# window_title = 'R.jpg - 看图'
# window_title = '穿越火线'
window_title = 'R1.jpg - 看图'
while True:

    # 获取窗口句柄值和大小
    ret = get_Windows_hwnd(window_title)
    if ret != 0 and loop_cnt ==  MAX:
        print("ret ", ret)
        break

    # 截取窗口图像
    img = grab_screen(window_title)

    # 将图像转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 使用级联分类器检测人脸
    delay_Detect(0.5)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # 绘制检测到的人脸并返回人脸位置、大小和个数
    delay_Detect(0.5)
    face_count = 0

    if len(faces) == 0:
        print("No faces detected -------------")
        # 释放摄像头并关闭所有窗口        
        cv2.destroyAllWindows()
    else:
        hwnd_dc = win32gui.GetWindowDC(hwnd)
        for (x, y, w, h) in faces:
            # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            face_count += 1

            # Draw face Info
            rect = (x, y, x+w, y+h)
            # 绘制人脸框，红色人脸框
            # drawFaceinfo(hwnd_dc, rect)

            # 绘制聚焦信息，虚线部分
            win32gui.DrawFocusRect(hwnd_dc, rect)

            # 输出人脸信息
            print("人脸坐标位置：({}, {}), 人脸大小：{}, {}".format(x, y, w, h))
            print(f"Detected {len(faces)} faces +++++++++++")
            if face_count >= 5:
                print("目前支持最大检测Face Num 为 5 !!!")


    delay_Detect(0.5)
    # 显示图像
    # cv2.imshow('Face Detection', img)

    # 刷新窗口
    if len(faces) != 0:
        delay_Detect(2)
        win32gui.UpdateWindow(hwnd)

    # 读取键盘输入
    key = cv2.waitKey(1) & 0xFF
    # 按下'q'键退出循环
    if key == ord('q'):
        break

# 释放资源
cv2.destroyAllWindows()
# save_dc.DeleteDC()
# win32gui.ReleaseDC(hwnd, hwnd_dc)
# win32gui.ReleaseDC(hwnd, dc)
