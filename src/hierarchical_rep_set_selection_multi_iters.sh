#!/bin/bash
#
# Laura Tung
#
# Hierarchical Representative Set Selection (multiple levels of iterations)
#
# Usage: hierarchical_rep_set_selection_multi_iters.sh <fullset_fullpath_kmer_files> <representative_set_size> <num_iters> <chunk_size> <chunk_dir_prefix> <Q> <chunking_method> <top_subset_size>
#
# <fullset_fullpath_kmer_files>: file listing the datasets (full-path kmer files) in the full set.
# <representative_set_size>: user-desired final representative set size.
# <num_iters>: number of iterations (i.e. the number of divide-merge levels in the hierarchy. e.g. 2).
# <chunk_size>: chunk size (e.g. 1000).
# <chunk_dir_prefix>: prefix of chunk directories (e.g. chunk_).
# <Q>: average representative-set size for each chunk (e.g. Q=200).
# <chunking_method>: "seeded" or "sequential".
# <top_subset_size>: When choosing "seeded" chunking, a random subset from the fullset is used for seeding. Provide the size of the random subset for the top level here (e.g. 2000). At the next level, the random subset size is the previous level's subset size divided by 2.

fullset_fullpath_kmer_files=$1
representative_set_size=$2
num_iters=$3
chunk_size=$4
chunk_dir_prefix=$5
Q=$6
chunking_method=$7

curr_dir="$PWD"

bin_dir=/mnt/disk37/user/ltung/representative_set/bin
exe_dir=/home/ltung/jellyfishsim

merge_dir=merge_of_chunks
merged_set_file=merged_datasets


if [ $chunking_method == 'seeded' ]
then
    subset_size=$8
fi


echo "Representative set size = $representative_set_size"
echo "Chunk size = $chunk_size"
echo "Q = $Q"

# Perform multiple levels of iterations:

for (( it=0; it<=$(($num_iters-1)); it++ ))
do
    echo "Level $it:"

    fullset_size=$(wc -l $fullset_fullpath_kmer_files | awk '{print $1}' -)

    echo "Full-set size = $fullset_size"

    if [ $chunking_method == 'seeded' ]
    then
        echo "Random subset size = $subset_size"
    fi

    # find the number of chunks for the current level
    num_chunks=$(python3.6 $bin_dir/get_num_chunks.py $fullset_size $chunk_size)

    echo "Number of chunks k = $num_chunks"

    # Do the current level: Steps (1)-(5)
    if [ $chunking_method == 'seeded' ]
    then
        $bin_dir/hierarchical_rep_set_selection_one_level.sh $fullset_fullpath_kmer_files $num_chunks $chunk_size $chunk_dir_prefix $Q $chunking_method $subset_size
    else
        $bin_dir/hierarchical_rep_set_selection_one_level.sh $fullset_fullpath_kmer_files $num_chunks $chunk_size $chunk_dir_prefix $Q $chunking_method
    fi

    # Go to $merge_dir for the next level of iteration, update $fullset_fullpath_kmer_files and $subset_size.
    cd $merge_dir

    fullset_fullpath_kmer_files=$merged_set_file

    if [ $chunking_method == 'seeded' ]
    then
	subset_size=$(($subset_size/2))
    fi

    echo "Done Level $it"

done

# (6) Compute similarity matrix for the merged set:

echo "Computing similarity matrix for the merged set..."
{ /usr/bin/time $exe_dir/sortsim 17 merged_datasets > sortsim.log; } 2> sortsim.time.log 
echo "Done Computing similarity matrix for the merged set"

# (7) Run apricot for the merged set:

echo "Running apricot for the merged set..."
{ /usr/bin/time python3.6 $bin_dir/run_apricot_with_kmers_similarity.py similarity_matrix $representative_set_size merged_datasets > run_apricot.log; } 2> run_apricot.time.log 
echo "Done Running apricot for the merged set"

cd $curr_dir

echo "Done Hierarchical Representative Set Selection"


