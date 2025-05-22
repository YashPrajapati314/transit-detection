import os
import networkx as nx
import numpy as np
import gzip
import pickle

def load_graph(star_name: str, path: str) -> list[list[int]] | None:
    if os.path.exists(path):
        print(f'\nLoading visibility graph for {star_name} from {path}\n')
        with gzip.open(path, 'rb') as f:
            G: nx.classes.graph.Graph = pickle.load(f)
            numpy_graph: np.ndarray = nx.to_numpy_array(G)
            graph: list[list[int]] = numpy_graph.astype(int).tolist()
            return graph
    else:
        return None

def visibility_graph(star_name: str, points: list[tuple[int|float, int|float]], full_curve: bool, already_sorted: bool = False, region_wise: bool = False, region: int = 0) -> list[list[int]]:
    if full_curve:
        parent_directory = 'full_curve'
    else:
        parent_directory = 't14_region_curve'
        
    if region_wise:
        directory = os.path.join('.', 'ogle_star_data', 'precomputed_data', 'Visibility Graph Regionwise')
        match(region):
            case 1:
                add_to_path = 'before-transit'
            case 2:
                add_to_path = 'during-transit'
            case 3:
                add_to_path = 'after-transit'
            case _:
                add_to_path = 'error'
        rel_path = os.path.join(directory, f'{star_name}_{add_to_path}.pkl.gz')
    else:
        directory = os.path.join('.', 'ogle_star_data', 'precomputed_data', parent_directory, 'Visibility Graph')
        rel_path = os.path.join(directory, f'{star_name}.pkl.gz')
        
    
    loaded_graph = load_graph(star_name=star_name, path=rel_path)

    if loaded_graph != None:
        return loaded_graph
        
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
    
    
    G: nx.classes.graph.Graph = nx.from_numpy_array(np.array(graph))

    with gzip.open(rel_path, 'wb') as f:
        pickle.dump(G, f)
    
    return graph


def visibility_graph_range_wise(star_name: str, points: list[tuple[int|float, int|float]], full_curve: bool, t14: float, tc: float = 0, already_sorted: bool = False) -> tuple[list[list[int]], list[list[int]], list[list[int]]]:
    if not already_sorted:
        points.sort(key=lambda point: (point[0]))
    
    # if full_curve:
    #     parent_directory = 'full_curve'
    # else:
    #     parent_directory = 't14_region_curve'
    
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
    
    before_transit_vg = visibility_graph(star_name, points_left, full_curve=False, already_sorted=True, region_wise=True, region=1)
    during_transit_vg = visibility_graph(star_name, points_mid, full_curve=False, already_sorted=True, region_wise=True, region=2)
    after_transit_vg = visibility_graph(star_name, points_right, full_curve=False, already_sorted=True, region_wise=True, region=3)
    
    return (before_transit_vg, during_transit_vg, after_transit_vg)


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


def points_range_wise(star_name: str, points: list[tuple[float, float]], t14: str, already_sorted: bool = False) -> tuple[list[tuple[float, float]], list[tuple[float, float]], list[tuple[float, float]]]:
    if not already_sorted:
        points.sort(key=lambda point: (point[0]))
    
    transit_start = (-1 * t14 / 2) * 24
    transit_end = (t14 / 2) * 24
    
    
    points_left: list[tuple[float, float]] = list(filter(lambda x: (x[0] < transit_start), points))
    points_mid: list[tuple[float, float]] = list(filter(lambda x: (x[0] > transit_start and x[0] < transit_end), points))
    points_right: list[tuple[float, float]] = list(filter(lambda x: (x[0] > transit_end), points))
    
    return points_left, points_mid, points_right