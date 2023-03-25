import numpy as np
import cv2
from PIL import ImageGrab
import time

# 延时函数
def delay_Detect(t):
    time.sleep(t)
    print("Delay time", t)


while True:
    # 截取整个屏幕
    img = np.array(ImageGrab.grab())

    # 将图像从RGB转换为灰度
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    # 在图像中检测人脸
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # 监测频率修改，避免刷屏幕
    delay_Detect(2)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    delay_Detect(1)

    if len(faces) == 0:
        print("No faces detected")
        # 释放摄像头并关闭所有窗口        
        cv2.destroyAllWindows()
    else:
        # 遍历每张检测到的人脸并绘制矩形
        for (x, y, w, h) in faces:
            delay_Detect(1.5)
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                # 显示图像
            cv2.imshow('img', img)
        print(f"Detected {len(faces)} faces")

    # 显示图像
    # cv2.imshow('img', img)
    

    # 按下“q”键退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头并关闭所有窗口
cv2.destroyAllWindows()

