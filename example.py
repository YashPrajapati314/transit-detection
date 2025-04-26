import pandas as pd
from compute_visibility_graph import visibility_graph
from plot_graphs import plot_visibility_graph
from compute_degree_distribution import degree_count_distribution, degree_count_probability_distribution, degrees_of_points
from plot_degree_distribution import *
from star_data_reader_plotter import get_folded_curve_subset, read_star_data
from fit_line import line_fit

# points = [(1,2), (2,8), (3.5,4), (3,4), (4,5), (5,7), (6,8)]

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

star_name = 'OGLE-TR-1021'

star_data = read_star_data(star_name, margin_in_hours=15)

points = get_folded_curve_subset(star_data)

# print()
# print(points)
# print()


x, y = zip(*points)

sorted_points = sorted(points, key=lambda x: x[0])

xs, ys = zip(*sorted_points)

df = pd.DataFrame(columns=['T', 'Mag'], data=[[xs[i], ys[i]] for i in range(len(sorted_points))])

df.to_csv('Kink Points.csv', index=False)

n = len(x)

new_y = [val*-1 for val in y]

new_points = [(x[i], new_y[i]) for i in range(n)]

graph = visibility_graph(new_points)
# graph = visibility_graph(points)
# print(graph)

deg_points = degrees_of_points(graph)

# plt.scatter(x, deg_points)
plt.scatter([i for i in range(len(deg_points))], deg_points)
plt.xlabel('Point Number')
plt.ylabel('Degree')
plt.title(f'{star_name} Degree of Each Point')
plt.plot()

plot_visibility_graph(new_points, graph)
# plot_visibility_graph(points, graph)

degree_dist = degree_count_distribution(graph)
print(degree_dist)

degree_prob_dist = degree_count_probability_distribution(graph)

deg_count_dist = plot_degree_count_distribution(degree_prob_dist)

semi_log_dist = semi_log_plot_degree_distribution(degree_prob_dist)

log_log_dist = log_log_plot_degree_distribution(degree_prob_dist)

line_fit(log_log_dist)