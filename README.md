# Overview

This repository contains the programs for the Hierarchical Representative Set Selection, and the programs for direct representative set selection and random sampling, as well as the program for evaluating a representative set.
   

# Installation

Download the source code from this repository. In addition, also download the source code from the repository https://github.com/Kingsford-Group/jellyfishsim and then compile them (see Installation instructions there). You will need these three binaries compiled from the repository https://github.com/Kingsford-Group/jellyfishsim: `sortsim`, `chunking`, and `hausdorff`, in order to run the programs in this repository.

Modify the directory paths (`bin_dir` and `exe_dir`) accordingly in the code of this repository, to point to your local directory that holds the source code of this repository and your local directory that holds the binaries compiled from the repository https://github.com/Kingsford-Group/jellyfishsim.

You also need to install a Python package [apricot](https://github.com/jmschrei/apricot) by using:
```
    pip install apricot-select
```

# Usage

## Hierarchical representative set selection

The hierarchical representative set selection is a divide-and-conquer-like algorithm that breaks the representative set selection into sub-selections and hierarchically selects representative samples through multiple levels. Use the following command to run the hierarchical representative set selection:

```
hierarchical_rep_set_selection_multi_iters.sh <fullset_fullpath_kmer_files> <representative_set_size> <num_iters> <chunk_size> <chunk_dir_prefix> <Q> <chunking_method> <top_subset_size>
```
Where: <br>
`<fullset_fullpath_kmer_files>`:  A file containing the names of all the datasets' k-mer counts files (full-path) in the original full set, one filename per line. These k-mer counts files are gzipped. <br>
`<representative_set_size>`: The desired size of the final representative set. <br>
`<num_iters>`: The number of iterations (i.e. levels in the hierarchy). <br>
`<chunk_size>`: The size of each chunk. <br>
`<chunk_dir_prefix>`: The prefix of the chunk directories (e.g. "chunk_"). <br>
`<Q>`: The average representative-set size for each chunk. <br>
`<chunking_method>`: "seeded" or "sequential". You should use "seeded". <br>
`<top_subset_size>`: The size of the randomly-selected subset from the full set used for the seeded-chunking at the top level.

The output representative set (`representative_set_datasets`) is located in the directory `merge_of_chunks/`. If there are multiple levels of iterations, the final representative set is located under the lowest level of directory `merge_of_chunks/` by going down each `merge_of_chunks/` directory recursively.

## Direct representative set selection

The direct representative set selection computes the full similarity matrix of the original full set and performs representative set selection directly on the full similarity matrix using apricot. Use the following command to run the direct representative set selection:

```
direct_apricot_rep_set_selection.sh <fullset_fullpath_kmer_files> <representative_set_size> 
```
Where: <br>
`<fullset_fullpath_kmer_files>`:  A file containing the names of all the datasets' k-mer counts files (full-path) in the original full set, one filename per line. These k-mer counts files are gzipped. <br>
`<representative_set_size>`: The desired size of the representative set. <br>

The output representative set is `representative_set_datasets`.

## Random sampling

Random sampling randomly selects a subset from the original full set. Use the following command to run random sampling:

```
python select_random_subset_fullpath_files.py <fullset_fullpath_kmer_files> <subset_size>
```

Where: <br>
`<fullset_fullpath_kmer_files>`:  A file containing the names of all the datasets' k-mer counts files (full-path) in the original full set, one filename per line. These k-mer counts files are gzipped. <br>
`<subset_size>`: The desired size of the selected subset. <br>

The output subset is `selected_subset_datasets_fullpath`.

## Evaluating a representative set

The partial Hausdorff distance is used to evaluate how well a selected subset represents the original full set. Use the following command to compute both the partial Hausdorff distance and the classical Hausdorff distance:

```
hausdorff 17 <fullset_fullpath_kmer_files> <representative_set_datasets> <q>
```

The optimal k-mer size 17 is used here. Where: <br>
`<fullset_fullpath_kmer_files>`:  A file containing the names of all the datasets' k-mer counts files (full-path) in the original full set, one filename per line. These k-mer counts files are gzipped. <br>
`<representative_set_datasets>`: A file containing the names of the selected representative datasets' k-mer counts files (gzipped).
`<q>`: A parameter used in the partial Hausdorff distance: `q = 1 – K / |X|` where `|X|` is the size of the original full set, and `K` is for using the Kth largest value (counting from the minimum) as the partial Hausdorff distance. 


