#!/bin/bash
#
# Laura Tung
#
# Usage: optimize_k_jellyfish.sh <SRA_Run_accession>
#
# <SRA_Run_accession>: SRA Run accession ID.
#


accession=$1

fastq_1=${accession}_pass_1.fastq
fastq_2=${accession}_pass_2.fastq

touch ${accession}_optimize_k

jellyfish_dir=jellyfish_output_optimize_k
if [ ! -d $jellyfish_dir ]
then
    mkdir $jellyfish_dir
fi

for k in {5..25}
do

   if [ -f $fastq_1 ] && [ -f $fastq_2 ]
   then
       jellyfish count -m $k -s 100M -t 10 -C -F 2 -o $jellyfish_dir/${accession}_counts_$k.jf $fastq_1 $fastq_2
   elif [ -f $fastq_1 ] 
   then
       jellyfish count -m $k -s 100M -t 10 -C -o $jellyfish_dir/${accession}_counts_$k.jf $fastq_1
   elif [ -f $fastq_2 ]
   then
       jellyfish count -m $k -s 100M -t 10 -C -o $jellyfish_dir/${accession}_counts_$k.jf $fastq_2
   fi

   jellyfish dump -c -t -o $jellyfish_dir/${accession}_counts_dumps_$k $jellyfish_dir/${accession}_counts_$k.jf

   num_k_mers=$(wc -l $jellyfish_dir/${accession}_counts_dumps_$k | awk '{print $1}' -)
   echo "${k} ${num_k_mers}" >> ${accession}_optimize_k

done



