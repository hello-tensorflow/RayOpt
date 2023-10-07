import numpy as np
import scipy.optimize
from matplotlib import pyplot as plt
import sympy

class Ray:
    def __init__(self, x_0, y_0, angle, t, color, thick):
        self.origin = [x_0, y_0]
        self.angle = np.deg2rad(angle)
        self.t = t
        self.dir = [np.cos(self.angle), np.sin(self.angle)]
        self.k = None
        self.b = None
        self.end = None
        self.collisions = [self.origin]
        self.color = color
        self.thickness = thick

    def calc_params(self):
        self.k = self.dir[1]/self.dir[0]
        self.b = self.origin[1] - self.k * self.origin[0]
        self.end = [self.origin[0] + self.dir[0] * self.t, self.origin[1] + self.dir[1] * self.t]


    def find_y(self, x):
        return self.k*x+self.b
    
    def parametric(self, t):
        self.t = t
        return self.end
    
    def find_collision(self, mirror):
        discriminant = np.sqrt(pow(self.dir[0],2)-4*mirror.a*(mirror.c-self.origin[0]))
        t_1 = (self.dir[0]+discriminant)/(2*mirror.a)
        t_2 = (self.dir[1]-discriminant)/(2*mirror.a)
        t_3 = self.origin[0]/(1+self.dir[0])
        x_col = self.origin[0] + t_1*self.dir[0]
        y_col = self.origin[1] + t_1*self.dir[1]
        return x_col, y_col
    
    def find_collision_2(self, mirror):
        discriminant = np.sqrt(1-4*mirror.a*self.k*(self.k*mirror.c+self.b))
        t = (1+np.sign(self.dir[0])*discriminant)/(2*mirror.a*self.k)
        #t_1 = (1+discriminant)/(2*mirror.a*self.k)
        #t_2 = (1-discriminant)/(2*mirror.a*self.k)
        x_col, _, y_col = mirror.eq_param(t)
        return x_col, y_col, t
    
    def find_tan(self, mirror):
        x, y, t = self.find_collision_2(mirror)
        norm = np.sqrt(1+4*pow(mirror.a, 2)*pow(t, 2))
        t_x = (2*mirror.a*t)/norm
        t_y = 1/norm
        return t_x, t_y, x, y
    
    def find_norm(self,mirror):
        t_x, t_y, x, y = self.find_tan(mirror)
        n_x = t_y
        n_y = -t_x
        return n_x, n_y, x, y
    
    def find_reflection(self, mirror):
        n_x, n_y, x, y = self.find_norm(mirror)
        v = np.array(self.dir)
        n = np.array([n_x, n_y])
        r = v-2*np.dot(v, n)*n
        return r, x, y
    
    def screen_collision(self, screen):
        x1 = screen.origin[0]
        y1 = screen.origin[1]
        x2 = screen.end[0] 
        y2 = screen.end[1]

        x3 = self.origin[0]
        y3 = self.origin[1]
        x4 = self.dir[0]
        y4 = self.dir[1]

        # Using line-line intersection formula to get intersection point of ray and wall
        # Where (x1, y1), (x2, y2) are the ray pos and (x3, y3), (x4, y4) are the wall pos
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        enumerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        if denominator == 0:
            return None

        t = enumerator / denominator
        u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / denominator

        if 1 >= t > 0 and u > 0:
            x = x1 + t * (x2 - x1)
            y = y1 + t * (y2 - y1)
            collide_pos = [x, y]
            return collide_pos

    def propagate(self, mirror, screen):
        while True:
            self.calc_params()
            r, x, y = self.find_reflection(mirror)
            self.collisions.append([x, y])
            self.origin = [x, y]
            self.dir = [r[0], r[1]]
            self.k = self.dir[1]/self.dir[0]
            self.b = self.origin[1] - self.k * self.origin[0]
            if x > 1:
                collide_pos = self.screen_collision(screen)
                self.collisions.append(collide_pos)
                screen.collisions.append(collide_pos[1])
                break
            

class Screen:
    def __init__(self, x, y, angle, length):
        self.origin = [x, y]
        self.angle = angle
        self.length = length
        self.end = [self.origin[0]+self.length*np.cos(np.deg2rad(self.angle)), 
                    self.origin[1]+self.length*np.sin(np.deg2rad(self.angle))]
        self.collisions = []
    
    
