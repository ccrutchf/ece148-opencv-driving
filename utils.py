import os
import cv2

should_display = "DISPLAY" in os.environ and False

def imshow(title, img):
    if should_display:
        cv2.imshow(title, img)

def clamp(value, min, max):
    if value < min:
        return min
    if value > max:
        return max

    return value