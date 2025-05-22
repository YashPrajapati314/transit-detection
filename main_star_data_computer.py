import os
import pandas as pd
from compute_visibility_graph import visibility_graph, visibility_graph_range_wise, points_range_wise
from plot_graphs import plot_visibility_graph, plot_light_curve
from compute_degree_distribution import degree_count_distribution, degree_count_probability_distribution, degrees_of_points, clustering_coefficients_of_points
from plot_degree_distribution import *
from star_data_reader_plotter import get_folded_curve_subset, read_star_data
from fit_line import line_fit, my_line_fit_algorithm
from star_data_preprocessor import *

def create_file_and_write_avg_k_for_each_region(star_name: str, avg_k_left: float, avg_k_mid: float, avg_k_right: float, parent_directory: str):
    new_data = {
        'star_name': star_name,
        'before_transit_start': avg_k_left,
        'during_transit': avg_k_mid,
        'after_transit_end': avg_k_right
    }
    relative_path = f'./ogle_star_data/precomputed_data/avg_k_regionwise.csv'
    if os.path.exists(relative_path):
        df = pd.read_csv(relative_path, index_col=0)
    else:
        df = pd.DataFrame(columns=new_data.keys())

    df.loc[star_name] = new_data

    df.to_csv(relative_path)


def create_file_and_write_plot_data(star_name: str, points: list[tuple[int | float, int | float]], plot_type: str, x_axis: str, y_axis: str, parent_directory: str):
    columns = [x_axis, y_axis]
    df = pd.DataFrame(columns=columns, data=points)
    df.to_csv(f'./ogle_star_data/precomputed_data/{parent_directory}/{plot_type}/{star_name}.csv', index=False)


def create_file_and_write_line_fit_data(star_name: str, intercept, slope, sum_of_square_of_fit_errors, sum_of_square_of_all_errors, start_point, end_point, parent_directory: str, semilog: bool = False):
    new_data = {
        'intercept': intercept,
        'slope': slope,
        'sum_of_square_of_fit_errors': sum_of_square_of_fit_errors,
        'sum_of_square_of_all_errors': sum_of_square_of_all_errors,
        'start_range': start_point,
        'end_range': end_point
    }
    
    if semilog:
        relative_path = f'./ogle_star_data/precomputed_data/{parent_directory}/Line Fit Semilog/line_fit_results.csv'
    else:
        relative_path = f'./ogle_star_data/precomputed_data/{parent_directory}/Line Fit/line_fit_results.csv'
    
    if os.path.exists(relative_path):
        df = pd.read_csv(relative_path, index_col=0)
    else:
        df = pd.DataFrame(columns=new_data.keys())

    df.loc[star_name] = new_data

    df.to_csv(relative_path)


def create_file_and_write_data_for_each_point(star_name: str, directory: str, x_coords: list[float], y_coords: list[float], degrees: list[tuple[int, int]], clustering_coefficients: list[float]):
    if len(x_coords) == len(y_coords) == len(degrees) == len(clustering_coefficients):
        star_file_path = os.path.join(directory, f'{star_name}.csv')
        n = len(x_coords)
        columns = ['Point Number', 'X Coords', 'Y Coords', 'Degree', 'Clustering Coefficient']
        data = [[i, x_coords[i], y_coords[i], degrees[i][1], clustering_coefficients[i]] for i in range(n)]
        df = pd.DataFrame(data=data, columns=columns)
        df.to_csv(star_file_path, index=False)
        
        avg_degree = sum([degrees[i][1] for i in range(n)]) / n
        avg_clust_coeff = sum(clustering_coefficients) / n
        
        avg_file_path = os.path.join(directory, 'Average Data of Each Star.csv')
        
        new_row = {
            'avg_degree': avg_degree,
            'avg_clust_coeff': avg_clust_coeff
        }
        
        if os.path.exists(avg_file_path):
            df = pd.read_csv(avg_file_path, index_col=0)
        else:
            df = pd.DataFrame(columns=new_row.keys())
            df.index.name = 'star_name'

        df.loc[star_name] = new_row
        
        df.to_csv(avg_file_path)
    else:
        print('Length mismatch error')

