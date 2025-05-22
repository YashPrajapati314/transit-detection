import numpy as np
import pandas as pd
from main_star_data_computer import compute_star_data

file_path = './ogle_star_data/star_period_and_transit_time.csv'

df = pd.read_csv(file_path)

confirmed_transits = ['OGLE-TR-10', 'OGLE-TR-56', 'OGLE-TR-111', 'OGLE-TR-132', 'OGLE-TR-211']
other_stars = [f'OGLE-TR-{star_id}' for star_id in range(1001, 1100)]
all_stars = other_stars + confirmed_transits

data_to_add = {}

for star in all_stars:
  print(star)
  star_data, points = compute_star_data(
    star, compute_for_full_curve=True, write=False,
    plot_folded_curve_subset=False,
    plot_deg_count_dist=False,
    plot_degree_of_each_point=False,
    plot_log_log_dist=False,
    plot_semi_log_dist=False
  )

  half_of_transit_period_in_hours = star_data.t14_in_days / 2 * 24

  points_before_transit = len(list(filter(lambda point: point[0] < -half_of_transit_period_in_hours, points)))
  points_during_transit = len(list(filter(lambda point: point[0] >= -half_of_transit_period_in_hours and point[0] <= half_of_transit_period_in_hours, points)))
  points_after_transit = len(list(filter(lambda point: point[0] > half_of_transit_period_in_hours, points)))
  total_number_of_points = len(points)

  columns_to_add = {
    'no_of_points_before_transit': points_before_transit,
    'no_of_points_during_transit': points_during_transit,
    'no_of_points_after_transit': points_after_transit,
    'total_number_of_points': total_number_of_points
  }
  
  data_to_add[star] = columns_to_add
  

additional_df = pd.DataFrame.from_dict(data_to_add, orient='index').reset_index()
additional_df.rename(columns={'index': 'ID'}, inplace=True)

merged_df = df.merge(additional_df, on='ID', how='left')

merged_df.to_csv('augmented_star_data.csv', index=False)

print(merged_df.head())