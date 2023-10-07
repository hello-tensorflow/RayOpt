import numpy as np
from matplotlib import pyplot as plt
import matplotlib
from scipy.stats import norm
 

def plotter(design_area, mirror, all_collisions, light_source, screen_position, cnt):
    fig, (ax1, ax2) = plt.subplots(1, 2)
    # Plot mirror    
    limits = np.sqrt((design_area-mirror.c)/mirror.a)
    t = np.linspace(0, limits, 1000)

    ax1.plot(mirror.eq_param(t)[0], mirror.eq_param(t)[2], 'red')
    ax1.plot(mirror.eq_param(t)[0], mirror.eq_param(t)[1], 'red')
    ax1.set_title("Sine Function")

    # Plot rays
    # for single_ray in all_collisions:
    #     res = np.array(single_ray).T
    #     ax1.plot(res[0], res[1], light_source.color, linewidth=light_source.thickness)
    # ax1.plot(light_source.origin[0], light_source.origin[1], marker="o", markersize=3, markerfacecolor="red")

    # Plot screen
    # ax1.plot([screen_position, screen_position], [-100, 100], 'black', linewidth=5)

    screen_collisions = []
    for ray in all_collisions:
        screen_collisions.append(ray[-1][1])
    #screen_collisions = norm.pdf(screen_collisions, 0, 0.2)
    mu = 0
    sigma = 0.2
    x = np.linspace(mu - 3*sigma, mu + 3*sigma, 100)
    ax2.plot(x, norm.pdf(x, mu, sigma))
    #x_axis = np.arange(-0.6, 0.6, 0.01)
    #plt.plot(x_axis, norm.pdf(x_axis, 0, 0.2))
    ax2.hist(screen_collisions, bins=100, density=True)
        # Save figure
    plt.savefig('./results/test_results_{}.png'.format(cnt), dpi = 300)

# def plotter(design_area, mirror, all_collisions, light_source, screen_position, cnt):
#     plt.figure(figsize=(10,10))
#     plt.axis([-0.2, 2, -0.8, 0.8])
#     # Plot mirror    
#     limits = np.sqrt((design_area-mirror.c)/mirror.a)
#     t = np.linspace(0, limits, 1000)

#     plt.plot(mirror.eq_param(t)[0], mirror.eq_param(t)[2], 'red')
#     plt.plot(mirror.eq_param(t)[0], mirror.eq_param(t)[1], 'red')


#     # Plot rays
#     for single_ray in all_collisions:
#         res = np.array(single_ray).T
#         plt.plot(res[0], res[1], light_source.color, linewidth=light_source.thickness)
#     plt.plot(light_source.origin[0], light_source.origin[1], marker="o", markersize=3, markerfacecolor="red")

#     # Plot screen
#     plt.plot([screen_position, screen_position], [-100, 100], 'black', linewidth=5)

#     plt.savefig('./results/results_{}.png'.format(cnt), dpi = 300)