class Mirror:
    def __init__(self, params, a, c):
        self.matrix = [[params[0], 0.5*params[2], 0.5*params[3]], 
                       [0.5*params[2], params[1], 0.5*params[4]],
                       [0.5*params[3], 0.5*params[4], params[5]]]
        self.params = params
        self.a = a
        self.c = c


    # def equation(self, x, y):
    #     vec = np.array([x, y, 1])
    #     return vec.T.dot(self.matrix)*vec
    def equation_implicit(self, x,y):
        eq = self.params[0]*pow(x,2) + self.params[1]*pow(y,2) + self.params[2]*(x*y) + self.params[3] * x + self.params[4] * y + self.params[5]
        mat = [[0, -1], [0, 1]]
        return np.dot(mat, [])
    
    def eq_param(self, t):
        y_1 = -t
        y_2 = t
        x = self.a*pow(t,2) + self.c

        return x, y_1, y_2
    

def plotter_parametric(ray, mirror):
    plt.figure(figsize=(10,10))
    plt.axis([-1.1, 1.1, -1.1, 1.1])
    res = ray.find_collision_2(mirror)
    #print(res[0], res[1], res[2])
    plt.plot([ray.origin[0], res[0]], [ray.origin[1], res[1]], ray.color, linewidth=ray.thickness)
    t_x, t_y, x, y = ray.find_tan(mirror)
    
    plt.plot([x, x+t_x], [y, y+t_y], 'green', linewidth=1)
    plt.plot([x, x-t_x], [y, y-t_y], 'green', linewidth=1)
    n_x, n_y, x, y = ray.find_norm(mirror)
    plt.plot([x, x+n_x], [y, y+n_y], 'green', linewidth=1)
    r, x, y = ray.find_reflection(mirror)
    plt.plot([x, x+r[0]], [y, y+r[1]], 'purple', linewidth=1)
    #plt.plot([x, x-n_x], [y, y-n_y], 'red', linewidth=2)
    t = np.linspace(0,10,1000)
    plt.plot(mirror.eq_param(t)[0], mirror.eq_param(t)[2], 'blue')
    plt.plot(mirror.eq_param(t)[0], mirror.eq_param(t)[1], 'red')

    plt.savefig('ray_mirror.png', dpi = 300)


def plotter_implicit(ray, mirror):
    # plt.figure(figsize=(10,10))
    # plt.axis([-1, 2.1, -1.1, 1.1])
    # plt.plot([ray.origin[0], ray.end[0]], [ray.origin[1], ray.end[1]], ray.color, linewidth=ray.thickness)
    # delta = 0.025
    # xrange = np.arange(-5.0, 20.0, delta)
    # yrange = np.arange(-5.0, 20.0, delta)
    # x, y = np.meshgrid(xrange, yrange)
    # equation = mirror.equation(x, y)
    # print(equation)
    # plt.contour(x, y, equation, [0])
    # plt.savefig('ray_mirror.png', dpi = 300)

    fig = plt.figure()
    axis = fig.add_subplot(1,1,1)

    x, y = np.mgrid[-2: 2: 4001j, -2: 2: 4001j]

    axis.set_title('Ellipse')
    axis.set_xlabel(r'$x$', fontsize=20, fontname='serif')
    axis.set_ylabel(r'$y$', fontsize=20, fontname='serif')
    axis.tick_params(axis='both', length=10, which='major')
    axis.tick_params(axis='both', length=5,  which='minor')
    axis.minorticks_on()
    axis.set_aspect('equal', 'box')
    axis.set(xlim=(-2, 2), ylim=(-2, 2))
    def func(x,y):
        return x**2+y**2
    axis.contour(x, y, mirror.equation(x,y), [1])

    plt.show()
    fig.savefig('plot.png', transparent=False)



def main():
    plt.figure(figsize=(10,10))
    plt.axis([-1.1, 2.1, -1.1, 1.1])
    angles = np.linspace(1,2,2)
    pars = [1,0,0,0.5,1,1]
    mirror = Mirror(pars, 5, -1)
    screen = Screen(2, -10, 90, 20)
    for angle in angles:
        ray = Ray(0,0, angle, 100, 'blue', 0.5)
        
        
        #plotter_parametric(ray, mirror)
        ray.propagate(mirror, screen)
        res = np.array(ray.collisions).T
        plt.plot(res[0], res[1], ray.color, linewidth=ray.thickness)

    t = np.linspace(0,np.sqrt(2)/np.sqrt(5),1000)
    plt.plot(mirror.eq_param(t)[0], mirror.eq_param(t)[2], 'blue')
    plt.plot(mirror.eq_param(t)[0], mirror.eq_param(t)[1], 'red')
    plt.plot([screen.origin[0], screen.end[0]], [screen.origin[1], screen.end[1]], 'black', linewidth=10)
    plt.savefig('reflections.png', dpi = 300)
    print(screen.collisions)


if __name__=='__main__':
    main()