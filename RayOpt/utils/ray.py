import numpy as np


class Ray:
    def __init__(self, x_0, y_0, angle, color, thick):
        self.origin = [x_0, y_0]
        self.angle = np.deg2rad(angle)
        self.dir = np.array([np.cos(self.angle), np.sin(self.angle)])
        self.k = None
        self.b = None
        self.t = None
        self.norm = None
        self.reflected = None
        self.collisions = [self.origin]
        self.color = color
        self.thickness = thick

    def calc_params(self):
        self.k = self.dir[1]/self.dir[0]
        self.b = self.origin[1] - self.k * self.origin[0]
    
    def find_collision(self, mirror):
        discriminant = np.sqrt(1-4*mirror.a*self.k*(self.k*mirror.c+self.b))
        self.t = (1+np.sign(self.dir[0])*discriminant)/(2*mirror.a*self.k)
        x_col, _, y_col = mirror.eq_param(self.t)
        self.collisions.append([x_col, y_col])
    
    def find_norm(self, mirror):
        normalization = np.sqrt(1+4*pow(mirror.a, 2)*pow(self.t, 2))
        n_y = -(2*mirror.a*self.t)/normalization
        n_x = 1/normalization
        self.norm = np.array([n_x, n_y])
    
    def find_reflection(self):
        self.reflected = self.dir-2*np.dot(self.dir, self.norm)*self.norm

    def screen_collision(self, screen_position):
        return self.k * screen_position + self.b

    def propagate(self, mirror, screen_position):
        while True:
            self.calc_params()
            if self.k != 0:
                self.find_collision(mirror)
                self.find_norm(mirror)
                self.find_reflection()
                self.origin = self.collisions[-1]
                self.dir = self.reflected
                if self.collisions[-1][0] > mirror.right_lim:
                    collide_pos = self.screen_collision(screen_position)
                    self.collisions.append([screen_position, collide_pos])
                    break
            else:
                collide_pos = self.screen_collision(screen_position)
                self.collisions.append([screen_position, collide_pos])
                break



class Light_Source:
    def __init__(self, x_0, y_0, color, thick, num_rays):
        self.num_rays = num_rays
        self.angles = np.linspace(0, 360-360/num_rays, num_rays)
        self.rays = [Ray(x_0, y_0, angle, color, thick) for angle in self.angles]
        self.color = color
        self.thickness = thick
        self.origin = [x_0, y_0]
