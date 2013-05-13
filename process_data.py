'''
This is calling the system functions from find_similarity.py respect to the needs of the system
'''
from find_similarities import *

#===============================================================================
# Test Code
#===============================================================================
# (data, indices) = read_csv_file('toy_data/sample_data.txt')
# data = read_csv_file('data/weight_matrix.txt')
# sim_mat = find_similarity_matrix(data)
# sim_mat = squareform(sim_mat)
# save_sim_mat(sim_mat,'processed_data/sim_mat.txt');
# indices = find_missings(data);
# recovered_data = fill_missings_with_entities(data, sim_mat, indices, 4)
# save_sim_mat(recovered_data,'processed_data/sim_mat_non_missing.txt');
# data

site_order = read_website_dict_file("data/site_order.txt")
websites = get_site_from_file([5,34,6],site_order)
# dist_v = find_dist_v_to_all(data[1,:], data)
  
# data_r = remove_v_from_data(data[1,:], data)
# sim_mat