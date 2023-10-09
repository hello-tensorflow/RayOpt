import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from scipy.stats import norm
 

def plotter(design_area, mirror, all_collisions, light_source, screen_position, cnt, path, mirror_a, mirror_c, fitness):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    # Plot mirror    
    limits = np.sqrt((design_area-mirror.c)/mirror.a)
    t = np.linspace(0, limits, 1000)

    ax1.plot(mirror.eq_param(t)[0], mirror.eq_param(t)[2], 'red')
    ax1.plot(mirror.eq_param(t)[0], mirror.eq_param(t)[1], 'red')
    ax1.set_title("Best a: {}; Best c: {}".format(round(mirror_a,3), round(mirror_c,3)))

    screen_collisions = []
    for ray in all_collisions:
        screen_collisions.append(ray[-1][1])

    mu = 0
    sigma = 0.2
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    ax2.plot(x, norm.pdf(x, mu, sigma))
    ax2.hist(screen_collisions, bins=100, density=True)
    ax2.set_title("Epoch: {}; KS: {}".format(cnt, round(fitness,3)))
    plt.savefig('{}/epoch_{}.png'.format(path, cnt), dpi = 300)

