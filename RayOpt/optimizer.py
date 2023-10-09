from experiment import Experiment
from utils.plotter import plotter
import numpy as np
from scipy.stats import kstest, anderson, norm
from scipy import special
import random
import yaml
from datetime import datetime
import os


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
        self.path = settings['path']

    def generate_init_pop(self):
        for _ in range(self.pop_size):
            a = random.uniform(0, 1000)
            c = random.uniform(-1, 0)
            self.population.append(Experiment(self.num_rays, a, c, self.mirror_right_lim, self.screen_position))

    def fitness_function(self, arr):
        ksstat, p_value = kstest(arr, "norm", args=(0, 0.2))
        res = [ksstat, p_value]
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
                        epoch,
                        self.path,
                        self.best_ind.mirror.a,
                        self.best_ind.mirror.c,
                        self.best_ind.fitness)
    
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
                print('Best parameter a: {}'.format(self.best_ind.mirror.a))
                print('Best parameter c: {}'.format(self.best_ind.mirror.c))
                break
            self.cross_section()
            self.mutation()

        print('Best parameter a: {}'.format(self.best_ind.mirror.a))
        print('Best parameter c: {}'.format(self.best_ind.mirror.c))


def main():
    with open('config.yml', 'r') as file:
        settings = yaml.safe_load(file)

    now = datetime.now()
    now = now.strftime("%d_%m_%Y-%H_%M_%S")
    path = './results/experiment_{}'.format(now)
    if not os.path.isdir(path):
        os.makedirs(path)
    settings['path'] = path
    
    optimizer = RayOpt(settings)
    optimizer.optimize()


if __name__=='__main__':
    main()
