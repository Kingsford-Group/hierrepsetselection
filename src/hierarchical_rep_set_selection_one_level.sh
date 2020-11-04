#!/bin/bash
#
# Laura Tung
#
# One leve of Hierarchical Representative Set Selection used for multiple iterations.
#
# Usage: hierarchical_rep_set_selection_one_level.sh <fullset_fullpath_kmer_files> <num_chunks> <chunk_size> <chunk_dir_prefix> <Q> <chunking_method> <subset_size>
#
# <fullset_fullpath_kmer_files>: file listing the datasets (full-path kmer files) in the full set.
# <num_chunks>: number of chunks (e.g. 10).
# <chunk_size>: chunk size (e.g. 100, 1000).
# <chunk_dir_prefix>: prefix of chunk directories (e.g. chunk_).
# <Q>: average representative-set size for each chunk (e.g. Q=20 or Q=200).
# <chunking_method>: "seeded" or "sequential".
# <subset_size>: When choosing "seeded" chunking, a random subset from the fullset is used for seeding. Provide the size of the random subset here (e.g. 200, 1000).

fullset_fullpath_kmer_files=$1
num_chunks=$2
chunk_size=$3
chunk_dir_prefix=$4
Q=$5
chunking_method=$6

curr_dir="$PWD"

bin_dir=/mnt/disk37/user/ltung/representative_set/bin
exe_dir=/home/ltung/jellyfishsim

datasets_file_prefix=fullset_datasets_chunk_


# (1) Divide (Chunking):
echo "Chunking..."
if [ $chunking_method == 'seeded' ]
then
    echo "seeded chunking"
    subset_size=$7

    # SEEDED_CHUNKING:
    # (a) Select a random subset from the fullset, to be used for seeded-chunking:

    python3.6 $bin_dir/select_random_subset_fullpath_files.py $fullset_fullpath_kmer_files $subset_size > select_random_subset_fullpath_files.log

    # (b) Perform seeded-chunking:

    { /usr/bin/time $exe_dir/chunking 17 $fullset_fullpath_kmer_files selected_subset_datasets_fullpath $num_chunks $chunk_size > chunking.log; } 2> chunking.time.log 

else
    echo "sequential chunking"
    
    # SEQUENTIAL_CHUNKING:
    python3.6 $bin_dir/sequential_chunking.py $fullset_fullpath_kmer_files $num_chunks $chunk_size > sequential_chunking.log

fi

# (c) Create chunks directories:

$bin_dir/create_chunk_dirs.sh $datasets_file_prefix $chunk_dir_prefix $num_chunks

echo "Done Chunking"

# (2) Compute similarity matrix for every chunk:

echo "Computing similarity matrix for every chunk..."
{ /usr/bin/time $bin_dir/compute_sim_matrix_for_chunks.sh $datasets_file_prefix $chunk_dir_prefix $num_chunks > compute_sim_matrix.log; } 2> compute_sim_matrix.time.log 
echo "Done Computing similarity matrix for every chunk"

# (3) Compute weights (mean-square weighting) for every chunk:

echo "Computing weights for every chunk..."
python3.6 $bin_dir/compute_chunk_weights_mean-square-only.py $chunk_dir_prefix $num_chunks $Q $chunk_size > compute_chunk_weights_mean-square-only.log 
echo "Done Computing weights for every chunk"

# (4) Run apricot for every chunk:

echo "Running apricot for every chunk..."
{ /usr/bin/time $bin_dir/run_apricot_for_chunks.sh $datasets_file_prefix $chunk_dir_prefix $num_chunks > run_apricot_for_chunks.log; } 2> run_apricot_for_chunks.time.log 
echo "Done Running apricot for every chunk"

# (5) Merge (merge chunks):

echo "Merging chunks..."
$bin_dir/merge_chunks.sh $chunk_dir_prefix
echo "Done Merging chunks"



