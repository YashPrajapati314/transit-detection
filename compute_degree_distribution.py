def degree_count_distribution(graph: list[list[int]], increment_extreme_point_degrees: bool = True) -> dict[int, int]:
    n = len(graph)
    degree_counts: dict[int, int] = dict()
    for i, row in enumerate(graph):
        degree = sum(row)
        if increment_extreme_point_degrees and (i == 0 or i == n-1):
            degree += 1
        current_number_of_occurences = degree_counts.get(degree, 0)
        degree_counts[degree] = current_number_of_occurences + 1
    return degree_counts

def degree_count_probability_distribution(graph: list[list[int]], increment_extreme_point_degrees: bool = True) -> dict[int, float]:
    degree_counts = degree_count_distribution(graph, increment_extreme_point_degrees)
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