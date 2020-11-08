#!/bin/bash
#
# Laura Tung
#
# Usage: run_apricot_for_chunks.sh <file_prefix> <chunk_dir_prefix> <num_chunks>
#
# <file_prefix>: filename prefix for the sub-datasets files split from the original full set.
# <chunk_dir_prefix>: chunk directory prefix (e.g. "chunk_")
# <num_chunks>: number of chunks.


prefix=$1
chunk_dir_prefix=$2
num_chunks=$3

bin_dir=/mnt/disk37/user/ltung/representative_set/bin
curr_dir="$PWD"

for (( k=0; k<=$(($num_chunks-1)); k++ ))
do
    echo "Chunk $k:"

    run_dir=${chunk_dir_prefix}$k
    datasets_file=${prefix}$k

    cd $run_dir

    rep_set_size=$(cat rep_set_size)

    python $bin_dir/run_apricot_with_kmers_similarity.py similarity_matrix $rep_set_size $datasets_file
    
    cd $curr_dir

done
