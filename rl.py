from adafruit_servokit import ServoKit
import pygame
import os

# init joystick
os.putenv('SDL_VIDEODRIVER', 'dummy')
pygame.display.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

# init servos
kit = ServoKit(channels=16)

# constants
steering_offset = 18

# joystick constants
joystick_throttle_scalar = 0.05

def clamp(value, min, max):
    if value < min:
        return min
    if value > max:
        return max

    return value

while True:
    pygame.event.pump()

    kit.servo[1].angle = clamp(90 * joystick.get_axis(0) + 90 + steering_offset, 0, 180)
    kit.continuous_servo[2].throttle = ((joystick.get_axis(5) + 1) / 2) * joystick_throttle_scalar