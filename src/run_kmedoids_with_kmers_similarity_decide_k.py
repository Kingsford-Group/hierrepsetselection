# run_kmedoids_with_kmers_similarity_decide_k.py
#
# Name: Laura Tung
#
# Usage: python run_kmedoids_with_kmers_similarity_decide_k.py <similarity_matrix_file> <representative_set_size> <full_set_datasets_file>
#
# <similarity_matrix_file>: filename of similarity_matrix file.
# <representative_set_size>: desired size of the representative set (i.e. number of datasets desired).
# <full_set_datasets_file>: file listing the datasets in the full set (which was used to generate similarity_matrix).

#import pdb; pdb.set_trace() # Uncomment to debug code using pdb (like gdb)

import sys
import numpy as np
import matplotlib.pyplot as plt
import math
import random

from Bio.Cluster import kmedoids


def k_medoids_clustering(dist_array, k_clusters):
    
    clusterid, error, nfound = kmedoids(dist_array, nclusters=k_clusters, npass=100)
    
    return clusterid

def convert_to_dist_matrix(similarity_matrix):
    
    data_dist_array = np.ones_like(similarity_matrix) - similarity_matrix
    
    return data_dist_array

def get_rep_set_indices(medoids_indices, clusters_ids, n_rep_set, k):
    
    total_elements = len(clusters_ids)
    
    if k == n_rep_set:
        # just use all medoids
        rep_set_indices = medoids_indices
        
    elif k < n_rep_set:
        # randomly subsampling elements from each cluster, with # of elements proportional to the cluster volume
        # if only sampling one element for a cluster, just use the medoid of that cluster
        rep_set_indices = []
        for medoid_index in medoids_indices:
            cluster_elements = [i for i in range(total_elements) if clusters_ids[i] == medoid_index]
            
            # determine the number of elements to sample in current cluster
            if medoid_index == medoids_indices[-1]:
                # last cluster, just make up all remaining quota
                num_samples = n_rep_set - len(rep_set_indices)
            else:
                # proportional to the cluster volume
                proportion = len(cluster_elements)/total_elements
                num_samples = int(n_rep_set*proportion)
                if num_samples == 0:
                    num_samples = 1
            
            # subsampling elements from current cluster
            if num_samples == 1:
                # just use the medoid of current cluster
                rep_set_indices.append(medoid_index)
            else:
                rep_set_indices = rep_set_indices + random.sample(cluster_elements, num_samples)
    else: 
        # k > n_rep_set
        # randomly subsmapling from the medoids
        rep_set_indices = random.sample(medoids_indices, n_rep_set)
    
    return rep_set_indices


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

    # perform k-medoids clustering, using k = square root of the size of full-set
    k = int(math.sqrt(similarity_matrix.shape[0]))
    clusters_ids = k_medoids_clustering(data_dist_array, k)
    print("Shape of clusters_ids:", clusters_ids.shape)

    # get all medoids indices
    medoids_indices = list(set(clusters_ids))
    print("Number of clusters:", len(medoids_indices))
    
    # get representive set indices by subsampling the clusters
    rep_set_indices = get_rep_set_indices(medoids_indices, clusters_ids, n_rep_set, k)
    
    rep_set_datasets = fullset_datasets_array[rep_set_indices]
    
    # save the result
    np.savetxt("representative_set_datasets", rep_set_datasets, fmt='%s')
    np.savetxt("representative_set_index", rep_set_indices, fmt='%d')
    
    
    
    
