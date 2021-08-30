from .driver import Driver

class JoystickDriver(Driver):
    def __init__(self, joystick):
        self.joystick = joystick

        self._throttle_scalar = 0.05

    def get_controls(self):
        steering = self.joystick.get_axis(0)
        throttle = ((self.joystick.get_axis(5) + 1) / 2) * self._throttle_scalar
        
        return (steering, throttle)
