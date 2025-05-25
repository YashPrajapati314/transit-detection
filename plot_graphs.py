import matplotlib.pyplot as plt
import math
from typing import Literal

def plot_visibility_graph(points, graph, full_curve: bool, star_name: str):
    plt.figure(figsize=(8, 6))
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    plt.scatter(x_coords, y_coords)
    n = len(points)
    for i in range(n):
        for j in range(i + 1, n):  
            if graph[i][j] == 1:
                x_vals = [points[i][0], points[j][0]]
                y_vals = [points[i][1], points[j][1]]
                plt.plot(x_vals, y_vals)
                
    curve = full_curve

    plt.xlabel("Time (Phase Folded) [h]", fontsize=13)
    plt.ylabel("Infrared Magnitude (Negated)", fontsize=13)
    
    curve = 'Full Curve' if full_curve else 't14 Region'
    
    plt.title(f"{star_name} {curve} Visibility Graph", fontsize=14)
    plt.grid(True, linestyle="--")
    plt.show()



def plot_light_curve(star_name: str, points: list[tuple[float, float]], use_full_curve: bool, grandparent_directory: Literal['binned_precomputed_data', 'precomputed_data'], write: bool, plot: bool = True):
    plt.figure(figsize=(8, 5))
    x, y = zip(*points)
    plt.scatter(x, y, s=3, color='black')
    plt.xlabel("Orbital Phase", fontsize=13)
    plt.ylabel("I Magnitude", fontsize=13)
    
    full_or_t14 = 'Full' if use_full_curve else 't14 Region'

    plt.title(f"{star_name} Phase-Folded Light Curve ({full_or_t14})", fontsize=14)
    plt.gca().invert_yaxis()
    # plt.grid(True)
    plt.tight_layout()
    
    if write:
        if use_full_curve:
            plt.savefig(f'./ogle_star_data/{grandparent_directory}/full_curve/Phased Folded Light Curve Points/Plots/{star_name}.png')
        else:
            plt.savefig(f'./ogle_star_data/{grandparent_directory}/t14_region_curve/Phased Folded Light Curve Points/Plots/{star_name}.png')
    
    if plot:
        plt.show()