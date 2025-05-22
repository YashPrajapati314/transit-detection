import numpy as np
import networkx as nx

def degree_count_distribution(degree_of_each_point: list[tuple[int, int]], increment_extreme_point_degrees: bool = True) -> dict[int, int]:
    degree_counts: dict[int, int] = dict()
    for point_num, degree in degree_of_each_point:
        current_number_of_occurences = degree_counts.get(degree, 0)
        degree_counts[degree] = current_number_of_occurences + 1
    degree_counts = dict(sorted(degree_counts.items()))
    return degree_counts

def degree_count_probability_distribution(degree_of_each_point: list[tuple[int, int]], increment_extreme_point_degrees: bool = True) -> dict[int, float]:
    degree_counts = degree_count_distribution(degree_of_each_point, increment_extreme_point_degrees)
    sum_of_degrees = sum(degree_counts.values())
    probability_distribution_of_degree_counts = {degree: (distribution / sum_of_degrees) for degree, distribution in degree_counts.items()}
    return probability_distribution_of_degree_counts

def degrees_of_points(graph: list[list[int]], increment_extreme_point_degrees: bool = True) -> list[int]:
    n = len(graph)
    degrees_of_points_list: list[int] = []
    degree_counts: dict[int, int] = dict()
    for i, row in enumerate(graph):
        degree = sum(row)
        if increment_extreme_point_degrees and (i == 0 or i == n-1):
            degree += 1
        degrees_of_points_list.append(degree)
        current_number_of_occurences = degree_counts.get(degree, 0)
        degree_counts[degree] = current_number_of_occurences + 1
    return degrees_of_points_list

def clustering_coefficients_of_points(graph: list[list[int]], degrees_of_each_point: list[int] | None = None) -> list[float]:
    if degrees_of_each_point == None:
        degrees_of_each_point = degrees_of_points(graph)
    G: nx.classes.graph.Graph = nx.from_numpy_array(np.array(graph))
    triangle_counts: dict[int, int] = nx.triangles(G)
    triangles_containing_each_point: list[int] = list(triangle_counts.values())
    if len(triangles_containing_each_point) != len(degrees_of_each_point):
        print('Length mismatch error while computing clustering coefficient')
    else:
        n = len(triangles_containing_each_point)
        clustering_coefficients_of_each_point: list[float] = [2 * triangles_containing_each_point[i] / (degrees_of_each_point[i] * (degrees_of_each_point[i] - 1)) for i in range(n)]
        return clustering_coefficients_of_each_point