import numpy as np
from line import Line

class Light_Source(Line):
    def __init__(self, x_0, y_0, angle, length, color, thick, num_rays):
        super().__init__(self, x_0, y_0, angle, length, color, thick)
        self.num_rays = num_rays
        self.angles = np.linspace(0,360-360/num_rays,num_rays)
        self.rays = [Line(x_0, y_0, angle, length, color, thick) for angle in self.angles]

    
