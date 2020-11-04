# plot_optimize_k.py
#
# Name: Laura Tung
#
# Usage: python plot_optimize_k.py <optimize_k_file> <read_length> <SRA_RUN> <layout>
#
# <optimize_k_file>: filename of the *_optimize_k file.
# <read_length>: read length.
# <SRA_RUN>: SRA Run accession ID.
# <layout>: PAIRED or SINGLE.
# 

#import pdb; pdb.set_trace() # Uncomment to debug code using pdb (like gdb)

import sys
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":

    optimize_k_file = sys.argv[1]
    read_length = int(sys.argv[2])
    sra_run = sys.argv[3]
    layout = sys.argv[4]
    
    k_counts_array = np.loadtxt(optimize_k_file, dtype='int')
    print("Shape of k_counts_array:", k_counts_array.shape)
    
    fig = plt.figure(1)
    plt.plot(k_counts_array[:,0], k_counts_array[:,1], marker='.', markersize=8)
    x_ticks = np.arange(5, 26, 1)
    plt.xticks(x_ticks)
    plt.xlabel("k")
    plt.ylabel("Number of Distinct k-mers")
    plt.title("Number of Distinct k-mers vs. k (read length="+str(read_length)+", "+layout+", "+sra_run+")")
    plt.grid()
    plt.savefig(sra_run+"_optimize_k_plot.png", bbox_inches='tight')
    