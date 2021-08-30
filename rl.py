from adafruit_servokit import ServoKit
import pygame
import os
import cv2
from utils import clamp

from drivers.joystick_driver import JoystickDriver

should_display = "DISPLAY" in os.environ and True

# init joystick
os.putenv('SDL_VIDEODRIVER', 'dummy')
pygame.display.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# init servos
kit = ServoKit(channels=16)

# init camera
vid = cv2.VideoCapture(0)

# constants
steering_offset = 18

# joystick constants
joystick_throttle_scalar = 0.05

def imshow(title, img):
    if should_display:
        cv2.imshow(title, img)

driver = JoystickDriver(joystick)

while True:
    ret, frame = vid.read()

    if not ret:
        break

    pygame.event.pump()
    print("running")

    # imshow("frame", frame)

    steering, throttle = driver.get_controls()

    kit.servo[1].angle = clamp(steering + 90 + steering_offset, 0, 180)
    kit.continuous_servo[2].throttle = throttle

    if should_display and cv2.waitKey(25) & 0xFF == ord("q"):
        kit.continuous_servo[2].throttle = 0.0
        break

if should_display:
    cv2.destroyAllWindows() 