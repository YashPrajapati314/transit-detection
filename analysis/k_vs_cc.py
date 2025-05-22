import pandas as pd
import matplotlib.pyplot as plt


def plot_each_point_details(df: pd.DataFrame, xlabel='Degree', ylabel='Clustering Coefficient', title='', plot: bool = True):
    degree = list(df['degree'])
    clustering_coefficient = list(df['clustering_coefficient'])
    plt.scatter(degree, clustering_coefficient, s=5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if plot:
        plt.show()
    else:
        plt.close()
        

def plot_relation_for_star(star_name: str):
    
    df = pd.read_csv(f'../ogle_star_data/precomputed_data/t14_region_curve/Data of Each Point/{star_name}.csv')
    df = pd.read_csv(f'../ogle_star_data/precomputed_data/full_curve/Data of Each Point/{star_name}.csv')

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
    plot_each_point_details(df=complete_df, title=f'{star_name} Degree vs Clustering Coefficient of Each Point')
    
    complete_df.to_csv('temp.csv')


plot_relation_for_star('OGLE-TR-1089')