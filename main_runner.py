from main_star_data_computer import compute_star_data

# compute_star_data(
#   'OGLE-TR-1001', compute_for_full_curve=True, write=True,
#   plot_deg_count_dist=False,
#   plot_degree_of_each_point=False,
#   plot_folded_curve_subset=False,
#   plot_log_log_dist=False,
#   plot_semi_log_dist=False
# )

# compute_star_data(
#   'OGLE-TR-1002', compute_for_full_curve=True, write=True,
#   plot_deg_count_dist=False,
#   plot_degree_of_each_point=False,
#   plot_folded_curve_subset=False,
#   plot_log_log_dist=False,
#   plot_semi_log_dist=False
# )

# compute_star_data(
#   'OGLE-TR-1001', compute_for_full_curve=True, write=True,
#   plot_deg_count_dist=False,
#   plot_degree_of_each_point=False,
#   plot_folded_curve_subset=False,
#   plot_log_log_dist=False,
#   plot_semi_log_dist=False
# )


# for id in range(1066, 1100):
#     star_name = f'OGLE-TR-{id}'
    
#     print(f'\n{star_name}\n')
    
#     print(f'\nFull Curve\n')
#     compute_star_data(star_name, compute_for_full_curve=True, write=True,
#                       plot_deg_count_dist=False,
#                       plot_degree_of_each_point=False,
#                       plot_folded_curve_subset=False,
#                       plot_log_log_dist=False,
#                       plot_semi_log_dist=False,
#                     )
    
#     print(f'\nt14 Region\n')
#     compute_star_data(star_name, compute_for_full_curve=False, write=True,
#                       plot_deg_count_dist=False,
#                       plot_degree_of_each_point=False,
#                       plot_folded_curve_subset=False,
#                       plot_log_log_dist=False,
#                       plot_semi_log_dist=False,
#                     )
    
# confirmed_transits = ['OGLE-TR-10', 'OGLE-TR-56', 'OGLE-TR-111', 'OGLE-TR-132', 'OGLE-TR-211']

# for star_name in confirmed_transits:
#     print(f'\n{star_name}\n')
    
#     print(f'\nFull Curve\n')
#     compute_star_data(star_name, compute_for_full_curve=True, write=True,
#                       plot_deg_count_dist=False,
#                       plot_degree_of_each_point=False,
#                       plot_folded_curve_subset=False,
#                       plot_log_log_dist=False,
#                       plot_semi_log_dist=False,
#                     )
    
#     print(f'\nt14 Region\n')
#     compute_star_data(star_name, compute_for_full_curve=False, write=True,
#                       plot_deg_count_dist=False,
#                       plot_degree_of_each_point=False,
#                       plot_folded_curve_subset=False,
#                       plot_log_log_dist=False,
#                       plot_semi_log_dist=False,
#                     )
    
# # # print(f'\n{"OGLE-TR-211"}\n')

# # # print(f'\nFull Curve\n')
# # # compute_star_data('OGLE-TR-211', compute_for_full_curve=True, write=True,
# # #                     plot_deg_count_dist=False,
# # #                     plot_degree_of_each_point=False,
# # #                     plot_folded_curve_subset=False,
# # #                     plot_log_log_dist=False,
# # #                     plot_semi_log_dist=False
# # #                 )

# # # print(f'\nt14 Region\n')
# # # compute_star_data('OGLE-TR-211', compute_for_full_curve=False, write=True,
# # #                     plot_deg_count_dist=False,
# # #                     plot_degree_of_each_point=False,
# # #                     plot_folded_curve_subset=False,
# # #                     plot_log_log_dist=False,
# # #                     plot_semi_log_dist=False
# # #                 )

    
# # # compute_star_data(star_name='OGLE-TR-10', compute_for_full_curve=True, write=False)
# # # compute_star_data(star_name='OGLE-TR-10', compute_for_full_curve=False, write=False)

# # # compute_star_data('OGLE-TR-1056', compute_for_full_curve=True, write=False,
# # #                   plot_folded_curve_subset=False,
# # #                   plot_deg_count_dist=False,
# # #                   plot_degree_of_each_point=False,
# # #                   plot_semi_log_dist=False)

# # # compute_star_data('OGLE-TR-1021', compute_for_full_curve=True, write=True)
# # # compute_star_data('OGLE-TR-1056', compute_for_full_curve=True, write=True)

# # # compute_star_data('OGLE-TR-211', compute_for_full_curve=True, write=False)
# # # compute_star_data('OGLE-TR-211', compute_for_full_curve=False, write=False)

# # # compute_star_data('OGLE-TR-10', compute_for_full_curve=False, write=True)
# # # compute_star_data('OGLE-TR-56', compute_for_full_curve=False, write=True)
# # # compute_star_data('OGLE-TR-111', compute_for_full_curve=False, write=True)
# # # compute_star_data('OGLE-TR-132', compute_for_full_curve=False, write=True)
# # # compute_star_data('OGLE-TR-211', compute_for_full_curve=False, write=True)


# # # compute_star_data('OGLE-TR-1001', compute_for_full_curve=True, write=True)

# confirmed_transits = ['OGLE-TR-10', 'OGLE-TR-56', 'OGLE-TR-111', 'OGLE-TR-132', 'OGLE-TR-211']

# for star in confirmed_transits:
#     compute_star_data(star, compute_for_full_curve=True, write=False,
#                       plot_deg_count_dist=False,
#                       plot_degree_of_each_point=False,
#                       plot_log_log_dist=False,
#                       plot_semi_log_dist=False
#                     )


for condition in [True, False]:
  for id in range(1001, 1100):
      star_name = f'OGLE-TR-{id}'
      
      star_data, points = compute_star_data(
        star_name, compute_for_full_curve=condition, write=True,
        bin_based_on_no_of_points=True,
        plot_deg_count_dist=False,
        plot_degree_of_each_point=False,
        plot_log_log_dist=False,
        plot_semi_log_dist=False,
        plot_folded_curve_subset=False
      )
      
  confirmed_transits = ['OGLE-TR-10', 'OGLE-TR-56', 'OGLE-TR-111', 'OGLE-TR-132', 'OGLE-TR-211']
      
  for star_name in confirmed_transits:
      star_data, points = compute_star_data(
        star_name, compute_for_full_curve=condition, write=True,
        bin_based_on_no_of_points=True,
        plot_deg_count_dist=False,
        plot_degree_of_each_point=False,
        plot_log_log_dist=False,
        plot_semi_log_dist=False,
        plot_folded_curve_subset=False
      )

# 1038
# 1052