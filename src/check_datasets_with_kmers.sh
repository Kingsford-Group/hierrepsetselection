#!/bin/bash
#
# Laura Tung
#
# Find those datasets with no k-mers dumped: the k-mers counts-dump file is empty, due to that the read-length is too short (shorter than the k-mer size 17).
#
# Usage: check_datasets_with_kmers.sh <successful_download_datasets>
#
# <successful_download_datasets>: filename of successful_download_datasets which contains 3 columns (SRA_Experiment, BioSample, SRA_Run)
#


filename=$1

curr_dir="$PWD"

jellyfish_dir=jellyfish_output

touch successful_download_datasets_no_kmers
touch successful_download_datasets_with_kmers

while read -r line
do
    if [ ! -z "$line" ]
    then
	line_array=($line)
        biosample=${line_array[1]}
        exp=${line_array[0]}
        run=${line_array[2]}

        id_dir=${exp}_${biosample}_${run}
        run_dir=${id_dir}/${run}

	cd $run_dir/$jellyfish_dir

	if [ $(gunzip -c ${run}_counts_dumps.gz | head -c1 | wc -c) == "0" ]
	then
 	    # this dataset's counts_dumps file is empty (due to that the read-length is too short) 
            echo "${exp} ${biosample} ${run}" >> ${curr_dir}/successful_download_datasets_no_kmers

	else
            # this dataset's counts_dumps file is not empty 
	    echo "${exp} ${biosample} ${run}" >> ${curr_dir}/successful_download_datasets_with_kmers
	fi

        cd $curr_dir
    fi

done < $filename

echo "--------------------------------------------"
echo "DONE check datasets with k-mers."

