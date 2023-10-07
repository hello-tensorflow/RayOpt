from utils.ray import Light_Source
from utils.mirror import Mirror
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm, kstest
import statistics


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
    

def plot_simulation(light_source, mirror, screen_position, design_area, all_collisions):
    plt.figure(figsize=(10,10))
    plt.axis([-1.1, 2, -1.55, 1.55])
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
    plt.savefig('./results/reflections.png', dpi = 300)


def plot_histogram(all_collisions):
    plt.figure(figsize=(10,10))
    #plt.axis([-0.7, 0.7, 0, 2])
    screen_collisions = []
    for ray in all_collisions:
        screen_collisions.append(ray[-1][1])
    #screen_collisions = norm.pdf(screen_collisions, 0, 0.2)
    mu = 0
    sigma = 0.2
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    plt.plot(x, norm.pdf(x, mu, sigma))
    #x_axis = np.arange(-0.6, 0.6, 0.01)
    #plt.plot(x_axis, norm.pdf(x_axis, 0, 0.2))
    plt.hist(screen_collisions, bins=100, density=True)
    plt.savefig('./results/hist.png', dpi=300)


def main():

    light_source = Light_Source(0, 0, 'blue', 0.5, 1440)
    mirror = Mirror(202, -0.005, 2)
    screen_position = 2
    design_area = mirror.right_lim
    all_collisions = experiment(light_source, mirror, screen_position)
    screen_collisions = find_screen_collisions(all_collisions)

    ksstat, p_value = kstest(np.array(screen_collisions), "norm", args=(0, 0.2))
    print(ksstat, p_value)
    mean = statistics.mean(screen_collisions)
    sd = statistics.stdev(screen_collisions)
    print(mean, sd)

    plot_simulation(light_source, mirror, screen_position, design_area, all_collisions)
    plot_histogram(all_collisions)


if __name__=='__main__':
    main()
