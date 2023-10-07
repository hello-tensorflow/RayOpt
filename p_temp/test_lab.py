from sympy import plot_implicit, symbols, Eq, And
from matplotlib import pyplot as plt
import numpy as np

# # plt.rcParams['figure.figsize'] = 10, 10
# # plt.axis([-1, 2.1, -1.1, 1.1])
# x, y = symbols('x y')
# pars = [1,0,0,2,2,2]
# def equation(x,y, params):
#     return params[0]*pow(x,2) + params[1]*pow(y,2) + params[2]*(x*y) + params[3] * x + params[4] * y + params[5]
# graph = plot_implicit(Eq(equation(x,y,pars), 0), x_var=('x', -1,2.1), y_var=('y',-1.1, 1.1))
# #p2 = plot_implicit(Eq(x**2 + y**2, 1), x_var=('x', -1,2.1), y_var=('y',-1.1, 1.1))

# graph.save('fig.png')



##############################################################################################

# import numpy as np
# import matplotlib.pyplot as plt

# fig = plt.figure()
# axis = fig.add_subplot(1,1,1)

# x, y = np.mgrid[-2: 2: 4001j, -2: 2: 4001j]

# axis.set_title('Ellipse')
# axis.set_xlabel(r'$x$', fontsize=20, fontname='serif')
# axis.set_ylabel(r'$y$', fontsize=20, fontname='serif')
# axis.tick_params(axis='both', length=10, which='major')
# axis.tick_params(axis='both', length=5,  which='minor')
# axis.minorticks_on()
# axis.set_aspect('equal', 'box')
# axis.set(xlim=(-2, 2), ylim=(-2, 2))

# axis.contour(x, y, x**2 - 2*x*y + 2*y**2, [1])

# plt.show()
# fig.savefig('plot.png', transparent=False)

# a = 1
# # x = a*pow(t,2)
# # y = -t

# t = np.linspace(0,1,50)

# plt.plot(a*pow(t,2)-1, t, 'blue')
# plt.plot(a*pow(t,2)-1, -t, 'blue')
# plt.plot(pow(t,2), t, 'red')
# plt.plot(pow(t,2), -t, 'red')
# plt.savefig('par.png')


##############################################################################

a = [0, 90, 180, 270, 315]
b = [0,-45, -90, -180, -270]
def func(x):
    return np.sign(np.cos(np.deg2rad(x)))

print(list(map(func, a)))
print(list(map(func, b)))