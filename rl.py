from adafruit_servokit import ServoKit
import pygame
import os
import cv2
from utils import clamp
import time

from drivers.joystick_driver import JoystickDriver
from writers.file_writer import FileWriter

should_display = "DISPLAY" in os.environ and False

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
recording_freq = 15
recording_duration = 1 / recording_freq

# joystick constants
joystick_throttle_scalar = 0.05

def imshow(title, img):
    if should_display:
        cv2.imshow(title, img)

driver = JoystickDriver(joystick)
writer = FileWriter()

print("starting...")

while True:
    start_time = time.time()
    ret, frame = vid.read()

    if not ret:
        break

    pygame.event.pump()

    scale = cv2.resize(frame, (160, 120))

    imshow("scale", scale)

    steering, throttle = driver.get_controls()
    writer.write(steering, throttle, scale)

    kit.servo[1].angle = clamp(steering + 90 + steering_offset, 0, 180)
    kit.continuous_servo[2].throttle = throttle

    if should_display and cv2.waitKey(25) & 0xFF == ord("q"):
        kit.continuous_servo[2].throttle = 0.0
        break

    end_time = time.time()

    duration = end_time - start_time
    if duration < recording_duration:
        time.sleep(recording_duration - duration)
    else:
        print("warning, time exceeded")

if should_display:
    cv2.destroyAllWindows() 