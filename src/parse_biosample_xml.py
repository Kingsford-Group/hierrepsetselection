# parse_biosample_xml.py
#
# Name: Laura Tung
#
# Usage: python parse_biosample_xml.py <xml_filename> <determinant_attributes_file> <BioSamples_list_file>
#
# <xml_filename>: filename of the xml file obtained by efecth for BioSamples_list.
# <determinant_attributes_file>: filename of the determinant attributes .csv file.
# <BioSamples_list_file>: filename of total BioSamples_list which contains one column of BioSample IDs.
#

#import pdb; pdb.set_trace() # Uncomment to debug code using pdb (like gdb)

import sys
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import pandas as pd

def handle_na_values(value):
    
    na_value_list = ["n/a", "na", "missing", "not available", "unavailable", "non available", "non-available", "nonavailable", "not applicable", "inapplicable", "non applicable", "non-applicable", "nonapplicable", "not determined", "undetermined", "non determined", "non-determined", "nondetermined", "not collected", "uncollected", "non collected", "non-collected"]
    
    if value.lower() in na_value_list:
        return ""
    else:
        return value

def get_attributes(root, determinant_attributes, total_biosamples_list):
    
    biosamples_list = []
    
    for biosample_set in root.findall('BioSampleSet'):

        for BioSample in biosample_set.findall('BioSample'):
            biosample_id = BioSample.get("accession")
            if biosample_id in total_biosamples_list:
                Attributes = BioSample.find('Attributes')

                harmonized_attributes_list = []
                for Attribute in Attributes.findall('Attribute'):
                    harmonized_name = Attribute.get('harmonized_name')
                    if harmonized_name:
                        value = Attribute.text
                        value = handle_na_values(value)
                        harmonized_attributes_list.append((harmonized_name, value))
        
                biosample_attributes = [biosample_id]
                for det_attribute in determinant_attributes:
                    found_pair = [pair for pair in harmonized_attributes_list if pair[0] == det_attribute]
                    if found_pair:
                        found_pair = found_pair[0]
                        biosample_attributes.append(found_pair[1])
                    else:
                        biosample_attributes.append("")
        
                biosamples_list.append(biosample_attributes)
    
    biosample_df = pd.DataFrame(biosamples_list, columns = ["BioSample"]+determinant_attributes)
    print("BioSample attributes dataframe:")
    print(biosample_df.info())
    
    return biosample_df


if __name__ == "__main__":

    xml_file = sys.argv[1]
    determinant_attr_file = sys.argv[2]
    BioSamples_list_file = sys.argv[3]
    
    total_biosamples_list = np.loadtxt(BioSamples_list_file, dtype='str')
    print("Shape of total_biosamples_list:", total_biosamples_list.shape)

    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    determinant_attr_df = pd.read_csv(determinant_attr_file, sep = ",", usecols=[0, 3], engine='python')
    print("Determinant Attributes dataframe:")
    print(determinant_attr_df.info())
    
    determinant_attr_name_col = determinant_attr_df.iloc[:, 0]
    determinant_attributes = list(determinant_attr_name_col)

    biosample_df = get_attributes(root, determinant_attributes, total_biosamples_list)
    
    f_name = xml_file[0:-4]
    
    pd.DataFrame.to_csv(biosample_df, path_or_buf=f_name+"_attributes.csv", index=False)
    
    biosample_names = biosample_df["BioSample"].to_numpy()
    print("Total number of used BioSamples with records extracted:", biosample_names.shape[0])
    np.savetxt("human_used_BioSamples_with_records", biosample_names, fmt='%s')
    
    print("DONE")
    

 

    
    
