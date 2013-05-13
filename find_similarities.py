from numpy import *
from itertools import *
from scipy.spatial.distance import *
from collections import defaultdict
import csv
import pdb

'''
 cosine dist between vector a and b
 
 a         - row vector
 b         - row vector
 
 result    - distance of the vectors
'''
def cosine_dist(a,b):
    if len(a) != len(b):
        raise ValueError, "a and b must be same length"
    numerator = sum(tup[0]*tup[1] for tup in izip(a,b))
    denominator1 = sum(num**2 for num in a)
    denominator2 = sum(num**2 for num in b)
    result = 1-numerator / (sqrt(denominator1)*sqrt(denominator2))
    return result

'''
finds distance vector of row vector v to all 
row vectors of data

v         - vector 
data      - is data_matrix

distances - distance vector of row vector v
'''        
def find_dist_v_to_all(v, data):
    nom = sum(data*v, axis=1)
    denom1 = sum(v**2)
    denom2 = np.sum(data**2, axis=1)
    dist = 1 - (nom / (sqrt(denom1)*sqrt(denom2)))
    return dist

'''
finds the similarity matrix of row vectors

data     - data matrix

sim_mat  - similarity matrix
'''
def find_similarity_matrix(data):
    distances = pdist(data,'cosine')
    return distances

'''
read data from file and slice the id column 

data_name - string name of file

data_reduced - remaining data after first column
index_column - ids of columns
'''        
def read_csv_file(data_name):
    data = loadtxt(data_name, delimiter=',')
    return data
 
'''
find most similar vector to v at data matrix by calculating 
distances on fly

v         - vector
data      - data_matrix

index_min - row index of the most similar vector 
'''
def find_matching_by_calculation(v, data):
    distances = find_dist_v_to_all(v, data)
    index_min = distances.index(min(distances[:]))
    return index_min

'''
find the similar item from square similarity matrix
given the query item id

id              - query item and ids starts from 1
squared_sim_mat - similarity matrix
n               - number of required similar items

sim_item_indices - indices of most similar n items
'''
def find_similars_from_id(id, squared_sim_mat, n):
    real_index = id-1;
    sim_vec = squared_sim_mat[real_index,:]
    sim_item_indices = []
    for i in range(n):
        sim_item_index = where(sim_vec==min(sim_vec[nonzero(sim_vec != 0)]))[0][0]
        sim_vec[sim_item_index] = float("inf")
        sim_item_indices.append(sim_item_index);

    return sim_item_indices

'''
Remove given vector from matrix
v - row vector
data - data matrix

data_removed - data matrix v is removed
'''    
def remove_v_from_data(v, data):
    size = data.shape
    data_removed = setdiff1d(data,v).reshape(size[0]-1, size[1])
    return data_removed

'''
Saves similarity values as squeezed or squared
'''
def save_sim_mat(sim_mat,file_name):
    savetxt(file_name,sim_mat,delimiter=',')

def save_sim_mat_squared(sim_mat,file_name):
    squared_mat = squareform(sim_mat)
    savetxt(file_name,squared_mat,delimiter=',')

#=============================
# PROCESS MISSING INFORMATION
#=============================
'''
Finds missing values indicated by -1 at the data matrix
and returns index of

data    - data matrix nxd n is #entities d is # users

dict   - dictionary where missing rows are sub array values
indexed by row index of the entity at data matrix
'''
def find_missings(data):
    index_row, index_col = nonzero(data == -1)
    indices = zip(index_row, index_col)
    dict = defaultdict(list)
    for row,col in indices:
        dict[row].append(col)
    return dict

'''
Fill the missing values given by the index argument with 
data matrix respecting most similar n websites

data        - data matrix nxd n is #entities d is # users
sim_mat     - squared similarity matrix
indices     - index values of entries as 2 item tuples as 
row and column index
n           - number of users to define the missing value 

filled_data - data rectified by filling on the missing values

!!!! There is a bug that includes missing values where finding mean values
'''
def fill_missings_with_entities(data,sim_mat, indices,n):
    if n < 1:
        raise ValueError, "Given num users is wrong!"
    website_idx = indices.keys()
    for website in website_idx:
        # find replace values
        sim_indices = find_similars_from_id(website, sim_mat, n)
        sim_rows = data[sim_indices,:]
        invalid_entries = where(sim_rows==-1)
        mask = zeros(sim_rows.shape)
        mask[invalid_entries] = 1
        filtered_rows = ma.masked_array(sim_rows,mask)
        mean_colms = filtered_rows.mean(axis=0)
        # append values too misings
        missing_cols = indices[website]
        if sum(data[website,missing_cols]) == -1*size(data[website,missing_cols]):
            data[website,missing_cols] = mean_colms[missing_cols];
        else:
            print "Wrong missing value entry for row "+website
    return data

#====================================
# PROCESSING WEBSITE-ID LIST
#====================================
'''
Read list of websites and mathing ids list into memory as dictionary
dict[id] => website name
'''
def read_website_dict_file(file_path):
    dicti = []
    with open(file_path,'rb') as csvfile:
        readread = csv.reader(csvfile,delimiter=',')
        for line in readread:
            dicti.append(line[0])
    return dicti

'''
Returns the corresponding website name given the id values that starts from 1
'''
def get_site_from_file(ids, file):
    websites = []
    for id in ids:
        websites.append(file[id])
    return websites

'''
Returns set of id values matching given web pages
'''
def get_id_from_file(names, list):
    ids = names
    for id, item in enumerate(list):
        if item in names:
            insert_index = names.index(item)
            ids[insert_index] = id
    for id in ids:
        if type(id) == type('str'):
            raise ValueError, "One of the given website name is not in the active data list!!!"
    return ids
                




# #===============================================================================
# # Test Code
# #===============================================================================
# (data, indices) = read_csv_file('toy_data/sample_data.txt')
# sim_mat = find_similarity_matrix(data)
# sim_mat = squareform(sim_mat)
# indices = find_missings(data);
# fill_missings_with_entities(data, sim_mat, indices, 4)
# data
# # dist_v = find_dist_v_to_all(data[1,:], data)
# 
# # data_r = remove_v_from_data(data[1,:], data)
# # sim_mat

    