import matplotlib.pyplot as plt
import math
from typing import Literal

def plotter(type: Literal['degree_count_distibution', 'semi_log_plot', 'log_log_plot'], points, star_name, full_curve: bool, scatter=True, name='', xlabel='', ylabel=''):
    x, y = zip(*points)
    if type == 'degree_count_distibution' or type == 'log_log_plot':
        if scatter:
            plt.scatter(x, y, s=10)
        else:
            plt.plot(x, y)
    if type == 'semi_log_plot':
        plt.semilogy(x, y, marker='o', linestyle='', markersize=5)

    plt.xlabel(xlabel, fontsize=13)
    plt.ylabel(ylabel, fontsize=13)
    plt.title(name, fontsize=14)
    
    if type == 'degree_count_distibution':
        directory = 'Degree Probability Distribution'
    elif type == 'log_log_plot':
        directory = 'Log Log Degree Probability Distribution'
    elif type == 'semi_log_plot':
        directory = 'Semilog Degree Probability Distribution'
        
    
    if full_curve:
        plt.savefig(f'./ogle_star_data/precomputed_data/full_curve/{directory}/Plots/{star_name}.png')
    else:
        plt.savefig(f'./ogle_star_data/precomputed_data/t14_region_curve/{directory}/Plots/{star_name}.png')
    
    plt.show()
    
    
def plot_degree_vs_point_number(deg_points: list[int], star_name, full_curve: bool, xlabel='Point Number', ylabel='Degree', plot: bool = True) -> list[tuple[int, int]]:
    x = [i for i in range(len(deg_points))]
    y = deg_points
    
    plt.scatter(x, y, s=1)
    plt.xlabel(xlabel, fontsize=13)
    plt.ylabel(ylabel, fontsize=13)
    plt.title(f'{star_name} Degree of Each Point', fontsize=14)
    
    if full_curve:
        plt.savefig(f'./ogle_star_data/precomputed_data/full_curve/Degree of Each Point/Plots/{star_name}.png')
    else:
        plt.savefig(f'./ogle_star_data/precomputed_data/t14_region_curve/Degree of Each Point/Plots/{star_name}.png')
    
    if plot:
        plt.show()
    else:
        plt.clf()
    
    points = [(x[i], y[i]) for i in range(len(deg_points))]
    
    return points
    

def plot_degree_count_distribution(degree_count_distibution: dict[int, int|float], star_name, full_curve: bool, scatter=True, xlabel='Degree', ylabel='Probability/Occurence', plot: bool = True) -> list[tuple[int, int|float]]:
    points = degree_count_distibution.items()
    if plot:
        plotter('degree_count_distibution', points, star_name, full_curve, scatter, f'{star_name} Degree Distribution', xlabel, ylabel)
    return points


def semi_log_plot_degree_distribution(degree_count_distibution: dict[int, int|float], star_name, full_curve: bool, scatter=True, xlabel='Degree', ylabel='Probability/Occurence', plot: bool = True) -> list[tuple[int, int|float]]:
    points = degree_count_distibution.items()
    if plot:
        plotter('semi_log_plot', points, star_name, full_curve, scatter, f'{star_name} Semilog Plot Degree Distribution', xlabel, ylabel)
    return points

def log_log_plot_degree_distribution(degree_count_distibution: dict[int, int|float], star_name, full_curve: bool, scatter=True, xlabel='log(degree)', ylabel='log(P)', plot: bool = True) -> list[tuple[float, float]]:
    points = degree_count_distibution.items()
    log_probability_distribution = [(math.log(x), math.log(y)) for x, y in points]
    if plot:
        plotter('log_log_plot', log_probability_distribution, star_name, full_curve, scatter, f'{star_name} Logarithmic Plot Degree Distribution', xlabel, ylabel)
    return log_probability_distribution
