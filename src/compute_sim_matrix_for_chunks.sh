#!/bin/bash
#
# Laura Tung
#
# Usage: compute_sim_matrix_for_chunks.sh <file_prefix> <chunk_dir_prefix> <num_chunks>
#
# <file_prefix>: filename prefix for the sub-datasets files split from the original full set.
# <chunk_dir_prefix>: chunk directory prefix (e.g. "chunk_")
# <num_chunks>: number of chunks.


prefix=$1
chunk_dir_prefix=$2
num_chunks=$3

bin_dir=/home/ltung/jellyfishsim
curr_dir="$PWD"

for (( k=0; k<=$(($num_chunks-1)); k++ ))
do
    echo "Chunk $k:"

    run_dir=${chunk_dir_prefix}$k
    datasets_file=${prefix}$k

    cd $run_dir

    $bin_dir/sortsim 17 $datasets_file
    
    cd $curr_dir

done
