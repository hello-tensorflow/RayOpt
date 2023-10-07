from experiment_2 import Experiment
from utils.plotter import plotter
import numpy as np
from scipy.stats import kstest, anderson, norm
import random


# def fitness_function(arr, statistic):
#     if statistic == 'KS':
#         ksstat, p_value = kstest(np.array(arr), "norm", args=(0, 0.2))
#         res = [ksstat, p_value]
#     #fitness = np.abs(ksstat-0.5)
#     elif statistic == 'Anderson':
#         andtest = anderson(arr)
#         res = [andtest.fit_result.params[1]-0.2, andtest.fit_result.params[0]]

#     return res


class RayOpt:
    def __init__(self, settings):
        self.pop_size = settings['pop_size']
        self.num_genes = settings['num_genes']
        self.epochs = settings['epochs']
        self.selection_ratio = settings['selection_ratio']
        self.mutation_prob = settings['mutation_prob']
        self.num_rays = settings['num_rays']
        self.mirror_right_lim = settings['mirror_right_lim']
        self.screen_position = settings['screen_position']
        self.population = []
        self.best_fitness = 10000000000000
        self.best_ind = None
        self.threshold = settings['threshold']

    def generate_init_pop(self):
        for _ in range(self.pop_size):
            a = random.uniform(0, 1000)
            c = random.uniform(-1, 0)
            self.population.append(Experiment(self.num_rays, a, c, self.mirror_right_lim, self.screen_position))

    def fitness_function(self, arr):
        # arr = np.histogram(arr, bins='auto', density=True)
        # print(arr)
        ksstat, p_value = kstest(arr, "norm", args=(0, 0.2))
        res = [ksstat, p_value]
        #andtest = anderson(arr)
        #res = [andtest.fit_result.params[1]-0.2, andtest.fit_result.params[0]]
        
        # ind = np.histogram(screen_colls, bins=100, density=True)
        # print(ind)

        # print(len(ind), len(ind[0]), len(ind[1]))
        # x_axis = np.arange(-2, 2, 0.001)
        # arr = norm.pdf(x_axis, 0, 0.2)
        # print(arr)

        return res
    
    def evaluate(self):
        for ind in self.population:
            ind.run_experiment()
            ind.evaluate(self.fitness_function)

    def sort_by_fit_func(self):
        self.population = sorted(self.population, key=lambda ind: ind.fitness)

    def select_best(self, epoch):
        self.population = self.population[:int(len(self.population) * self.selection_ratio)]
        if self.population[0].fitness < self.best_fitness:
            self.best_fitness = self.population[0].fitness
            self.best_ind = self.population[0]
            plotter(self.mirror_right_lim, 
                        self.best_ind.mirror, 
                        self.best_ind.all_colls, 
                        self.best_ind.light_source, 
                        self.best_ind.screen_position, 
                        epoch)
    
    def cross_section(self):
        temp_pop = []
        random.shuffle(self.population)

        while len(temp_pop) < self.pop_size:
            parent_1, parent_2 = random.sample(self.population, 2)
            a_1 = parent_1.mirror.a
            a_2 = parent_2.mirror.a
            c_1 = parent_1.mirror.c
            c_2 = parent_2.mirror.c
            child_1 = Experiment(self.num_rays, a_1, c_2, self.mirror_right_lim, self.screen_position)
            child_2 = Experiment(self.num_rays, a_2, c_1, self.mirror_right_lim, self.screen_position)
            temp_pop.append(child_1)
            temp_pop.append(child_2)
        self.population = temp_pop

    def mutation(self):
        for ind in self.population:
            if random.uniform(0,1) < self.mutation_prob:
                if random.randint(0,1) == 1:
                    ind.mirror.a = random.uniform(0, 1000)
                else:
                    ind.mirror.c = random.uniform(-1, 0)

    def optimize(self):
        self.generate_init_pop()
        for epoch in range(self.epochs):
            self.evaluate()
            self.sort_by_fit_func()
            self.select_best(epoch)
            print('Epoch: {}; Best individual: {}'.format(epoch, self.best_fitness))
            if self.best_fitness <= self.threshold:
                print(self.best_ind.mirror.a)
                print(self.best_ind.mirror.c)
                break
            self.cross_section()
            self.mutation()

        print(self.best_ind.mirror.a)
        print(self.best_ind.mirror.c)


def main():
    settings = {'pop_size': 250,
                'num_genes': 2,
                'epochs': 100,
                'selection_ratio': 0.5,
                'mutation_prob': 0.05,
                'num_rays': 1440,
                'mirror_right_lim': 0.2,
                'screen_position': 2,
                'threshold': 0.02}
    
    optimizer = RayOpt(settings)
    optimizer.optimize()


if __name__=='__main__':
    main()
