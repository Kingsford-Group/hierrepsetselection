#!/bin/bash
#
# Laura Tung
#
# Usage: fetch_biosamples.sh <biosamples_list_file> 
#
# <biosamples_list_file>: filename of BioSamples_list file containing one column of BioSample IDs.
#


filename=$1
output_filename=human_used_biosamples.xml

touch $output_filename

while IFS= read -r -u "$fd_num" line
do
    if [ ! -z "$line" ]
    then
        biosample_id=$line

	echo "$biosample_id"
        esearch -db biosample -q $biosample_id | efetch -format xml >> $output_filename
	echo -e "\n" >> $output_filename
    fi

done {fd_num}< $filename

echo "DONE extracting BioSamples records"

