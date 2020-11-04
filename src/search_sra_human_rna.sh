#!/bin/bash
#
# Laura Tung
#
# Search and fetch all SRA Experiments records that are human RNA-seq using Illumina platform
#
# Usage: search_sra_human_rna.sh
#


# Search the SRA database and fetch the records
esearch -db sra -query "homo sapiens[Organism] AND transcriptomic[Source] AND rna seq[Strategy] AND illumina[Platform]" | efetch -format xml > sra_human_rna_seq_exp.xml

