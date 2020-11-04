# get_mapped_rep_set_index.py
#
# Name: Laura Tung
#
# Usage: python get_mapped_rep_set_index.py <full_set_datasets_file> <representative_set_datasets>
#
# <full_set_datasets_file>: file listing the datasets in the full set (which was used to generate similarity_matrix).
# <representative_set_datasets>: file listing the representative set datasets (representative_set_datasets).

#import pdb; pdb.set_trace() # Uncomment to debug code using pdb (like gdb)

import sys
import numpy as np


def get_mapped_rep_set_index(fullset_datasets_array, rep_set_datasets_array):
    
    mapped_rep_set_index = []
    for rep_dataset in rep_set_datasets_array:
        found_index = [i for i in range(len(fullset_datasets_array)) if fullset_datasets_array[i] == rep_dataset]
        mapped_rep_set_index.append(found_index[0])
    
    return mapped_rep_set_index


if __name__ == "__main__":

    full_set_datasets_file = sys.argv[1]
    rep_set_datasets_file = sys.argv[2]
        
    fullset_datasets_array = np.loadtxt(full_set_datasets_file, dtype='str')
    print("Shape of fullset_datasets_array:", fullset_datasets_array.shape)
 
    rep_set_datasets_array = np.loadtxt(rep_set_datasets_file, dtype='str')
    print("Shape of rep_set_datasets_array:", rep_set_datasets_array.shape)   

    mapped_rep_set_index = get_mapped_rep_set_index(fullset_datasets_array, rep_set_datasets_array)   

    np.savetxt("mapped_representative_set_index", mapped_rep_set_index, fmt='%d')

    