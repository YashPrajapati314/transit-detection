from main_star_data_computer import compute_star_data

for id in range(1001, 1100):
    star_name = f'OGLE-TR-{id}'

    compute_star_data(star_name, compute_for_full_curve=True, write=True)
    compute_star_data(star_name, compute_for_full_curve=False, write=True)