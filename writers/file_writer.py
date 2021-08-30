import os
import cv2
from .writer import Writer

class FileWriter(Writer):
    def __init__(self):
        if not os.path.exists("data"):
            os.mkdir("data")

        if os.path.exists("data/inputs.csv"):
            with open("data/inputs.csv", "r") as f:
                lines = [l for l in f.readlines() if l]
                if lines:
                    self._index = int(lines[-1].split(",")[0])
                else:
                    self._index = 0
        else:
            self._index = 0

        self._inputs = open("data/inputs.csv", "a" if os.path.exists("data/inputs.csv") else "w")

    def __del__(self):
        self._inputs.close()

    def write(self, steering, throttle, frame):
        if throttle:
            self._inputs.write("{index}, {steering}, {throttle}\n".format(index=self._index,steering=steering, throttle=throttle))
            cv2.imwrite("data/{index}.jpg".format(index=self._index), frame)

            self._index += 1