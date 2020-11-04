# compute_chunk_weights_mean-square-only.py
#
# Name: Laura Tung
#
# Usage: python compute_chunk_weights_mean-square-only.py <chunk_dir_prefix> <num_chunks> <Q> <full_chunk_size>
#
# <chunk_dir_prefix>: chunk directories prefix (e.g. "chunk_")
# <num_chunks>: number of chuncks (k).
# <Q>: average representative-set size for each chunk (e.g. Q=20 or Q=200)
# <full_chunk_size>: size of a full chunk.

#import pdb; pdb.set_trace() # Uncomment to debug code using pdb (like gdb)

import sys
import numpy as np
from scipy.spatial.distance import squareform


def convert_to_dist_matrix(similarity_matrix):
    
    data_dist_array = np.ones_like(similarity_matrix) - similarity_matrix
    
    return data_dist_array

def compute_weights_for_chunks(chunk_dir_prefix, num_chunks, Q, full_chunk_size):
    
    similarity_matrix_file = "similarity_matrix"
    
    weights_arr = np.ones(num_chunks)
    
    # get the mean-square of pairwise distances for each chunk
    mean_square_list = []
    for i in range(num_chunks):
        # for chunk i
        fullpath_similarity_matrix_file = chunk_dir_prefix + str(i) + "/" + similarity_matrix_file 
        similarity_matrix = np.loadtxt(fullpath_similarity_matrix_file, dtype='float')
        print("Chunk", i, ":  Shape of similarity_matrix:", similarity_matrix.shape)
    
        dist_matrix = convert_to_dist_matrix(similarity_matrix)
    
        dist_vector = squareform(dist_matrix)
        
        mean_square_list.append(np.mean(dist_vector)**2)
        
        # check if current chunk is an unfull chunk (there could be multiple unfull chunks in seeded-chunking)
        if similarity_matrix.shape[0] < full_chunk_size:
            alpha = similarity_matrix.shape[0]/full_chunk_size
            weights_arr[i] = alpha
    
    mean_square_array = np.array(mean_square_list)
    
    # get (weighted) mean-of-mean-square across all chuncks
    mean_of_mean_sqaure = np.average(mean_square_array, weights=weights_arr)
    print("Mean of mean-square:", mean_of_mean_sqaure)
    
    # compute weight (w1) and representative_set_size for each chunk
    full_weights_list = []
    for i in range(num_chunks):
        # for chunk i
        w1 = mean_square_list[i]/mean_of_mean_sqaure
        
        rep_set_size = round(w1*Q*weights_arr[i])
        
        full_weights_list.append([mean_square_list[i], w1, rep_set_size, weights_arr[i]])
        
        # write rep_set_size into the chunk_i directory
        f = open(chunk_dir_prefix + str(i) + "/rep_set_size", "w")
        f.write(str(int(rep_set_size)))
        f.close()
        
    # the returned full_weights_array has 4 columns: mean-square, w1, rep_set_size, weights_arr
    return np.array(full_weights_list)
  

if __name__ == "__main__":

    chunk_dir_prefix = sys.argv[1]
    num_chunks = int(sys.argv[2])
    Q = int(sys.argv[3])
    full_chunk_size = int(sys.argv[4])
    
    full_weights_array = compute_weights_for_chunks(chunk_dir_prefix, num_chunks, Q, full_chunk_size)
    print("Shape of full_weights_array:", full_weights_array.shape)
    print("Total # of representative datasets:", sum(full_weights_array[:,2]))
    
    # save full_weights_array to a file
    np.savetxt('weights_of_all_chunks', full_weights_array, fmt="%.9f")
    
    
    

    

    
    
    
    