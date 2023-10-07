class Mirror:
    def __init__(self, a, c, right_lim):
        self.a = a
        self.c = c
        self.right_lim = right_lim
    
    def eq_param(self, t):
        y_1 = -t
        y_2 = t
        x = self.a*pow(t,2) + self.c

        return x, y_1, y_2
