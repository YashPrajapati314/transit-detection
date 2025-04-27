import pandas as pd
import matplotlib.pyplot as plt

def plot_slope_vs_inter(df: pd.DataFrame, colour_map: list[str], xlabel='Slope', ylabel='Intercept', title='', plot: bool = True):
    plt.scatter(df['slope'], df['intercept'], s=15, c=colour_map)
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
        

def plot_relation_for_all_stars():
    df_t14 = pd.read_csv('../ogle_star_data/precomputed_data/t14_region_curve/Line Fit/line_fit_results.csv')
    df_full = pd.read_csv('../ogle_star_data/precomputed_data/full_curve/Line Fit/line_fit_results.csv')

    df_t14.rename(columns={'Unnamed: 0': 'star'}, inplace=True)
    df_full.rename(columns={'Unnamed: 0': 'star'}, inplace=True)
    df_t14.set_index('star', inplace=True)
    df_full.set_index('star', inplace=True)

    complete_df = pd.DataFrame({
        'star': df_full.index,
        'full_light_curve_vg_slope': df_full['slope'],
        'full_light_curve_vg_intercept': df_full['intercept'],
        't14_light_curve_vg_slope': df_t14['slope'],
        't14_light_curve_vg_intercept': df_t14['intercept']
    })

    star_names = complete_df['star'].tolist()

    # print(star_names)

    print(complete_df)

    confirmed_transits = ['OGLE-TR-10', 'OGLE-TR-56']

    colour_map = ['blue' if star_name in confirmed_transits else 'lightseagreen' for star_name in star_names]
    
    plot_slope_vs_inter(df=df_t14, colour_map=colour_map, title='Slope vs Intercept of t14 Region VG Curves of OGLE stars')
    plot_slope_vs_inter(df=df_full, colour_map=colour_map, title='Slope vs Intercept of Full VG Curves of OGLE stars')
    plot_slope_ratio_vs_inter_ratio(complete_df=complete_df, colour_map=colour_map)
    

plot_relation_for_all_stars()