#!/bin/bash
#
# Laura Tung
#
# Usage: run_jellyfish.sh <successful_download_datasets_file>
#
# <successful_download_datasets_file>: filename of successful_download_datasets which contains 3 columns (SRA_Experiment, BioSample, SRA_Run)
#


filename=$1
k=17

curr_dir="$PWD"

jellyfish_dir=jellyfish_output

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

	if [ ! -d $jellyfish_dir ]
	then
	    mkdir $jellyfish_dir
        fi

        fastq_1=${run}_pass_1.fastq
	fastq_2=${run}_pass_2.fastq

	echo "--------------------------------------------"
	echo "${run}:"

        if [ -f $fastq_1 ] && [ -f $fastq_2 ]
        then
             jellyfish count -m $k -s 100M -t 10 -C -F 2 -o $jellyfish_dir/${run}_counts.jf $fastq_1 $fastq_2
        elif [ -f $fastq_1 ]
        then
             jellyfish count -m $k -s 100M -t 10 -C -o $jellyfish_dir/${run}_counts.jf $fastq_1
        elif [ -f $fastq_2 ]
        then
             jellyfish count -m $k -s 100M -t 10 -C -o $jellyfish_dir/${run}_counts.jf $fastq_2
        fi

        jellyfish dump -c -t -o $jellyfish_dir/${run}_counts_dumps $jellyfish_dir/${run}_counts.jf

	gzip $jellyfish_dir/${run}_counts_dumps

	rm $jellyfish_dir/${run}_counts.jf

        cd $curr_dir
    fi

done < $filename

echo "--------------------------------------------"
echo "DONE jellyfish."