def create_file_and_write_data_for_each_point_regionwise(star_name: str, directory: str, before_transit_data: tuple[list[tuple[float, float]], list[int], list[float]], during_transit_data: tuple[list[tuple[float, float]], list[int], list[float]], after_transit_data: tuple[list[tuple[float, float]], list[int], list[float]]):
    data_names = ['before-transit', 'during-transit', 'after-transit']
    data = [before_transit_data, during_transit_data, after_transit_data]
    avg_degree: list[float] = [None, None, None]
    avg_clust_coeff: list[float] = [None, None, None]
    
    for i in range(len(data)):
        star_file_path = os.path.join(directory, f'{star_name}_{data_names[i]}.csv')
        columns = ['Point Number', 'X Coords', 'Y Coords', 'Degree', 'Clustering Coefficient']
        point_coords = data[i][0]
        degrees = data[i][1]
        clustering_coefficients = data[i][2]
        
        if len(point_coords) == len(degrees) == len(clustering_coefficients):
            n = len(point_coords)
            rows = [[i, *point_coords[i], degrees[i], clustering_coefficients[i]] for i in range(n)]
            
            df = pd.DataFrame(data=rows, columns=columns)
            df.to_csv(star_file_path, index=False)
            
            avg_degree[i] = sum(degrees) / len(degrees)
            avg_clust_coeff[i] = sum(clustering_coefficients) / len(clustering_coefficients)
        else:
            print('Length mismatch error')
            
    avg_file_path = os.path.join(directory, 'Average Data of Each Star.csv')
        
    new_row = {
        'avg_degree_before_transit': avg_degree[0],
        'avg_clust_coeff_before_transit': avg_clust_coeff[0],
        'avg_degree_during_transit': avg_degree[1],
        'avg_clust_coeff_during_transit': avg_clust_coeff[1],
        'avg_degree_after_transit': avg_degree[2],
        'avg_clust_coeff_after_transit': avg_clust_coeff[2]
    }
    
    if os.path.exists(avg_file_path):
        df = pd.read_csv(avg_file_path, index_col=0)
    else:
        df = pd.DataFrame(columns=new_row.keys())
        df.index.name = 'star_name'

    df.loc[star_name] = new_row
    
    df.to_csv(avg_file_path)
    


