import cv2
import numpy as np
from utils import imshow

white_h_low = 0
white_h_high = 60
white_s_low = 0
white_s_high = 20
white_v_low = 130
white_v_high = 160

yellow_h_low = 20
yellow_h_high = 25
yellow_s_low = 30
yellow_s_high = 120
yellow_v_low = 190
yellow_v_high = 230

class LaneDetector:
    def check_lane(self, frame):
        frame = frame[24:, :, :]

        blur = cv2.GaussianBlur(frame,(5,5),0)
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

        # x = 8
        # y = 60
        # print(hsv[y, x, :])
        # cv2.circle(blur, (x, y), 2, (255, 0, 255), -1)

        yellow_lower = np.array([yellow_h_low, yellow_s_low, yellow_v_low])
        yellow_upper = np.array([yellow_h_high, yellow_s_high, yellow_v_high])
        yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

        white_lower = np.array([white_h_low, white_s_low, white_v_low])
        white_upper = np.array([white_h_high, white_s_high, white_v_high])
        white_mask = cv2.inRange(hsv, white_lower, white_upper)

        if np.any(yellow_mask):
            return True

        element = cv2.getStructuringElement(
            cv2.MORPH_ELLIPSE, (6, 6)
        )
        white_dilated = cv2.dilate(white_mask, element)
        yellow_dilated = cv2.dilate(yellow_mask, element)

        white_dilated[yellow_dilated == 255] = 0

        contours, hierarchy = cv2.findContours(white_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        for i, _ in enumerate(contours):
            cv2.drawContours(blur, contours, i, (0,255,0), 3)

        rectangles = [cv2.boundingRect(c) for c in contours]
        centroids_with_area = [((int(x + w/2), int(y + h/2)), w * h) for x, y, w, h in rectangles]
        centroids_with_area.sort(key=lambda x: x[1], reverse=True)
        centroids = [c for c, _ in centroids_with_area]

        for cent in centroids:
            cv2.circle(blur, cent, 4, (255, 0, 0), -1)

        imshow("blur", blur)
        imshow("white_dilated", white_dilated)
        imshow("yellow_dilated", yellow_dilated)

        if len(centroids) < 2:
            return False

        centroids = centroids[:2]
        centroids.sort(key=lambda x: x[0])

        x_right, _ = centroids[0]
        x_left, _ = centroids[1]

        return x_right <= 80 and x_left >= 80
