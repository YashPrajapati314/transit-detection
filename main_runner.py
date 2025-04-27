from main_star_data_computer import compute_star_data

for id in range(1053, 1100):
    star_name = f'OGLE-TR-{id}'
    
    print(f'\n{star_name}\n')
    
    print(f'\nFull Curve\n')
    compute_star_data(star_name, compute_for_full_curve=True, write=True)
    
    print(f'\nt14 Region\n')
    compute_star_data(star_name, compute_for_full_curve=False, write=True)