import pandas as pd
import matplotlib.pyplot as plt
from typing import Literal

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

def plot_non_transit_vs_transit(df: pd.DataFrame, colour_map: list[str], xlabel='Non Transiting Region Average Clustering Coefficient', ylabel='Transiting Region Average Clustering Coefficient', title='', plot: bool = True):
    non_transit_avg_clust_coeff = list(df['avg_clust_coeff_non_transit'])
    during_transit_avg_clust_coeff = list(df['avg_clust_coeff_during_transit'])
    plt.scatter(non_transit_avg_clust_coeff, during_transit_avg_clust_coeff, s=15, c=colour_map)
    star_names: list[str] = list(df['star'])
    star_ids: list[str] = list(map(lambda x: x.split('-')[-1], star_names))
    for i in range(len(star_ids)):
        plt.annotate(star_ids[i], (non_transit_avg_clust_coeff[i], during_transit_avg_clust_coeff[i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=6)
    plt.plot([0.7, 0.8], [0.7, 0.8])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if plot:
        plt.show()
    else:
        plt.close()
        

def plot_relation_for_all_stars(grandparent_directory: Literal['precomputed_data', 'binned_precomputed_data']):
    df = pd.read_csv(f'../ogle_star_data/{grandparent_directory}/Regionwise Data of Each Point/Average Data of Each Star.csv')

    complete_df = pd.DataFrame({
        'star': df['star_name'],
        'avg_degree_before_transit': df['avg_degree_before_transit'],
        'avg_degree_during_transit': df['avg_degree_during_transit'],
        'avg_degree_after_transit': df['avg_degree_after_transit'],
        'avg_clust_coeff_before_transit': df['avg_clust_coeff_before_transit'],
        'avg_clust_coeff_during_transit': df['avg_clust_coeff_during_transit'],
        'avg_clust_coeff_after_transit': df['avg_clust_coeff_after_transit'],
        'avg_degree_non_transit': (df['avg_degree_before_transit'] + df['avg_degree_after_transit']) / 2,
        'avg_clust_coeff_non_transit': (df['avg_clust_coeff_before_transit'] + df['avg_clust_coeff_after_transit']) / 2,
    })

    star_names = complete_df['star'].tolist()
    
    print(star_names)

    print(star_names)

    print(complete_df)

    confirmed_transits = ['OGLE-TR-10', 'OGLE-TR-56', 'OGLE-TR-111', 'OGLE-TR-132', 'OGLE-TR-182', 'OGLE-TR-211']

    colour_map = ['blue' if star_name in confirmed_transits else 'lightseagreen' for star_name in star_names]
    
    # plot_relation(df=complete_df, colour_map=colour_map, title='Visibility Graph Average Degree of Non Transiting Region vs Transiting Region')
    plot_non_transit_vs_transit(df=complete_df, colour_map=colour_map, title='Visibility Graph Average Clustering Coefficient of Non Transiting Region vs Transiting Region')
    
    complete_df.to_csv('temp.csv')


plot_relation_for_all_stars()
# plot_non_transit_vs_transit()