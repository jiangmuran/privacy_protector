import cv2
import pyautogui

# Hash值对比

import win32gui, win32ui, win32con, win32api
import cv2
import numpy as np

print("欢迎进入隐私保护者v1.0，本项目由姜睦然原创。")
print("note:程序闪退是配置错误导致的，请尝试修改配置内容，切记不能出现非数字。")
print("热键指南：")
print("重置辨别器（出现问题时使用）：u")
print("提高匹配度：j")
print("降低匹配度：n")
print("------------------------------------")
print("进入配置阶段")
xjixhxh=int(input("请输入摄像头id并按下enter（如果不知道请输入0，出现问题请尝试递增）："))
print("正在配置摄像头，请稍等，如果闪退请尝试将id增加1并检查摄像头是否链接。")
sht=cv2.VideoCapture(xjixhxh)
biao=0.96

def window_capture():
    ret,frame=sht.read()
    return frame


def cmpHash(hash1, hash2,shape=(10,10)):
    n = 0
    # hash长度不同则返回-1代表传参出错
    if len(hash1)!=len(hash2):
        return -1
    # 遍历判断
    for i in range(len(hash1)):
        # 相等则n计数+1，n最终为相似度
        if hash1[i] == hash2[i]:
            n = n + 1
    return n/(shape[0]*shape[1])
# 均值哈希算法
def aHash(img,shape=(10,10)):
    # 缩放为10*10
    img = cv2.resize(img, shape)
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # s为像素和初值为0，hash_str为hash值初值为''
    s = 0
    hash_str = ''
    # 遍历累加求像素和
    for i in range(shape[0]):
        for j in range(shape[1]):
            s = s + gray[i, j]
    # 求平均灰度
    avg = s / 100
    # 灰度大于平均值为1相反为0生成图片的hash值
    for i in range(shape[0]):
        for j in range(shape[1]):
            if gray[i, j] > avg:
                hash_str = hash_str + '1'
            else:
                hash_str = hash_str + '0'
    return hash_str

import ctypes, sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False



keymode=0
listss=[["win","m"],["win","m"],["ctrl","win","left"],["volumeup"],-1]
print("请问在检测到可能泄密时按下的按键是：")
print("1. Windows+M （windows下强制回到桌面，建议新手选择）")
print("2. Control+Windows+Left （windows10下回到前一个桌面，需要提前配置）")
print("3. VolumeUP （音量上升，仅供测试）")
print("5. 自定义")
print("----------------------------------------------------------------------------")
keymode=listss[int(input("你的选择："))]
if (keymode==-1):
    print("格式：将按键名以空格为分割填写，直接按下enter以查看列表")
    keymode=input("请输入：").split(' ')

    if(keymode==['']):
        print(",".join(pyautogui.KEY_NAMES))
        input("请输入：").split(' ')
print("配置已经修改完成，请将弹出的窗口放置到右下角并置顶。")

if __name__ == '__main__':

    yuanshi = window_capture()
    cv2.namedWindow("CCimage",0)
    cv2.namedWindow("CCimage2",0)
    #win32gui.SetForegroundWindow(win32gui.FindWindow(None, "CCimage"))
    #win32gui.SetForegroundWindow(win32gui.FindWindow(None, "CCimage2"))
    while True:
        # 从摄像头中按帧返回图片
        frame = window_capture()

        hash=cmpHash(aHash(frame),aHash(yuanshi))
        if (hash <= biao):
            frame=cv2.putText(frame,str(int(hash*100))+"%",(50,100),cv2.FONT_HERSHEY_SIMPLEX,3,(0,0,255),thickness=4)
        else:
            frame = cv2.putText(frame, str(int(hash*100))+"%", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 255, 0), thickness=4)

        frame = cv2.putText(frame, str(int(biao*100))+"%", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), thickness=4)


        cv2.imshow('CCimage',frame) # 显示图片
        cv2.imshow('CCimage2', frame)  # 显示图片





        if (hash <= biao):
            pyautogui.hotkey(keymode)
            print("change!")
            yuanshi = window_capture()
        key = cv2.waitKey(10)
        if key == ord('q'): # 输入q退出读取
            break
        if key == ord('u'):
            yuanshi = window_capture()
            print("Update done.")
        if key == ord('j'):
            if (biao <= 0.98):
                biao+=0.01
        if key == ord('n'):
            if (biao >=0):
                biao-=0.01
    cv2.destroyAllWindows()