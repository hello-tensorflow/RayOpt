from utils.ray import Light_Source
from utils.mirror import Mirror
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm, kstest
import statistics
import argparse


def experiment(light_source, mirror, screen_position):
    all_rays_collisions = []
    for ray in light_source.rays:
        ray.propagate(mirror, screen_position)
        all_rays_collisions.append(ray.collisions)
    return all_rays_collisions

def find_screen_collisions(all_collisions):
    screen_collisions = []
    for ray in all_collisions:
        screen_collisions.append(ray[-1][1])
    return screen_collisions
    

def plot_simulation(light_source, mirror, screen_position, design_area, all_collisions, path):
    plt.figure(figsize=(10,10))
    plt.axis([-0.1, 2, -0.25, 0.25])
    # Plot rays
    for single_ray in all_collisions:
        res = np.array(single_ray).T
        plt.plot(res[0], res[1], light_source.color, linewidth=light_source.thickness)
    plt.plot(light_source.origin[0], light_source.origin[1], marker="o", markersize=3, markerfacecolor="red")
    # Plot mirror    
    limits = np.sqrt((design_area-mirror.c)/mirror.a)
    t = np.linspace(0, limits, 1000)
    plt.plot(mirror.eq_param(t)[0], mirror.eq_param(t)[2], 'red')
    plt.plot(mirror.eq_param(t)[0], mirror.eq_param(t)[1], 'red')
    # Plot screen
    plt.plot([screen_position, screen_position], [-100, 100], 'black', linewidth=5)
    # Save figure
    plt.savefig(path, dpi = 300)


def plot_histogram(all_collisions, path):
    plt.figure(figsize=(10,10))

    screen_collisions = []
    for ray in all_collisions:
        screen_collisions.append(ray[-1][1])

    mu = 0
    sigma = 0.2
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    plt.plot(x, norm.pdf(x, mu, sigma))

    plt.hist(screen_collisions, bins=100, density=True)
    plt.savefig(path, dpi=300)


def main():
    parser = argparse.ArgumentParser(description="Simple 2D ray tracer to play around")
    parser.add_argument("--num_rays", default=360, type=int, help="number of rays")
    parser.add_argument("--a", default=200, type=float, help="parameter 'a' of a parabola")
    parser.add_argument("--c", default=-0.005, type=float, help="parameter 'c' of a parabola")
    parser.add_argument("--rlim", default=0.1, type=float, help="right limit of the design area in meters")
    parser.add_argument("--screen", default=2, type=int, help="position of the screen in meters")
    parser.add_argument("--t_mu", default=0, type=float, help="target mean")
    parser.add_argument("--t_var", default=0.1, type=float, help="target variance")
    parser.add_argument("--path_h", default='./results/hist.png', type=str, help="path to save histogram")
    parser.add_argument("--path_s", default='./results/simulation.png', type=str, help="path to save simulation results")
    args = parser.parse_args()

    light_source = Light_Source(0, 0, 'blue', 0.5, args.num_rays)
    mirror = Mirror(args.a, args.c, args.rlim)
    screen_position = args.screen
    design_area = mirror.right_lim
    all_collisions = experiment(light_source, mirror, screen_position)
    screen_collisions = find_screen_collisions(all_collisions)

    ksstat, p_value = kstest(np.array(screen_collisions), "norm", args=(args.t_mu, args.t_var))
    print('Kolmogorov-Smirnov Test. Statistic: {}; P-value: {}'.format(ksstat, p_value))
    mean = statistics.mean(screen_collisions)
    sd = statistics.stdev(screen_collisions)
    print('The mean and variance of resulting distribution. Mean: {}; Variance: {}'.format(mean, sd))

    plot_simulation(light_source, mirror, screen_position, design_area, all_collisions, args.path_s)
    plot_histogram(all_collisions, args.path_h)


if __name__=='__main__':
    main()
