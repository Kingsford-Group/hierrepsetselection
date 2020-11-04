# select_random_subset_fullpath_files.py
#
# Name: Laura Tung
#
# Usage: python select_random_subset_fullpath_files.py <full_set_datasets_file> <subset_size>
#
# <full_set_datasets_file>: file listing the datasets (full-path files) in the full set.
# <subset_size>: desired size of the subset (i.e. number of datasets desired).

import sys
import numpy as np
import pandas as pd

if __name__ == "__main__":

    datasets_file = sys.argv[1]
    num_datasets = int(sys.argv[2])
    
    df = pd.read_csv(datasets_file, header=None, sep=' ', engine='python')
    print(df.info())
    
    selected_df = df.sample(n = num_datasets, random_state=1)
    
    outfile = "selected_subset_datasets_fullpath"
    pd.DataFrame.to_csv(selected_df, path_or_buf=outfile, sep=' ', header=False, index=False)
    np.savetxt("selected_subset_index", list(selected_df.index), fmt='%d')
    
    
    
