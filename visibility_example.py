import pandas as pd
from compute_visibility_graph import visibility_graph
from plot_graphs import plot_visibility_graph
from compute_degree_distribution import degree_count_distribution, degree_count_probability_distribution, degrees_of_points
from plot_degree_distribution import *
from star_data_reader_plotter import get_folded_curve_subset

points = [(1,2), (2,8), (3.5,4), (3,4), (4,5), (5,7), (6,8)]
# points = [(1,-2), (2,-8), (3.5,-4), (3,-4), (4,-5), (5,-7), (6,-8)]

x, y = zip(*points)
x = list(x)

print(x)

graph = visibility_graph(points, full_curve=False)

# deg_points = degrees_of_points(graph)

# print(deg_points)

plot_visibility_graph(points, graph)

# nums = [i for i in range(len(deg_points))]

# plt.scatter(x, deg_points)
# plt.scatter(nums, deg_points)
# plt.show()