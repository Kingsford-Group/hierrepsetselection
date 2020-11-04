# biosample_attributes_stats.py
#
# Name: Laura Tung
#
# Usage: python biosample_attributes_stats.py <biosamples_attributes.csv>
#
# <biosamples_attributes.csv>: filename of biosamples_attributes.csv file.

import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math

def compute_missing_percent(sub_df):
    
    missing_percent = []
    num_rows = len(sub_df.index.values)
    
    for colname in sub_df.columns.values:
        col = sub_df[colname]
        num_miss = col.isnull().sum()
        percent = (num_miss/num_rows)*100
        missing_percent.append(percent)
    
    print("missing_percent:", missing_percent)
    
    return missing_percent

def plot_missing_data(biosample_attributes_df):
    
    attributes = biosample_attributes_df.columns.values
    
    num_attributes = attributes.shape[0] - 1
    
    # divide attributes into 10 attributes per plot
    for i in range(math.ceil(num_attributes/10)):
        if i < math.ceil(num_attributes/10)-1:
            sub_df = biosample_attributes_df.iloc[:,(i*10)+1:(i+1)*10+1]
        else:
            sub_df = biosample_attributes_df.iloc[:,(i*10)+1:num_attributes+1]
        
        missing_percent = compute_missing_percent(sub_df)
            
        plt.figure()
        plt.barh(sub_df.columns.values, missing_percent, height=0.5)
        plt.xlabel("Missing Data Percentage (%)")
        plt.title("Missing Data in BioSample Attributes (total "+str(biosample_attributes_df.shape[0])+" BioSamples)")
        plt.savefig("missing_data_biosample_attributes_"+str(i)+".png", bbox_inches='tight')

    return None

if __name__ == "__main__":

    biosample_attributes_file = sys.argv[1]
    
    biosample_attributes_df = pd.read_csv(biosample_attributes_file, sep = ",", dtype='object', engine='python')
    print("Biosample attributes dataframe:")
    print(biosample_attributes_df.info())
    
    plot_missing_data(biosample_attributes_df)