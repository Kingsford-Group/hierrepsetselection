#!/bin/bash
#
# Laura Tung
#
# Usage: check_downloaded_subsets.sh <unaligned_exp_datasets_file>
#
# <unaligned_exp_datasets_file>: filename of unaligned_exp_datasets which contains 3 columns (SRA_Experiment, BioSample, SRA_Run)
#


filename=$1

curr_dir="$PWD"

touch failed_download_datasets
touch successful_download_datasets

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

	cd $run_dir

        fastq_1=${run}_pass_1.fastq
	fastq_2=${run}_pass_2.fastq

        if [ ! -f $fastq_1 ] && [ ! -f $fastq_2 ]
	then
	    # this dataset failed to download/dump
            echo "${exp} ${biosample} ${run}" >> ${curr_dir}/failed_download_datasets

	else
            # this dataset was downloaded and dumped
	    echo "${exp} ${biosample} ${run}" >> ${curr_dir}/successful_download_datasets
	fi

        cd $curr_dir
    fi

done < $filename

echo "--------------------------------------------"
echo "DONE check downloaded subsets of reads."

