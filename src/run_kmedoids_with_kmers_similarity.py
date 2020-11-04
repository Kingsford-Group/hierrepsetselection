# run_kmedoids_with_kmers_similarity.py
#
# Name: Laura Tung
#
# Usage: python run_kmedoids_with_kmers_similarity.py <similarity_matrix_file> <representative_set_size> <full_set_datasets_file>
#
# <similarity_matrix_file>: filename of similarity_matrix file.
# <representative_set_size>: desired size of the representative set (i.e. number of datasets desired).
# <full_set_datasets_file>: file listing the datasets in the full set (which was used to generate similarity_matrix).

#import pdb; pdb.set_trace() # Uncomment to debug code using pdb (like gdb)

import sys
import numpy as np
import matplotlib.pyplot as plt

from Bio.Cluster import kmedoids


def k_medoids_clustering(dist_array, k_clusters):
    
    clusterid, error, nfound = kmedoids(dist_array, nclusters=k_clusters, npass=100)
    
    return clusterid

def convert_to_dist_matrix(similarity_matrix):
    
    data_dist_array = np.ones_like(similarity_matrix) - similarity_matrix
    
    return data_dist_array


if __name__ == "__main__":

    similarity_matrix_file = sys.argv[1]
    n_rep_set = int(sys.argv[2])
    full_set_datasets_file = sys.argv[3]
    
    similarity_matrix = np.loadtxt(similarity_matrix_file, dtype='float')
    print("Shape of similarity_matrix:", similarity_matrix.shape)
    
    fullset_datasets_array = np.loadtxt(full_set_datasets_file, dtype='str')
    print("Shape of fullset_datasets_array:", fullset_datasets_array.shape)
    
    # convert similarity matrix to distance matrix
    data_dist_array = convert_to_dist_matrix(similarity_matrix)

    # perform k-medoids clustering
    clusters_ids = k_medoids_clustering(data_dist_array, n_rep_set)
    print("Shape of clusters_ids:", clusters_ids.shape)

    # get all medoids indices and medoids
    medoids_indices = list(set(clusters_ids))
    medoids = fullset_datasets_array[medoids_indices]
    
    # save the result
    np.savetxt("representative_set_datasets", medoids, fmt='%s')
    np.savetxt("representative_set_index", medoids_indices, fmt='%d')
    
    
    
    
