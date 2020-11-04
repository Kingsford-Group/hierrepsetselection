# filter_aligned_datasets.py
#
# Name: Laura Tung
#
# Usage: python filter_aligned_datasets.py <xml_filename> <exp_csv_filename>
#
# <xml_filename>: filename of the xml file obtained by efecth for many SRA Experiments.
# <exp_csv_filename>: filename of the SRA_Exps csv file originally generated from this corresponding xml file.
# 

#import pdb; pdb.set_trace() # Uncomment to debug code using pdb (like gdb)

import sys
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import pandas as pd

def get_all_aligned_runs(root):
    
    aligned_runs = []
    runs = root.findall(".//Table[@name='PRIMARY_ALIGNMENT']/../../..")
    for run in runs:
        aligned_runs.append(run.get('accession'))
    
    return aligned_runs

def get_unaligned_datasets(root, exp_df):
    
    aligned_runs = get_all_aligned_runs(root)
    print("# Aligned RUNs in the full xml file:", len(aligned_runs))
    
    aligned_flag = exp_df['SRA_Run'].isin(aligned_runs)
    
    unaligned_exp_df = exp_df[aligned_flag == False]
    print("Unaligned SRA Experiments dataframe:")
    print(unaligned_exp_df.info())
    
    aligned_exp_df = exp_df[aligned_flag == True]
    print("Aligned SRA Experiments dataframe:")
    print(aligned_exp_df.info())
    
    return unaligned_exp_df, aligned_exp_df
  
    
if __name__ == "__main__":

    xml_file = sys.argv[1]
    exp_csv_file = sys.argv[2]

    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    exp_df = pd.read_csv(exp_csv_file, sep = ",", engine='python')
    print("Original SRA Experiments dataframe:")
    print(exp_df.info())
    
    unaligned_exp_df, aligned_exp_df = get_unaligned_datasets(root, exp_df)
    
    f_name = exp_csv_file[0:-4]
    
    pd.DataFrame.to_csv(unaligned_exp_df, path_or_buf=f_name+"_unaligned.csv", index=False)
    pd.DataFrame.to_csv(aligned_exp_df, path_or_buf=f_name+"_aligned.csv", index=False)
    
    unaligned_exp_array = unaligned_exp_df[['SRA_Experiment', 'BioSample', 'SRA_Run']].to_numpy()
    print("Shape of unaligned_exp_array:", unaligned_exp_array.shape)
    
    aligned_exp_array = aligned_exp_df[['SRA_Experiment', 'BioSample', 'SRA_Run']].to_numpy()
    print("Shape of aligned_exp_array:", aligned_exp_array.shape)
    
    np.savetxt("unaligned_exp_datasets", unaligned_exp_array, fmt='%s')
    np.savetxt("aligned_exp_datasets", aligned_exp_array, fmt='%s')
    
    
    
    
    
    
    
    