def compute_star_data(star_name: str, compute_for_full_curve: bool, write: bool, bin_based_on_width: bool = False, bin_based_on_no_of_points: bool = False, bin_width: bool = None, recompute_star_data: bool = False, plot_folded_curve_subset: bool = True, plot_degree_of_each_point: bool = True, plot_deg_count_dist: bool = True, plot_semi_log_dist: bool = True, plot_log_log_dist: bool = True):
    
    if compute_for_full_curve:
        parent_directory = 'full_curve'
    else:
        parent_directory = 't14_region_curve'
    
    star_data = read_star_data(star_name)
    
    points = get_folded_curve_subset(star_data, use_full_curve=compute_for_full_curve, plot=plot_folded_curve_subset)
    
    points = center_transit_in_the_curve(points, period_in_hours=(star_data.period * 24))
    
    if bin_based_on_no_of_points:
        final_points = custom_binning_with_in_transit_priority(points=points, t14_in_days=star_data.t14_in_days, num_in_transit_bins=80, num_out_of_transit_bins=800)
    elif bin_based_on_width:
        final_points = bin_points(points, bin_width=bin_width)
    else:
        final_points = points
        

    if plot_folded_curve_subset:
        plot_light_curve(star_name, points)
        plot_light_curve(star_name, final_points)
    
    return star_data, final_points
    
    x, y = zip(*points)
    n = len(x)
    new_y = [val*-1 for val in y]
    new_points = [(x[i], new_y[i]) for i in range(n)]
    
    
    plot_types = ['Phased Folded Light Curve Points', 'Degree of Each Point', 'Degree Probability Distribution', 'Semilog Degree Probability Distribution', 'Log Log Degree Probability Distribution']
    
    
    points_for_rangewise_vg = get_folded_curve_subset(star_data, use_full_curve=True, plot=False)
    
    if compute_for_full_curve == True:
        x_rangewise, y_rangewise = zip(*points_for_rangewise_vg)
        n_rangewise = len(x_rangewise)
        new_y_rangewise = [val*-1 for val in y_rangewise]
        new_points_rangewise = [(x_rangewise[i], new_y_rangewise[i]) for i in range(n_rangewise)]


        left_points, mid_points, right_points = points_range_wise(star_name, new_points_rangewise, t14=star_data.t14_in_days)
        
        left_graph, mid_graph, right_graph = visibility_graph_range_wise(star_name, new_points_rangewise, full_curve=True, t14=star_data.t14_in_days)

        deg_left_points = degrees_of_points(left_graph)
        deg_mid_points = degrees_of_points(mid_graph)
        deg_right_points = degrees_of_points(right_graph)
        
        avg_k_left = sum(deg_left_points) / len(deg_left_points)
        avg_k_mid = sum(deg_mid_points) / len(deg_mid_points)
        avg_k_right = sum(deg_right_points) / len(deg_right_points)
        
        clust_coeff_left_points = clustering_coefficients_of_points(left_graph)
        clust_coeff_mid_points = clustering_coefficients_of_points(mid_graph)
        clust_coeff_right_points = clustering_coefficients_of_points(right_graph)
        
        
        print()
        print(star_name)
        print(avg_k_left, avg_k_mid, avg_k_right)
        print()
        
        data_of_each_point_regionwise_directory = f'./ogle_star_data/precomputed_data/Regionwise Data of Each Point/'
    
    data_of_each_point_directory = f'./ogle_star_data/precomputed_data/{parent_directory}/Data of Each Point/'
    
    degree_of_each_point_file_path = f'./ogle_star_data/precomputed_data/{parent_directory}/Degree of Each Point/{star_name}.csv'
    
    if os.path.exists(degree_of_each_point_file_path) and not recompute_star_data:
        print(f'Fetching data from {degree_of_each_point_file_path}')
        df = pd.read_csv(degree_of_each_point_file_path)
        degree_of_each_point: list[tuple[int, int]] = list(df.itertuples(index=False, name=None))
        temp = plot_degree_vs_point_number([val[1] for val in degree_of_each_point], star_name, full_curve=compute_for_full_curve, plot=plot_degree_of_each_point, write=write)
    else:
        graph = visibility_graph(star_name=star_name, points=new_points, full_curve=compute_for_full_curve)
        # plot_visibility_graph(new_points, graph)
        
        deg_points = degrees_of_points(graph)
        
        degree_of_each_point = plot_degree_vs_point_number(deg_points, star_name, full_curve=compute_for_full_curve, plot=plot_degree_of_each_point, write=write)
        
        # plot_visibility_graph(points, graph)
        
    graph = visibility_graph(star_name=star_name, points=new_points, full_curve=compute_for_full_curve)
    deg_points = degrees_of_points(graph)
    
    clustering_coefficient_of_each_point: list[float] = clustering_coefficients_of_points(graph, deg_points)

    degree_dist = degree_count_distribution(degree_of_each_point)
    
    print(degree_dist)

    degree_prob_dist = degree_count_probability_distribution(degree_of_each_point)
    
    deg_count_dist = plot_degree_count_distribution(degree_prob_dist, star_name, full_curve=compute_for_full_curve, plot=plot_deg_count_dist, write=write)

    semi_log_dist = semi_log_plot_degree_distribution(degree_prob_dist, star_name, full_curve=compute_for_full_curve, plot=plot_semi_log_dist, write=write)

    log_log_dist = log_log_plot_degree_distribution(degree_prob_dist, star_name, full_curve=compute_for_full_curve, plot=plot_log_log_dist, write=write)
    
    # midpoint_near_point_number, points_to_consider_on_each_side = input('Midpoint near and neigbours: ').split()
    
    # my_line_fit_algorithm(star_name, log_log_dist, float(midpoint_near_point_number), int(points_to_consider_on_each_side))
    
    # 2.196
    # my_line_fit_algorithm(star_name, log_log_dist, 2.196, 3)
    if compute_for_full_curve:
        midpoint_near, points_to_consider_on_each_side = 2.196, 3
    else:
        midpoint_near, points_to_consider_on_each_side = 1.5, 2
        
    # my_line_fit_algorithm(star_name, log_log_dist, midpoint_near, points_to_consider_on_each_side)
    # my_line_fit_algorithm(star_name, log_log_dist, midpoint_near, points_to_consider_on_each_side, bring_inline_points_closer=not(compute_for_full_curve))
    
    for_semilog = True
    
    # range_str = input('Taking space separated input for range start and end (a and b): ')
    
    # if range_str == '':
    #     a, b = 1.5, 2.5
    # else:
    #     a, b = tuple(map(float, range_str.split()))    

    if compute_for_full_curve:
        a = 0
        b = 25
    else:
        a = 0
        b = 15
    
    # intercept, slope, sum_of_square_of_fit_errors, sum_of_square_of_all_errors = line_fit(star_name, semi_log_dist, full_curve=compute_for_full_curve, filter_condition='between_a_and_b', a=a, b=b, semilog=for_semilog, write=True)
    
    # intercept, slope, sum_of_square_of_fit_errors, sum_of_square_of_all_errors = line_fit(star_name, log_log_dist, full_curve=compute_for_full_curve, filter_condition='between_a_and_b', a=a, b=b)
    # intercept, slope, sum_of_square_of_fit_errors, sum_of_square_of_all_errors, all_signed_errors = my_line_fit_algorithm(star_name, semi_log_dist, None, None, full_curve=compute_for_full_curve, semilog=True)
    
    if write:
            
        # create_file_and_write_plot_data(star_name, points, plot_type='Phased Folded Light Curve Points', x_axis='Time', y_axis='Magnitude', parent_directory=parent_directory)
            
        # create_file_and_write_plot_data(star_name, degree_of_each_point, plot_type='Degree of Each Point', x_axis='Point Number', y_axis='Degree', parent_directory=parent_directory)
        
        # create_file_and_write_plot_data(star_name, deg_count_dist, plot_type='Degree Probability Distribution', x_axis='Degree', y_axis='Probability', parent_directory=parent_directory)
        
        # create_file_and_write_plot_data(star_name, semi_log_dist, plot_type='Semilog Degree Probability Distribution', x_axis='Degree', y_axis='Log(Probability)', parent_directory=parent_directory)
        
        # create_file_and_write_plot_data(star_name, log_log_dist, plot_type='Log Log Degree Probability Distribution', x_axis='Log(Degree)', y_axis='Log(Probability)', parent_directory=parent_directory)
        
        # create_file_and_write_line_fit_data(star_name, intercept, slope, sum_of_square_of_fit_errors, sum_of_square_of_all_errors, a, b, parent_directory, semilog=for_semilog)

        # create_file_and_write_avg_k_for_each_region(star_name, avg_k_left, avg_k_mid, avg_k_right, parent_directory)
        
        # create_file_and_write_data_for_each_point(star_name, data_of_each_point_directory, x, new_y, degree_of_each_point, clustering_coefficient_of_each_point)
        
        # if compute_for_full_curve == True:
        #     create_file_and_write_data_for_each_point_regionwise(star_name, data_of_each_point_regionwise_directory, (left_points, deg_left_points, clust_coeff_left_points), (mid_points, deg_mid_points, clust_coeff_mid_points), (right_points, deg_right_points, clust_coeff_right_points))
        
        pass
    
    return star_data, points