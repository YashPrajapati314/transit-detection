import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class StarData:
    def __init__(self, star_name: str, light_curve: pd.DataFrame, period: float, transit_epoch: float, margin_in_days: float):
        self.star_name = star_name
        self.light_curve = light_curve
        self.period = period
        self.transit_epoch = transit_epoch
        self.margin_in_days = margin_in_days

def read_star_data(star_name: str, main_directory = 'ogle_star_data', light_curve_directory='light_curves_csv', star_curve_info_filename = 'star_period_and_transit_time.csv', plot=False):
    star_curve_info = pd.read_csv(os.path.join(main_directory, star_curve_info_filename))
    
    light_curve_data = pd.read_csv(os.path.join(main_directory, light_curve_directory, f'{star_name}.csv'))

    time = light_curve_data['T']
    mag = light_curve_data['Flux']
    err = light_curve_data['E']
    
    
    star_of_interest = star_curve_info[star_curve_info['ID'] == star_name]
    
    
    transit_epoch = float(star_of_interest['transit_epoch'].item())
    period = float(star_of_interest['period'].item())
    margin_in_days = float(star_of_interest['t14'].item())
    

    # period = 50.23996  # days
    # t0 = 5394.4032     # HJD - 2450000
    # period = 2.1093182924  # days
    # t0 = 5378.1832438945     # HJD - 2450000

    # Phase-folded plot
    # phase = (((time - t0 + 0.5 * period) % period) / period) - 0.5
    
    if plot == True:
        plt.scatter(time, mag, s=3, color='black')
        plt.xlabel("Orbital Phase")
        plt.ylabel("I Magnitude")
        plt.title("OGLE-TR-1021 Original Light Curve")
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        
    
    star_data = StarData(star_name, light_curve_data, period, transit_epoch, margin_in_days)
    
    return star_data



def get_folded_curve_subset(star_data: StarData, use_full_curve: bool = True, plot=True):
    star_name = star_data.star_name
    light_curve = star_data.light_curve
    period = star_data.period
    transit_epoch = star_data.transit_epoch
    margin = star_data.margin_in_days

    # Access columns using column names
    time = light_curve["T"]
    mag = light_curve["Flux"]
    err = light_curve["E"]

    # Phase-folded plot
    # phase = (((time - t0 + 0.5 * period) % period) / period) - 0.5


    phase = (((time - transit_epoch) + margin) % period) - margin
    
    if use_full_curve:
        pass
        subset_phase = phase * 24
        subset_mag = light_curve["Flux"]
    else:
        subset_phase = phase[(phase > -margin) & (phase < margin)] * 24
        subset_time = light_curve[(phase > -margin) & (phase < margin)]["T"]
        subset_mag = light_curve[(phase > -margin) & (phase < margin)]["Flux"]
        subset_err = light_curve[(phase > -margin) & (phase < margin)]["E"]
    
    # print(subset_margin)
    # print(subset_period)

    # print(phase)
    # print()
    # print([(phase > -10) & (phase < 10)])
    # phase = ((time - t0) % period) / period
    # plt.scatter(phase, mag, s=3, color='black')
    
    plt.figure(figsize=(8, 5))
    plt.scatter(subset_phase, subset_mag, s=3, color='black')
    plt.xlabel("Orbital Phase", fontsize=13)
    plt.ylabel("I Magnitude", fontsize=13)
    plt.title(f"{star_name} Phase-Folded Light Curve", fontsize=14)
    plt.gca().invert_yaxis()
    # plt.grid(True)
    plt.tight_layout()
    
    if use_full_curve:
        plt.savefig(f'./ogle_star_data/precomputed_data/full_curve/Phased Folded Light Curve Points/Plots/{star_name}.png')
    else:
        plt.savefig(f'./ogle_star_data/precomputed_data/t14_region_curve/Phased Folded Light Curve Points/Plots/{star_name}.png')

    plt.show()
    
    subset_curve_points: list[tuple[float, float]] = [(subset_phase.iloc[i], subset_mag.iloc[i]) for i in range(len(subset_phase))]
    
    subset_curve_points.sort(key=lambda x: x[0])
    
    return subset_curve_points
