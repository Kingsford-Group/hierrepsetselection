# plot_similarity_distribution.py
#
# Name: Laura Tung
#
# Usage: python plot_similarity_distribution.py <similarity_matrix_file> <similarity_type>
#
# <similarity_matrix_file>: filename of similarity_matrix file.
# <similarity_type>: type of similarity (cosine-similarity, weighted-jaccard)

#import pdb; pdb.set_trace() # Uncomment to debug code using pdb (like gdb)

import sys
import numpy as np
import matplotlib.pyplot as plt

def make_similarity_instances(similarity_matrix):
    
    similarity_instances = []
    
    row = similarity_matrix.shape[0]
    
    for i in range(row):
        for j in range(i+1, row):
            similarity_instances.append(similarity_matrix[i, j])
    
    return np.array(similarity_instances)


def plot_similarity_distribution(similarity_instances, similarity_matrix_file, similarity_type):
    
    plt.figure()
    plt.hist(similarity_instances, bins = 50, edgecolor='red')
    plt.xlabel("K-mers Similarity ("+similarity_type+")")
    plt.ylabel("Number of Dataset-Pairs")
    plt.title("K-mers Similarity Distribution ("+similarity_type+")")
    plt.savefig(similarity_matrix_file+"_distribution.png", bbox_inches='tight')
    
    return None


if __name__ == "__main__":

    similarity_matrix_file = sys.argv[1]
    similarity_type = sys.argv[2]
    
    similarity_matrix = np.loadtxt(similarity_matrix_file, dtype='float')
    print("Shape of similarity_matrix:", similarity_matrix.shape)
    
    similarity_instances = make_similarity_instances(similarity_matrix)
    print("Shape of similarity_instances:", similarity_instances.shape)
    
    plot_similarity_distribution(similarity_instances, similarity_matrix_file, similarity_type)
    
    
    
    