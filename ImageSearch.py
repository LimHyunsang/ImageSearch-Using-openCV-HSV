import keyboard
from PIL import ImageGrab
import numpy as np
import cv2


def LiveCapture():
    pos = (685, 389, 924, 446)  # 캡처 범위
    img = ImageGrab.grab(pos)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv_low = np.array([0, 0, 0], np.uint8)
    hsv_high = np.array([179, 255, 255], np.uint8)
    mask = cv2.inRange(img, hsv_low, hsv_high)
    img = cv2.bitwise_and(img, img, mask=mask)
    img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    return img


def TargetImg(img_link):
    template = cv2.imread(img_link, cv2.IMREAD_UNCHANGED)
    template = cv2.cvtColor(template, cv2.COLOR_RGB2HSV)
    hsv_low = np.array([0, 0, 0], np.uint8)
    hsv_high = np.array([179, 255, 255], np.uint8)
    mask = cv2.inRange(template, hsv_low, hsv_high)
    template = cv2.bitwise_and(template, template, mask=mask)
    template = cv2.cvtColor(template, cv2.COLOR_HSV2BGR)
    return template


def check(event):
    img = LiveCapture()
    template = TargetImg("imglink")
    result = cv2.matchTemplate(template, img, cv2.TM_CCOEFF_NORMED)
    threshold = 0.90  # 오차범위
    box_loc = np.where(result >= threshold)  # 오차범위 이상의 값 반환
    if box_loc[0].size > 0:
        print("찾음")


keyboard.on_press_key("0", check)  # 키보드 0번 키 누르면 작동
keyboard.wait("esc")
