from utils.ray import Light_Source
from utils.mirror import Mirror
import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import norm, kstest, anderson
import statistics
import seaborn as sns

# x_axis = np.arange(-0.6, 0.6, 0.001)
# arr = norm.pdf(x_axis, 0, 0.2)

# ksstat, p_value = kstest(np.array(arr), "norm", args=(0, 0.2))
# print(ksstat)

# def plot_histogram():
#     plt.figure(figsize=(10,10))
#     #plt.axis([-2, 2, 0, 15])
    
#     x_axis = np.arange(-2, 2, 0.001)
#     arr = norm.pdf(x_axis, 0, 0.2)
#     plt.plot(x_axis, norm.pdf(x_axis, 0, 0.2))
#     plt.hist(arr, bins=25, density=True)
#     plt.savefig('./results/test.png', dpi=300)

def plot_histogram():
    data_normal = norm.rvs(size=10000, loc=0, scale=0.2)
    data_normal = np.array(data_normal)
    
    ksstat, p_value = kstest(data_normal, "norm", args=(0, 0.2))
    print(ksstat, p_value)
    #ax = sns.distplot(data_normal, bins=100, kde=True, color='skyblue', hist_kws={"linewidth": 15, 'alpha':1})
    #ax = sns.distplot(data_normal)
    andtest = anderson(data_normal)
    print(andtest)
    print(andtest.fit_result)
    print(andtest.fit_result.params[0])
    #ax.set(xlabel='Normal Distribution', ylabel='Frequency')

    #ax.savefig('./results/test_sns.png')
    x_axis = np.arange(-2, 2, 0.001)
    arr = norm.pdf(x_axis, 0, 0.2)
    plt.plot(x_axis, norm.pdf(x_axis, 0, 0.2))
    plt.hist(data_normal, bins = 100, density=True)
    plt.savefig('./results/test_sns.png')

def main():
    #plot_histogram()
    x_axis = np.arange(-2, 2, 0.001)
    arr = norm.pdf(x_axis, 0, 0.2)
    print(arr)
    print(len(arr))

if __name__=='__main__':
    main()