import cv2
import numpy as np
from utils import imshow
import os

white_h_low = 105
white_h_high = 115
white_s_low = 170
white_s_high = 185
white_v_low = 200
white_v_high = 240

yellow_h_low = 15
yellow_h_high = 25
yellow_s_low = 30
yellow_s_high = 130
yellow_v_low = 110
yellow_v_high = 230

class LaneDetector:
    def __init__(self):
        self.reset()
        self._has_prev_cross = False
        self._prev_yellow_counter = 0

    def reset(self):
        self._counter = 0
        self._prev_yellow = False

    def check_lane(self, frame):
        frame = frame[40:, :, :]

        blur = cv2.GaussianBlur(frame,(5,5),0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # x = 82
        # y = 10
        # print(hsv[y, x, :])
        # cv2.circle(blur, (x, y), 2, (255, 0, 255), -1)

        yellow_lower = np.array([yellow_h_low, yellow_s_low, yellow_v_low])
        yellow_upper = np.array([yellow_h_high, yellow_s_high, yellow_v_high])
        yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

        imshow("blur_check_lane", blur)
        imshow("yellow_mask_check_lane", yellow_mask)
        
        in_lane = np.any(yellow_mask)

        if in_lane:
            self._prev_yellow_counter = 0
        else:
            self._prev_yellow_counter += 1

        actually_in_lane = self._prev_yellow_counter < 3

        if not actually_in_lane and not os.path.exists("not_in_lane.jpg"):
            print("writing lane")
            cv2.imwrite("not_in_lane.jpg", frame)

        return actually_in_lane

    def check_finish(self, frame, has_not_left_lane):
        frame = frame[30:, :, :]

        blur = cv2.GaussianBlur(frame,(5,5),0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # x = 40
        # y = 8
        # print(hsv[y, x, :])
        # cv2.circle(blur, (x, y), 4, (255, 0, 255), -1)

        white_lower = np.array([white_h_low, white_s_low, white_v_low])
        white_upper = np.array([white_h_high, white_s_high, white_v_high])
        white_mask = cv2.inRange(hsv, white_lower, white_upper)

        # imshow("blur", blur)
        # imshow("white_mask", white_mask)

        has_crossed = has_not_left_lane and np.any(white_mask)
        prev_has_prev_cross = self._has_prev_cross

        if not has_crossed:
            self._has_prev_cross = False
        else:
            self._has_prev_cross = True

        has_crossed = has_crossed and not prev_has_prev_cross

        return has_crossed

    def get_track_pos(self, frame):
        frame = frame[80:90, :, :]

        blur = cv2.GaussianBlur(frame,(5,5),0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # x = 150
        # y = 20
        # print(hsv[y, x, :])
        # cv2.circle(blur, (x, y), 2, (255, 0, 255), -1)

        yellow_lower = np.array([yellow_h_low, yellow_s_low, yellow_v_low])
        yellow_upper = np.array([yellow_h_high, yellow_s_high, yellow_v_high])
        yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

        has_mask = np.any(yellow_mask)

        if not has_mask:
            self._prev_yellow = False

        if has_mask and not self._prev_yellow:
            self._prev_yellow = True
            self._counter += 1

        # imshow("yellow_mask", yellow_mask)

        return self._counter
