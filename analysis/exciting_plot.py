import pandas as pd
import matplotlib.pyplot as plt

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

print(star_names)

colour_map = ['purple' if star_name == 'OGLE-TR-10' else 'blue' for star_name in star_names]

print(complete_df)

plt.scatter(complete_df['full_light_curve_vg_slope'] / complete_df['t14_light_curve_vg_slope'], complete_df['full_light_curve_vg_intercept'] / complete_df['t14_light_curve_vg_intercept'], s=10, c=colour_map)
plt.xlabel('Full Slope / t14 Slope')
plt.ylabel('Full Intercept / t14 Intercept')
plt.title('Slope Ratio vs Intercept Ratio of VG Curves of OGLE stars')
plt.show()