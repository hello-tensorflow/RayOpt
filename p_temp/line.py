import numpy as np

class Line:
    def __init__(self, x_0, y_0, angle, length, color, thick):
        self.origin = [x_0, y_0]
        self.end = [self.origin[0] + self.length * np.cos(np.deg2rad(self.angle)), self.origin[1] + self.length * np.sin(np.deg2rad(self.angle))]
        self.length = length
        self.angle = angle
        self.color = color
        self.thickness = thick

    def check_collision(self, curve):
        return None
