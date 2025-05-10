import math
import numpy as np
import matplotlib.pyplot as plt
from typing import Literal
from sklearn.cluster import DBSCAN

def line_fit_condition_filter(original_points: list[tuple[float, float]], condition: Literal['between_a_and_b', 'first_a_after_first_b'], a: int|float, b: int|float) -> tuple[list[tuple[float, float]], list[str], int, int]:
    if condition == 'between_a_and_b':
        points = [point for point in original_points if (point[0] >= a and point[0] <= b)]
        color_condition = ['purple' if (point[0] >= a and point[0] <= b) else 'blue' for point in original_points]
        point_start = color_condition.index('purple')
        point_end = len(original_points) - list(reversed(color_condition)).index('purple') - 1
        return points, color_condition, point_start, point_end
    elif condition == 'first_a_after_first_b':
        start_inclusive = a
        end_inclusive = a + b - 1
        points = original_points[start_inclusive:end_inclusive+1]
        color_condition = ['purple' if (i >= start_inclusive and i <= end_inclusive) else 'blue' for i in range(len(original_points))]
        return points, color_condition, a, b


def line_fit(star_name: str, original_points: list[tuple[float, float]], full_curve: bool, filter_condition: Literal['between_a_and_b', 'first_a_after_first_b'], a: int|float, b: int|float, write: bool = False, semilog: bool = False) -> tuple[float, float, float, float]:
    # original_points.sort(key=lambda x: x[0])
    points = list(original_points)
    points, color_condition, a, b = line_fit_condition_filter(original_points, condition=filter_condition, a=a, b=b)
    
    n = len(points)

    all_x = [val[0] for val in original_points]
    all_y = [val[1] for val in original_points]
    
    x = [val[0] for val in points]
    y = [val[1] for val in points]

    sigma_x = sum(x)
    sigma_y = sum(y)
    sigma_xy = sum([x[i] * y[i] for i in range(n)])
    sigma_x2 = sum(list(map(lambda x: x**2, x)))

    denom = (n * sigma_x2) - (sigma_x ** 2)

    b0 = (sigma_y * sigma_x2 - sigma_x * sigma_xy) / (denom)
    b1 = (n * sigma_xy - sigma_x * sigma_y) / (denom)

    line_fit_values = [b0 + b1 * val for val in x]

    errors = [y[i] - line_fit_values[i] for i in range(len(y))]

    sum_of_square_of_fit_errors = sum(list(map(lambda x: x**2, errors)))
    
    all_line_fit_values = [b0 + b1 * val for val in all_x]

    all_errors = [all_y[i] - all_line_fit_values[i] for i in range(len(all_y))]
    
    sum_of_square_of_all_errors = sum(list(map(lambda x: x**2, all_errors)))

    print(f'Ideal value of the intercept and slope (b0: {b0}, b1: {b1})')
    print('Sum of square errors between only the points used to fit:', sum_of_square_of_fit_errors)
    print('Sum of square errors between all the points:', sum_of_square_of_all_errors)

    plt.scatter(all_x, all_y, c=color_condition, s=10)
    plt.plot(all_x, all_line_fit_values, color='purple', label=f'Line Fit: y = {b1:.4f}x + {b0:.4f}')
    plt.grid(True)
    plt.legend(fontsize=12)
    xlabel='log(degree)'
    ylabel='log(P)'
    plt.xlabel(xlabel, fontsize=13)
    plt.ylabel(ylabel, fontsize=13)
    plt.title(f'{star_name} Semilog Degree Distribution \nLine Fit from Point {a+1} to Point {b+1}', fontsize=14)
    
    if semilog:
        directory = 'Line Fit Semilog'
    else:
        directory = 'Line Fit'
        
    
    if write:
        if full_curve:
            plt.savefig(f'./ogle_star_data/precomputed_data/full_curve/{directory}/Plots/{star_name}.png')
        else:
            plt.savefig(f'./ogle_star_data/precomputed_data/t14_region_curve/{directory}/Plots/{star_name}.png')
    
    # plt.show()
    
    return b0, b1, sum_of_square_of_fit_errors, sum_of_square_of_all_errors


