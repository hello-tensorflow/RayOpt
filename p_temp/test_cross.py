import numpy as np
import scipy.optimize

def MyFunction(z):
    x = z[0]
    y = z[1]

    F = np.empty((2))
    F[0] = pow(x,2) + 2*x*y + pow(y,2) + 2*x + 2*y + 1
    F[1] = np.tan(np.deg2rad(45))*x - 1 - y

    return F

zGuess = np.array([10,10])

z = scipy.optimize.fsolve(MyFunction, zGuess)

print(z)

params = [1,2,3,4,5,6]

matrix = [[params[0], 0.5*params[2], 0.5*params[3]], 
                [0.5*params[2], params[1], 0.5*params[4]],
                [0.5*params[3], 0.5*params[4], params[5]]]

vec = np.array([1,2,3])
print(vec)
#vec = vec.T
print(matrix)
print(vec)
print(vec.T.dot(matrix)*vec.T)