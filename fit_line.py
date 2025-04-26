import matplotlib.pyplot as plt
import math


def line_fit(points: list[tuple[float, float]]):
    points = [point for point in points if (point[0] > 1.5 and point[0] < 3.0)]
    n = len(points)

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

    sum_of_square_errors = sum(list(map(lambda x: x**2, errors)))

    print(f'Ideal value of the intercept and slope (b0: {b0}, b1: {b1})')
    print('Sum of square errors:', sum_of_square_errors)

    plt.scatter(x, y)
    plt.plot(x, line_fit_values)
    plt.grid(True)
    plt.show()