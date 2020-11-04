#!/bin/bash
#
# Laura Tung
#
# Direct apricot Representative Set Selection 
#
# Usage: direct_apricot_rep_set_selection.sh <fullset_fullpath_kmer_files> <representative_set_size> 
#
# <fullset_fullpath_kmer_files>: file listing the datasets (full-path kmer files) in the full set.
# <representative_set_size>: user-desired final representative set size.

fullset_fullpath_kmer_files=$1
representative_set_size=$2

curr_dir="$PWD"

bin_dir=/mnt/disk37/user/ltung/representative_set/bin
exe_dir=/home/ltung/jellyfishsim


# (1) Compute similarity matrix for the full set:

echo "Computing similarity matrix for the full set..."
{ /usr/bin/time $exe_dir/sortsim 17 $fullset_fullpath_kmer_files > sortsim.log; } 2> sortsim.time.log 
echo "Done Computing similarity matrix for the full set"

# (2) Run apricot on the full set:

echo "Running apricot on the full set..."
{ /usr/bin/time python3.6 $bin_dir/run_apricot_with_kmers_similarity.py similarity_matrix $representative_set_size $fullset_fullpath_kmer_files > run_apricot.log; } 2> run_apricot.time.log 
echo "Done Running apricot on the full set"


echo "Done Direct apricot Representative Set Selection"


