from utils.ray import Light_Source
from utils.mirror import Mirror
import numpy as np
from scipy.stats import kstest


def fitness_function(arr):
    ksstat, p_value = kstest(np.array(arr), "norm", args=(0, 0.2))
    return ksstat, p_value


class Experiment:
    def __init__(self, num_rays, a, c, mirror_right_lim, screen_position):
        self.light_source = Light_Source(0, 0, 'blue', 0.5, num_rays)
        self.mirror = Mirror(a, c, mirror_right_lim)
        self.screen_position = screen_position
        self.all_colls = []
        self.screen_colls = []
        self.fitness = None

    def run_experiment(self):
        for ray in self.light_source.rays:
            ray.propagate(self.mirror, self.screen_position)
            self.all_colls.append(ray.collisions)

        for ray in self.all_colls:
            self.screen_colls.append(ray[-1][1])

    def evaluate(self, fit_func):
        res = fit_func(self.screen_colls)
        self.fitness = res[0]


def main():
    experiment = Experiment(1440, 10, -1, 0.2, 2)
    experiment.run_experiment()
    experiment.evaluate(fitness_function)
    print(experiment.fitness)


if __name__=='__main__':
    main()
