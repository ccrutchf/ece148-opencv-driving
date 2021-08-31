import cv2
import numpy as np
from utils import imshow

white_h_low = 0
white_h_high = 60
white_s_low = 0
white_s_high = 20
white_v_low = 130
white_v_high = 160

yellow_h_low = 15
yellow_h_high = 25
yellow_s_low = 30
yellow_s_high = 120
yellow_v_low = 110
yellow_v_high = 230

class LaneDetector:
    def __init__(self):
        self._counter = 0

    def check_lane(self, frame):
        frame = frame[40:, :, :]

        blur = cv2.GaussianBlur(frame,(5,5),0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # x = 150
        # y = 20
        # print(hsv[y, x, :])
        # cv2.circle(blur, (x, y), 2, (255, 0, 255), -1)

        yellow_lower = np.array([yellow_h_low, yellow_s_low, yellow_v_low])
        yellow_upper = np.array([yellow_h_high, yellow_s_high, yellow_v_high])
        yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

        # imshow("yellow_mask", yellow_mask)
        
        return np.any(yellow_mask)

    def check_finish(self, frame, has_not_left_lane):
        frame = frame[-10:, 75:85, :]
        blur = cv2.GaussianBlur(frame,(5,5),0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # x = 400
        # y = 100
        # print(hsv[y, x, :])
        # cv2.circle(blur, (x, y), 4, (255, 0, 255), -1)

        white_lower = np.array([white_h_low, white_s_low, white_v_low])
        white_upper = np.array([white_h_high, white_s_high, white_v_high])
        white_mask = cv2.inRange(hsv, white_lower, white_upper)

        return has_not_left_lane and np.any(white_mask)

    def check_finish2(self, steering, has_not_left_lane):
        return has_not_left_lane and steering <= -0.1