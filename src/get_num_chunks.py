# get_num_chunks.py
#
# Name: Laura Tung
#
# Usage: python get_num_chunks.py <fullset_size> <chunk_size>
#
# <fullset_size>: size of the set to be chunked.
# <chunk_size>: size of chunk.

#import pdb; pdb.set_trace() # Uncomment to debug code using pdb (like gdb)

import sys
import math



if __name__ == "__main__":

    fullset_size = int(sys.argv[1])
    chunk_size = int(sys.argv[2])

    num_chunks = math.ceil(fullset_size/chunk_size)
    print(num_chunks)


    
    

    


    

    



    
    
