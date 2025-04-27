import matplotlib.pyplot as plt
import math
from typing import Literal

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


def line_fit(star_name: str, original_points: list[tuple[float, float]], full_curve: bool, filter_condition: Literal['between_a_and_b', 'first_a_after_first_b'], a: int|float, b: int|float) -> tuple[float, float, float, float]:
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

    all_errors = [all_y[i] - all_line_fit_values[i] for i in range(len(y))]
    
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
    plt.title(f'{star_name} Log Log Degree Distribution \nLine Fit from Point {a+1} to Point {b+1}', fontsize=14)
    
    if full_curve:
        plt.savefig(f'./ogle_star_data/precomputed_data/full_curve/Line Fit/Plots/{star_name}.png')
    else:
        plt.savefig(f'./ogle_star_data/precomputed_data/t14_region_curve/Line Fit/Plots/{star_name}.png')
    
    plt.show()
    
    return b0, b1, sum_of_square_of_fit_errors, sum_of_square_of_all_errors