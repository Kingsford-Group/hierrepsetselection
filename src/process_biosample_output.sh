#!/bin/bash
#
# Laura Tung
#
# Process the esearch output from BioSample to make it a true, single-root XML.
#
# Usage: process_biosample_output.sh <input_file> <output_file>
#
# <input_file>: filename (no path) of the SRA output xml file to be processed.
# <output_file>: filename (no path) of the processed xml file.
#
# It should be run in the directory where <input_file> resides.

infile=$1

outfile=$2


# Remove all the xml declarations lines throughout the file
sed '/<?xml version="1.0" ?>/d' $infile > tmp

# Add a single-root wrapper, and also add an xml declaration line at the beginning
echo '<root>' | cat - tmp > tmp1
rm tmp

echo '<?xml version="1.0"  ?>' | cat - tmp1 > tmp2
rm tmp1

echo '</root>' | cat tmp2 - > $outfile
rm tmp2

