import pandas as pd
import matplotlib.pyplot as plt

def plot_relation(df: pd.DataFrame, colour_map: list[str], xlabel='Non Transiting Region Average Degree', ylabel='Transiting Region Average Degree', title='', plot: bool = True):
    before_transit_avg_k = list(df['before_transit_avg_k'])
    during_transit_avg_k = list(df['during_transit_avg_k'])
    after_transit_avg_k = list(df['after_transit_avg_k'])
    
    before_transit_avg_k_1 = [1 for _ in range(len(before_transit_avg_k))]
    during_transit_avg_k_2 = [2 for _ in range(len(during_transit_avg_k))]
    after_transit_avg_k_3 = [3 for _ in range(len(after_transit_avg_k))]
    
    final_x = before_transit_avg_k_1 + during_transit_avg_k_2 + after_transit_avg_k_3
    final_y = before_transit_avg_k + during_transit_avg_k + after_transit_avg_k
    
    plt.scatter(final_x, final_y, s=5)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if plot:
        plt.show()
    else:
        plt.close()

        
        

def plot_relation_for_all_stars():
    df = pd.read_csv('../ogle_star_data/precomputed_data/avg_k_regionwise.csv')

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


plot_relation_for_all_stars()

