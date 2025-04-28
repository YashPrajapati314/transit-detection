from main_star_data_computer import compute_star_data

# for id in range(1001, 1100):
#     star_name = f'OGLE-TR-{id}'
    
#     print(f'\n{star_name}\n')
    
#     print(f'\nFull Curve\n')
#     compute_star_data(star_name, compute_for_full_curve=True, write=False)
    
#     print(f'\nt14 Region\n')
#     compute_star_data(star_name, compute_for_full_curve=False, write=False)
    
# compute_star_data(star_name='OGLE-TR-10', compute_for_full_curve=True, write=False)
# compute_star_data(star_name='OGLE-TR-10', compute_for_full_curve=False, write=False)

compute_star_data('OGLE-TR-1021', compute_for_full_curve=True, write=False,
                  plot_deg_count_dist=False,
                  plot_degree_of_each_point=False,
                  plot_semi_log_dist=False)