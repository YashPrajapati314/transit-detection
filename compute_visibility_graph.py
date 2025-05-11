import json


def visibility_graph(points: list[tuple[int|float, int|float]], full_curve: bool, already_sorted: bool = False) -> list[list[int]]:
    # Do not use the read write feature, storing visibility graphs is taking a lot of space and can crash your device
    if full_curve:
        parent_directory = 'full_curve'
    else:
        parent_directory = 't14_region_curve'
        
    # if read_from_file_of_star != '' and write_to_file_of_star != '' and read_from_file_of_star != write_to_file_of_star:
    #     print('Read Write Name Mismatch')
    #     return None
    
    # if read_from_file_of_star != '':
    #     with open(f'./ogle_star_data/precomputed_data/{parent_directory}/visibility_graphs.json') as f:
    #         data: dict[str, list[list[int]]] = json.load(f)
    #         visibility_graph_matrix = data.get(read_from_file_of_star)
    #         if visibility_graph_matrix == None:
    #             pass
    #         else:
    #             print(f'Reading data of precomputed visibility graph of {read_from_file_of_star}')
    #             return visibility_graph_matrix
        
    if not already_sorted:
        points.sort(key=lambda point: (point[0]))
        
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    n = len(y_coords)
    graph = [[0] * n for _ in range(n)]  # adjacency matrix
    
    def find_max_index_in_subarray(subarray, offset):
        max_val = subarray[0]
        max_idx = 0
        for i in range(1, len(subarray)):
            if subarray[i] > max_val:
                max_val = subarray[i]
                max_idx = i
        return max_idx + offset

    def visibility_graph_subarray(x, y, left, right, graph):
        if left >= right:
            return
        
        k = find_max_index_in_subarray(x[left:right + 1], left)
        for i in range(left, right + 1):
            if i == k:
                continue

            visible = True
            for j in range(min(i + 1, k + 1), max(i, k)):
                if x[j] >= x[i] + (x[k] - x[i]) * ((y[j] - y[i]) / (y[k] - y[i])):
                    visible = False
                    break

            if visible:
                graph[k][i] = 1
                graph[i][k] = 1
        
        visibility_graph_subarray(x, y, left, k - 1, graph) 
        visibility_graph_subarray(x, y, k + 1, right, graph) 

    visibility_graph_subarray(y_coords, x_coords, 0, n - 1, graph)
    
    # if write_to_file_of_star != '':
    #     with open(f'./ogle_star_data/precomputed_data/{parent_directory}/visibility_graphs.json') as f:
    #         data: dict[str, list[list[int]]] = json.load(f)
            
    #     data[write_to_file_of_star] = graph
        
    #     with open(f'./ogle_star_data/precomputed_data/{parent_directory}/visibility_graphs.json', 'w') as f:
    #         json.dump(data, f)
    #         # json.dump(data, f, separators=(',', ':'))
    #         print(f'Stored the visibility graph for {write_to_file_of_star}')
    
    return graph


def visibility_graph_range_wise(points: list[tuple[int|float, int|float]], full_curve: bool, t14: float, tc: float = 0, already_sorted: bool = False) -> tuple[list[list[int]], list[list[int]], list[list[int]]]:
    if not already_sorted:
        points.sort(key=lambda point: (point[0]))
    
    if full_curve:
        parent_directory = 'full_curve'
    else:
        parent_directory = 't14_region_curve'
    
    transit_start = (-1 * t14 / 2) * 24
    transit_end = (t14 / 2) * 24
    
    # print('!!!')
    # print(transit_start)
    # print([float(point[0]) for point in points])
    # print('!!!')
    
    points_left = list(filter(lambda x: (x[0] < transit_start), points))
    points_mid = list(filter(lambda x: (x[0] > transit_start and x[0] < transit_end), points))
    points_right = list(filter(lambda x: (x[0] > transit_end), points))
    
    # print('!!!')
    # print(points_left)
    # print('!!!')
    
    return (visibility_graph(points_left, full_curve=False, already_sorted=True), visibility_graph(points_mid, full_curve=False, already_sorted=True), visibility_graph(points_right, full_curve=False, already_sorted=True))


def horizontal_visibility_graph(points: list[tuple[int|float, int|float]], already_sorted: bool = False) -> list[list[int]]:
    if not already_sorted:
        points.sort(key=lambda point: (point[0]))
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    n = len(y_coords)
    graph = [[0] * n for _ in range(n)]  # adjacency matrix

    def find_max_index_in_subarray(subarray, offset):
        max_val = subarray[0]
        max_idx = 0
        for i in range(1, len(subarray)):
            if subarray[i] > max_val:
                max_val = subarray[i]
                max_idx = i
        return max_idx + offset  

    def visibility_graph_subarray(y, x, left, right, graph):
        if left >= right:
            return
        
        k = find_max_index_in_subarray(y[left:right + 1], left)
        for i in range(left, right + 1):
            if i == k:
                continue

            visible = True
            for j in range(i + 1, k):
                if y[j] >= min(y[i], y[k]): 
                    visible = False
                    break

            if visible:
                graph[k][i] = 1
                graph[i][k] = 1
        
        visibility_graph_subarray(y, x, left, k - 1, graph)  
        visibility_graph_subarray(y, x, k + 1, right, graph)  

    visibility_graph_subarray(y_coords, x_coords, 0, n - 1, graph)
    return graph