def line_fit_for_auto_cluster(star_name: str, all_points: list[tuple[float, float]], start_index: int, end_index: int) -> tuple[float, float, float, float, list[float]]:
    # all_points.sort(key=lambda x: x[0])
    points = list(all_points)
    
    points = all_points[start_index:end_index+1]
    color_condition = ['purple' if (i >= start_index and i <= end_index) else 'blue' for i in range(len(all_points))]
    
        
    n = len(points)

    all_x = [val[0] for val in all_points]
    all_y = [val[1] for val in all_points]
    
    x = [val[0] for val in points]
    y = [val[1] for val in points]

    sigma_x = sum(x)
    sigma_y = sum(y)
    sigma_xy = sum([x[i] * y[i] for i in range(n)])
    sigma_x2 = sum(list(map(lambda x: x**2, x)))

    denom = (n * sigma_x2) - (sigma_x ** 2)

    b0 = (sigma_y * sigma_x2 - sigma_x * sigma_xy) / (denom)
    b1 = (n * sigma_xy - sigma_x * sigma_y) / (denom)

    line_fit_values = [b0 + b1 * val for val in x]

    errors = [y[i] - line_fit_values[i] for i in range(len(y))]

    sum_of_square_of_fit_errors = sum(list(map(lambda x: x**2, errors)))
    
    all_line_fit_values = [b0 + b1 * val for val in all_x]

    all_errors = [all_y[i] - all_line_fit_values[i] for i in range(len(all_y))]

    # signed_all_errors = list(map(lambda x: math.copysign(x**4, x), all_errors))
    signed_all_errors = list(map(lambda x: math.copysign(x**2, x), all_errors))
    
    sum_of_square_of_all_errors = sum(list(map(lambda x: x**2, all_errors)))

    print(f'Ideal value of the intercept and slope (b0: {b0}, b1: {b1})')
    print('Sum of square errors between only the points used to fit:', sum_of_square_of_fit_errors)
    print('Sum of square errors between all the points:', sum_of_square_of_all_errors)

    plt.scatter(all_x, all_y, c=color_condition, s=10)
    plt.plot(all_x, all_line_fit_values, color='purple', label=f'Line Fit: y = {b1:.4f}x + {b0:.4f}')
    plt.grid(True)
    plt.legend(fontsize=12)
    xlabel='log(degree)'
    ylabel='log(P)'
    plt.xlabel(xlabel, fontsize=13)
    plt.ylabel(ylabel, fontsize=13)
    plt.title(f'{star_name} Log Log Degree Distribution \nLine Fit from Point {start_index+1} to Point {end_index+1}', fontsize=14)
    
    plt.show()
    
    return b0, b1, sum_of_square_of_fit_errors, sum_of_square_of_all_errors, signed_all_errors

def my_line_fit_algorithm(star_name: str, all_points: list[tuple[float, float]], midpoint_near: float, points_to_consider_on_each_side: int, full_curve, semilog: bool = False):
    bring_inline_points_closer = not(full_curve)
    if semilog:
        start_index = 0
        end_index = 15 if full_curve else 50
    else:
        midpoint_near_point_number = min([(i, abs(point[0] - midpoint_near)) for i, point in enumerate(all_points)], key=lambda x: x[1])[0]
        start_index = max(midpoint_near_point_number - points_to_consider_on_each_side, 0)
        end_index = min(midpoint_near_point_number + points_to_consider_on_each_side, len(all_points) - 1)
    intercept, slope, sum_of_square_of_fit_errors, sum_of_square_of_all_errors, signed_all_errors = line_fit_for_auto_cluster(star_name, all_points, start_index, end_index)
    
    if bring_inline_points_closer:
        new_all_points = [(all_points[i][0], all_points[i][1] - signed_all_errors[i]) if (i>=start_index and i<=end_index)
                        else (all_points[i][0], all_points[i][1] + signed_all_errors[i])
                        for i in range(len(all_points))]
    else:
        new_all_points = [(all_points[i][0], all_points[i][1] + signed_all_errors[i]) for i in range(len(all_points))]
        
    intercept, slope, sum_of_square_of_fit_errors, sum_of_square_of_all_errors, signed_all_errors = line_fit_for_auto_cluster(star_name, new_all_points, start_index, end_index)
    X = np.array(new_all_points)
    if bring_inline_points_closer:
        clustering = DBSCAN(eps=0.5, min_samples=4).fit(X) # Works very well for full curves
    else:
        # clustering = DBSCAN(eps=0.6, min_samples=4).fit(X)
        clustering = DBSCAN(eps=0.4, min_samples=3).fit(X)
    labels = list(clustering.labels_)
    print(labels)
    
    new_all_x, new_all_y = zip(*new_all_points)
    
    plt.scatter(new_all_x, new_all_y, c=labels, cmap='Set1')
    # plt.plot(new_all_x, all_line_fit_values, color='purple', label=f'Line Fit: y = {b1:.4f}x + {b0:.4f}')
    plt.grid(True)
    plt.legend(fontsize=12)
    xlabel='log(degree)-SSE'
    ylabel='log(P)-SSE'
    plt.xlabel(xlabel, fontsize=13)
    plt.ylabel(ylabel, fontsize=13)
    plt.title(f'{star_name} DBSCAN on Log Log Degree Distribution \nLine Fit from Point {start_index+1} to Point {end_index+1}', fontsize=14)
    
    plt.show()
    
    cluster_of_midpoint = labels[midpoint_near_point_number]
    
    if cluster_of_midpoint == -1:
        if semilog:
            my_line_fit_algorithm(star_name, all_points, None, None, full_curve=full_curve)
        else:
            my_line_fit_algorithm(star_name, all_points, midpoint_near=midpoint_near+0.5, points_to_consider_on_each_side=points_to_consider_on_each_side, bring_inline_points_closer=bring_inline_points_closer)
    else:
        new_start_index = labels.index(cluster_of_midpoint)
        new_end_index = len(labels) - list(reversed(labels)).index(cluster_of_midpoint) - 1
        
        b0, b1, sum_of_square_of_fit_errors, sum_of_square_of_all_errors, signed_all_errors = line_fit_for_auto_cluster(star_name, all_points, new_start_index, new_end_index)
        
        return b0, b1, sum_of_square_of_fit_errors, sum_of_square_of_all_errors, signed_all_errors