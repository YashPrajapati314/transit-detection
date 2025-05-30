import pandas as pd
import matplotlib.pyplot as plt
from typing import Literal

def plot_relation(df: pd.DataFrame, colour_map: list[str], xlabel='Non Transiting Region Average Degree', ylabel='Transiting Region Average Degree', title='', plot: bool = True):
    non_transit_avg_k = list(df['non_transit_avg_k'])
    during_transit_avg_k = list(df['during_transit_avg_k'])
    plt.scatter(non_transit_avg_k, during_transit_avg_k, s=15, c=colour_map)
    star_names: list[str] = list(df['star'])
    star_ids: list[str] = list(map(lambda x: x.split('-')[-1], star_names))
    for i in range(len(star_ids)):
        plt.annotate(star_ids[i], (non_transit_avg_k[i], during_transit_avg_k[i]), textcoords="offset points", xytext=(0,5), ha='center', fontsize=6)
    plt.plot([5, 8], [5, 8])
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if plot:
        plt.show()
    else:
        plt.close()


def plot_slope_ratio_vs_inter_ratio(complete_df: pd.DataFrame, colour_map: list[str], plot: bool = True):
    plt.scatter(complete_df['full_light_curve_vg_slope'] / complete_df['t14_light_curve_vg_slope'], complete_df['full_light_curve_vg_intercept'] / complete_df['t14_light_curve_vg_intercept'], s=15, c=colour_map)
    plt.xlabel('Full Slope / t14 Slope')
    plt.ylabel('Full Intercept / t14 Intercept')
    plt.title('Slope Ratio vs Intercept Ratio of VG Curves of OGLE stars')
    if plot:
        plt.show()
    else:
        plt.close()
        

def plot_relation_for_all_stars(grandparent_directory: Literal['precomputed_data', 'binned_precomputed_data']):
    df = pd.read_csv(f'../ogle_star_data/{grandparent_directory}/avg_k_regionwise.csv')

    complete_df = pd.DataFrame({
        'star': df['star_name'],
        'before_transit_avg_k': df['before_transit_start'],
        'during_transit_avg_k': df['during_transit'],
        'after_transit_avg_k': df['after_transit_end'],
        'non_transit_avg_k': (df['before_transit_start'] + df['after_transit_end']) / 2,
    })

    star_names = complete_df['star'].tolist()

    # print(star_names)

    print(complete_df)

    confirmed_transits = ['OGLE-TR-10', 'OGLE-TR-56', 'OGLE-TR-111', 'OGLE-TR-132', 'OGLE-TR-182', 'OGLE-TR-211']

    colour_map = ['blue' if star_name in confirmed_transits else 'lightseagreen' for star_name in star_names]
    
    plot_relation(df=complete_df, colour_map=colour_map, title='Visibility Graph Average Degree of Non Transiting Region vs Transiting Region')
    
    complete_df.to_csv('temp.csv')


plot_relation_for_all_stars(grandparent_directory=...)

