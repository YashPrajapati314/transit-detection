import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np

def plot_relation(df: pd.DataFrame, colour_map: list[str], xlabel='Region', ylabel='Average Clustering Coefficient', title='', plot: bool = True):
    avg_clust_coeff_before_transit = list(df['avg_clust_coeff_before_transit'])
    avg_clust_coeff_during_transit = list(df['avg_clust_coeff_during_transit'])
    avg_clust_coeff_after_transit = list(df['avg_clust_coeff_after_transit'])
    
    # rows = df.iterrows()
    
    # for _, row in df.iterrows():
    #     plt.plot([1, 2, 3], [row['avg_clust_coeff_before_transit'], row['avg_clust_coeff_during_transit'], row['avg_clust_coeff_after_transit']])
    
    avg_clust_coeff_before_transit_1 = [1 for _ in range(len(avg_clust_coeff_before_transit))]
    avg_clust_coeff_during_transit_2 = [2 for _ in range(len(avg_clust_coeff_during_transit))]
    avg_clust_coeff_after_transit_3 = [3 for _ in range(len(avg_clust_coeff_after_transit))]
    
    final_x = avg_clust_coeff_before_transit_1 + avg_clust_coeff_during_transit_2 + avg_clust_coeff_after_transit_3
    final_y = avg_clust_coeff_before_transit + avg_clust_coeff_during_transit + avg_clust_coeff_after_transit
    
    plt.scatter(final_x, final_y, s=5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if plot:
        plt.show()
    else:
        plt.close()


def plot_3D(df: pd.DataFrame, colour_map: list[str], xlabel='Hurst Exponent', ylabel='Alpha', zlabel='Kappa', title='', plot: bool = True):
    hurst = list(df['hurst'])
    alpha = list(df['alpha'])
    kappa = list(df['kappa'])

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    norm = mcolors.Normalize(vmin=min(kappa), vmax=max(kappa))
    cmap = plt.get_cmap('plasma')
    colors = cmap(norm(kappa))
    
    star_names: list[str] = list(df['star_name'])
    
    col = []
    
    confirmed_transits = ['OGLE-TR-10', 'OGLE-TR-56', 'OGLE-TR-111', 'OGLE-TR-132', 'OGLE-TR-182', 'OGLE-TR-211']
    
    conditional_stars = []
    
    for i in range(len(hurst)):
        if (star_names[i] in confirmed_transits):
            col.append('red')
        elif (hurst[i] < 0.5 and alpha[i] < 0.024 and kappa[i] < 1):
            conditional_stars.append(star_names[i])
            col.append('blue')
        else:
            col.append('green')

    print()
    print(conditional_stars)
    
    # ax.grid()
    ax.scatter(hurst, alpha, kappa, c=col, s=25, alpha=0.8)
    
    # Generate ranges based on data
    x_range = np.linspace(min(hurst), max(hurst), 10)
    y_range = np.linspace(min(alpha), max(alpha), 10)
    z_range = np.linspace(min(kappa), max(kappa), 10)

    # Plane 1: X = 0.5 (YZ plane)
    Y1, Z1 = np.meshgrid(y_range, z_range)
    X1 = np.full_like(Y1, 0.5)
    ax.plot_surface(X1, Y1, Z1, alpha=0.2, color='blue', label='X=0.5')

    # Plane 2: Y = 0.024 (XZ plane)
    X2, Z2 = np.meshgrid(x_range, z_range)
    Y2 = np.full_like(X2, 0.024)
    ax.plot_surface(X2, Y2, Z2, alpha=0.2, color='green', label='Y=0.024')

    # Plane 3: Z = 1 (XY plane)
    X3, Y3 = np.meshgrid(x_range, y_range)
    Z3 = np.full_like(X3, 1)
    ax.plot_surface(X3, Y3, Z3, alpha=0.2, color='red', label='Z=1')

    ax.set_xlabel(xlabel, labelpad=10)
    ax.set_ylabel(ylabel, labelpad=10)
    ax.set_zlabel(zlabel, labelpad=10)
    ax.set_title(title)

    star_ids = [name.split('-')[-1] for name in star_names]
    offset = 0.025
    
    # ax.view_init(elev=30, azim=45)

    for i in range(len(star_ids)):
        ax.text(hurst[i], alpha[i], kappa[i]+offset, star_ids[i], fontsize=4, ha='center', va='bottom')

    if plot:
        plt.show()
    else:
        plt.close()
        

def plot_relation_for_all_stars():
    df = pd.read_csv('../ogle_star_data/OGLE_TR_H_ALPHA_KAPPA.csv')

    complete_df = pd.DataFrame({
        'star_name': df['ID'],
        'hurst': df['Hurst Exponent'],
        'alpha': df['alpha'],
        'kappa': df['KAPPA'],
    })

    star_names = complete_df['star_name'].tolist()

    confirmed_transits = ['OGLE-TR-10', 'OGLE-TR-56', 'OGLE-TR-111', 'OGLE-TR-132', 'OGLE-TR-182', 'OGLE-TR-211']

    colour_map = ['blue' if star_name in confirmed_transits else 'lightseagreen' for star_name in star_names]
    
    # plot_relation(df=complete_df, colour_map=colour_map, title='Visibility Graph Average Degree of Non Transiting Region vs Transiting Region')
    plot_3D(df=complete_df, colour_map=colour_map, title='Hurst vs Alpha vs Kappa')
    
    complete_df.to_csv('temp.csv')


plot_relation_for_all_stars()