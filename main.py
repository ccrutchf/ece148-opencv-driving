from adafruit_servokit import ServoKit
import cv2
import numpy as np
import os

should_display = "DISPLAY" in os.environ and True

white_h_low = 0
white_h_high = 35
white_s_low = 0
white_s_high = 15
white_v_low = 210
white_v_high = 240

yellow_h_low = 20
yellow_h_high = 25
yellow_s_low = 30
yellow_s_high = 120
yellow_v_low = 190
yellow_v_high = 230

steering_scalar = 0.12
min_steering = -90
max_steering = 90

def imshow(title, img):
    if should_display:
        cv2.imshow(title, img)

def clamp(val, min_val, max_val):
    if val >= min_val and val <= max_val:
        return val
    
    if val < min_val:
        return min_val
    
    if val > max_val:
        return max_val

def slider_to_image(val):
    return int((val / 2000) * 255)

def get_steering_white(frame):
    middle = frame[200:399,:,:]
    blur = cv2.GaussianBlur(middle,(5,5),0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # x = 400
    # y = 100
    # print(hsv[y, x, :])
    # cv2.circle(blur, (x, y), 4, (255, 0, 255), -1)

    yellow_lower = np.array([yellow_h_low, yellow_s_low, yellow_v_low])
    yellow_upper = np.array([yellow_h_high, yellow_s_high, yellow_v_high])
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

    white_lower = np.array([white_h_low, white_s_low, white_v_low])
    white_upper = np.array([white_h_high, white_s_high, white_v_high])
    white_mask = cv2.inRange(hsv, white_lower, white_upper)

    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (20, 20)
    )
    white_dilated = cv2.dilate(white_mask, element)
    yellow_dilated = cv2.dilate(yellow_mask, element)

    white_dilated[yellow_dilated == 255] = 0

    contours, hierarchy = cv2.findContours(white_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i, _ in enumerate(contours):
        cv2.drawContours(blur, contours, i, (0,255,0), 3)

    rectangles = [cv2.boundingRect(c) for c in contours]
    centroids = [(int(x + w/2), int(y + h/2)) for x, y, w, h in rectangles]
        
    y_center = 100
        
    if len(centroids) == 1:
        x, _ = centroids[0]

        if x <= 400:
            centroids.insert(0, (800, y_center))
        else:
            centroids.append((0, y_center))

    for cent in centroids:
       cv2.circle(blur, cent, 4, (255, 0, 0), -1)

    # imshow("blur", blur)
    # imshow("white_dilated", white_dilated)
    # imshow("yellow_dilated", yellow_dilated)

    if not centroids:
        return 0

    x_right, _ = centroids[0]
    x_left, _ = centroids[1]

    x_center = int((x_right - x_left) / 2 + x_left)

    cv2.circle(blur, (x_center, y_center), 4, (0, 0, 255), -1)
    imshow("blur", blur)

    return clamp(int((x_center - 400) * steering_scalar), min_steering, max_steering)

def get_steering_yellow(frame):
    middle = frame[200:399,:,:]
    blur = cv2.GaussianBlur(middle,(5,5),0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    # x = 400
    # y = 100
    # print(hsv[y, x, :])
    # cv2.circle(blur, (x, y), 4, (255, 0, 255), -1)

    yellow_lower = np.array([yellow_h_low, yellow_s_low, yellow_v_low])
    yellow_upper = np.array([yellow_h_high, yellow_s_high, yellow_v_high])
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)

    white_lower = np.array([white_h_low, white_s_low, white_v_low])
    white_upper = np.array([white_h_high, white_s_high, white_v_high])
    white_mask = cv2.inRange(hsv, white_lower, white_upper)

    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (20, 20)
    )
    white_dilated = cv2.dilate(white_mask, element)
    yellow_dilated = cv2.dilate(yellow_mask, element)

    yellow_dilated[white_dilated == 255] = 0
    # white_dilated[yellow_dilated == 255] = 0

    contours, hierarchy = cv2.findContours(yellow_dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i, _ in enumerate(contours):
        cv2.drawContours(blur, contours, i, (0,255,0), 3)

    rectangles = [cv2.boundingRect(c) for c in contours]
    centroids_with_area = [((int(x + w/2), int(y + h/2)), w * h) for x, y, w, h in rectangles]
    centroids_with_area.sort(key=lambda x: x[1], reverse=True)
    centroids = [c for c, _ in centroids_with_area]
        
    y_center = 100

    for cent in centroids:
       cv2.circle(blur, cent, 4, (255, 0, 0), -1)

    imshow("blur", blur)
    imshow("white_dilated", white_dilated)
    imshow("yellow_dilated", yellow_dilated)

    if not centroids:
        return None

    x_center, _ = centroids[0]

    cv2.circle(blur, (x_center, y_center), 4, (0, 0, 255), -1)
    imshow("blur", blur)

    return clamp(int((x_center - 400) * steering_scalar), -90, 90)

def thresh(steering):
    if abs(steering) > 30:
        return 0
    return steering

def main():
    vid = cv2.VideoCapture(0)
    kit = ServoKit(channels=16)

    steering = 0
    while True:
        ret, frame = vid.read()

        if not ret:
            break

        prev_steering = steering
        steering = get_steering_yellow(frame)

        if steering is None:
            # print("using white")
            # steering = get_steering_white(frame)

            print("using prev")
            steering = thresh(prev_steering)

        print(steering)

        kit.servo[1].angle = clamp(steering + 95, 0, 180)
        kit.continuous_servo[2].throttle = 0.2

        # imshow("frame", frame)
        if should_display and cv2.waitKey(25) & 0xFF == ord("q"):
            kit.continuous_servo[2].throttle = 0.0
            break

    if should_display:
        cv2.destroyAllWindows() 

if __name__ == "__main__":
    main()
