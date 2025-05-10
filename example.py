import pandas as pd
from compute_visibility_graph import visibility_graph
from plot_graphs import plot_visibility_graph
from compute_degree_distribution import degree_count_distribution, degree_count_probability_distribution, degrees_of_points
from plot_degree_distribution import *
from star_data_reader_plotter import get_folded_curve_subset, read_star_data
from fit_line import line_fit
import networkx as nx

points = [(1,2), (2,8), (3.5,4), (3,4), (4,5), (5,7), (6,8)]

graph = visibility_graph(points, full_curve=True)

plot_visibility_graph(points, graph)

nx.Graph

# light_curve_data = pd.read_csv('star1.csv')

# x = light_curve_data['T']
# y = light_curve_data['Flux']

# points = [(x[i], y[i]) for i in range(len(x))]

# star_data = read_star_data('OGLE-TR-1001')
# star_data = read_star_data('OGLE-TR-1002')
# star_data = read_star_data('OGLE-TR-1049')
# star_data = read_star_data('OGLE-TR-1001')
# star_data = read_star_data('OGLE-TR-1021', margin_in_hours=8.2536/2)
# star_data = read_star_data('OGLE-TR-1049', margin_in_hours=15)

# star_name = 'OGLE-TR-1021'

# star_data = read_star_data(star_name)

# points = get_folded_curve_subset(points, use_full_curve=True)
# points = get_folded_curve_subset(star_data, use_full_curve=False)

# print()
# print(points)
# print()


# x, y = zip(*points)

# sorted_points = sorted(points, key=lambda x: x[0])

# xs, ys = zip(*sorted_points)

# df = pd.DataFrame(columns=['T', 'Mag'], data=[[xs[i], ys[i]] for i in range(len(sorted_points))])

# df.to_csv('Kink Points.csv', index=False)

# n = len(x)

# new_y = [val*-1 for val in y]

# new_points = [(x[i], new_y[i]) for i in range(n)]

# graph = visibility_graph(new_points, full_curve=True)
# # graph = visibility_graph(new_points, read_from_file_of_star=star_name, write_to_file_of_star=star_name)
# # graph = visibility_graph(points)
# # print(graph)

# deg_points = degrees_of_points(graph)

# # plt.scatter(x, deg_points)
# plot_degree_vs_point_number(deg_points)
# plt.scatter([i for i in range(len(deg_points))], deg_points)
# plt.xlabel('Point Number')
# plt.ylabel('Degree')
# plt.title(f'{star_name} Degree of Each Point')
# plt.plot()

# plot_visibility_graph(new_points, graph)
# # plot_visibility_graph(points, graph)

# degree_dist = degree_count_distribution(graph)
# print(degree_dist)

# degree_prob_dist = degree_count_probability_distribution(graph)

# deg_count_dist = plot_degree_count_distribution(degree_prob_dist)

# semi_log_dist = semi_log_plot_degree_distribution(degree_prob_dist)

# log_log_dist = log_log_plot_degree_distribution(degree_prob_dist)

# intercept, slope, sum_of_square_of_fit_errors, sum_of_square_of_all_errors = line_fit(log_log_dist, filter_condition='first_a_after_first_b', a=3, b=20)