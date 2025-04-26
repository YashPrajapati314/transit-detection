import matplotlib.pyplot as plt
import math

def plotter(type, points, scatter=True, name='', xlabel='', ylabel=''):
    x, y = zip(*points)
    if type == 'degree_count_distibution' or type == 'log_log_plot':
        if scatter:
            plt.scatter(x, y)
        else:
            plt.plot(x, y)
    if type == 'semi_log_plot':
        plt.semilogy(x, y, marker='o', linestyle='')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(name)
    
    plt.show()

def plot_degree_count_distribution(degree_count_distibution: dict[int, int|float], scatter=True, name='Degree Distribution', xlabel='Degree', ylabel='Probability/Occurence', plot: bool = True) -> list[tuple[int, int|float]]:
    points = degree_count_distibution.items()
    if plot:
        plotter('degree_count_distibution', points, scatter, name, xlabel, ylabel)
    return points


def semi_log_plot_degree_distribution(degree_count_distibution: dict[int, int|float], scatter=True, name='Semilog Plot Degree Distribution', xlabel='Degree', ylabel='Probability/Occurence', plot: bool = True) -> list[tuple[int, int|float]]:
    points = degree_count_distibution.items()
    if plot:
        plotter('semi_log_plot', points, scatter, name, xlabel, ylabel)
    return points

def log_log_plot_degree_distribution(degree_count_distibution: dict[int, int|float], scatter=True, name='Logarithmic Plot Degree Distribution', xlabel='log(degree)', ylabel='log(P)', plot: bool = True) -> list[tuple[float, float]]:
    points = degree_count_distibution.items()
    log_probability_distribution = [(math.log(x), math.log(y)) for x, y in points]
    if plot:
        plotter('log_log_plot', log_probability_distribution, scatter, name, xlabel, ylabel)
    return log_probability_distribution
