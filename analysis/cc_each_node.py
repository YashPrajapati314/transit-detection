import pandas as pd
import matplotlib.pyplot as plt
from typing import Literal


def plot_each_point_details(df: pd.DataFrame, xlabel='Point Number', ylabel='Clustering Coefficient', title='', plot: bool = True):
    point_num = list(df['point_num'])
    clustering_coefficient = list(df['clustering_coefficient'])
    plt.scatter(point_num, clustering_coefficient, s=5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if plot:
        plt.show()
    else:
        plt.close()
        

def plot_relation_for_star(star_name: str, grandparent_directory: Literal['precomputed_data', 'binned_precomputed_data']):
    
    df = pd.read_csv(f'../ogle_star_data/{grandparent_directory}/t14_region_curve/Data of Each Point/{star_name}.csv')

    complete_df = pd.DataFrame({
        'point_num': df['Point Number'],
        'degree': df['Degree'],
        'clustering_coefficient': df['Clustering Coefficient'],
    })

    # star_names = complete_df['star'].tolist()

    # print(star_names)

    print(complete_df)

    # confirmed_transits = ['OGLE-TR-10', 'OGLE-TR-56', 'OGLE-TR-111', 'OGLE-TR-132', 'OGLE-TR-182', 'OGLE-TR-211']

    # colour_map = ['blue' if star_name in confirmed_transits else 'lightseagreen' for star_name in star_names]
    
    # plot_relation(df=complete_df, colour_map=colour_map, title='Visibility Graph Average Degree of Non Transiting Region vs Transiting Region')
    plot_each_point_details(df=complete_df, title=f'{star_name} Clustering Coefficient of Each Point')
    
    complete_df.to_csv('temp.csv')


plot_relation_for_star('OGLE-TR-1021', grandparent_directory=...)