#!/bin/bash
#
# Laura Tung
#
# Usage: merge_chunks.sh <chunk_dir_prefix> 
#
# <chunk_dir_prefix>: chunk directory prefix (e.g. "chunk_")


chunk_dir_prefix=$1

merge_dir=merge_of_chunks

if [ ! -d $merge_dir ]
then
     mkdir $merge_dir
fi

cat ${chunk_dir_prefix}*/representative_set_datasets > $merge_dir/merged_datasets
