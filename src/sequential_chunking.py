# sequential_chunking.py
#
# Name: Laura Tung
#
# Usage: python sequential_chunking.py <full_set_datasets_file> <num_chunks> <chunk_size>
#
# <full_set_datasets_file>: file listing the datasets in the full set (which is going to be chunked).
# <num_chunks>: number of chunks. e.g. 10.
# <chunk_size>: chunk size. e.g. 100, 1000.

#import pdb; pdb.set_trace() # Uncomment to debug code using pdb (like gdb)

import sys
import numpy as np


def generate_chunks(fullset_datasets_array, num_chunks, chunk_size):
    
    for i in range(num_chunks):
        ith_chunk = fullset_datasets_array[i*chunk_size:(i+1)*chunk_size]
        print("Shape of ith_chunk:", ith_chunk.shape)
        np.savetxt("fullset_datasets_chunk_" + str(i), ith_chunk, fmt='%s')
    
    return None


if __name__ == "__main__":

    full_set_datasets_file = sys.argv[1]
    num_chunks = int(sys.argv[2])
    chunk_size = int(sys.argv[3])
        
    fullset_datasets_array = np.loadtxt(full_set_datasets_file, dtype='str')
    print("Shape of fullset_datasets_array:", fullset_datasets_array.shape)
 
    generate_chunks(fullset_datasets_array, num_chunks, chunk_size)   


    