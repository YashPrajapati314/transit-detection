import matplotlib.pyplot as plt
import math
from collections import Counter

def plot_visibility_graph(points, graph):
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

    plt.xlabel("X", fontsize=13)
    plt.ylabel("Y", fontsize=13)
    plt.title("Visibility Graph", fontsize=14)
    plt.grid(True, linestyle="--")
    plt.show()



def plot_light_curve(star_name: str, points: list[tuple[float, float]]):
    plt.figure(figsize=(8, 5))
    x, y = zip(*points)
    plt.scatter(x, y, s=3, color='black')
    plt.xlabel("Orbital Phase", fontsize=13)
    plt.ylabel("I Magnitude", fontsize=13)
    plt.title(f"{star_name} Phase-Folded Light Curve", fontsize=14)
    plt.gca().invert_yaxis()
    # plt.grid(True)
    plt.tight_layout()
    plt.show()