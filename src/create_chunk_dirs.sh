#!/bin/bash
#
# Laura Tung
#
# Usage: create_chunk_dirs.sh <file_prefix> <chunk_dir_prefix> <num_chunks>
#
# <file_prefix>: filename prefix for the sub-datasets files (chunks) split from the original full set.
# <chunk_dir_prefix>: prefix for chunks directories (e.g. "chunk_").
# <num_chunks>: number of chunks.


prefix=$1
chunk_dir_prefix=$2
num_chunks=$3

curr_dir="$PWD"


for (( k=0; k<=$(($num_chunks-1)); k++ ))
do
    run_dir=${chunk_dir_prefix}$k
    filename=${prefix}$k

    mkdir $run_dir
    cd $run_dir
    ln -s ../${filename} .
    
    cd $curr_dir

done
