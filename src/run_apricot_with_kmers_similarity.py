# run_apricot_with_kmers_similarity.py
#
# Name: Laura Tung
#
# Usage: python run_apricot_with_kmers_similarity.py <similarity_matrix_file> <representative_set_size> <full_set_datasets_file>
#
# <similarity_matrix_file>: filename of similarity_matrix file.
# <representative_set_size>: desired size of the representative set (i.e. number of datasets desired).
# <full_set_datasets_file>: file listing the datasets in the full set (which was used to generate similarity_matrix).

#import pdb; pdb.set_trace() # Uncomment to debug code using pdb (like gdb)

import sys
import numpy as np
import matplotlib.pyplot as plt

from apricot import FacilityLocationSelection


def facility_location(n_rep_set, X_similarity):
    
    model = FacilityLocationSelection(n_samples=n_rep_set, metric='precomputed')
    model.fit(X_similarity)
    
    return model.ranking


if __name__ == "__main__":

    similarity_matrix_file = sys.argv[1]
    n_rep_set = int(sys.argv[2])
    full_set_datasets_file = sys.argv[3]
    
    min_rep_set_size = 10
    
    similarity_matrix = np.loadtxt(similarity_matrix_file, dtype='float')
    print("Shape of similarity_matrix:", similarity_matrix.shape)
    
    fullset_datasets_array = np.loadtxt(full_set_datasets_file, dtype='str')
    print("Shape of fullset_datasets_array:", fullset_datasets_array.shape)
        
    # perform representative set selection using facility location function
    if (similarity_matrix.shape[0] <= n_rep_set) or (similarity_matrix.shape[0] <= min_rep_set_size):
        # do not run apricot, just use the original-set datasets as the representative-set datasets
        ranking = np.arange(similarity_matrix.shape[0])
        X_subset = fullset_datasets_array
    else:
        ranking = facility_location(n_rep_set, similarity_matrix)
        X_subset = fullset_datasets_array[ranking]

    # save the result
    np.savetxt("representative_set_datasets", X_subset, fmt='%s')
    np.savetxt("representative_set_index", ranking, fmt='%d')

    
    

    


    

    



    
    
