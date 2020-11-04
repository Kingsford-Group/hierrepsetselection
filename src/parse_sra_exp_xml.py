# parse_sra_exp_xml.py
#
# Name: Laura Tung
#
# Usage: python parse_sra_exp_xml.py <xml_filename>
#
# <xml_filename>: filename of the xml file obtained by efecth for many SRA Experiments.

#import pdb; pdb.set_trace() # Uncomment to debug code using pdb (like gdb)

import sys
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import random
import pandas as pd

def check_single_cell(exp, design, lib_des, sample, study):
    
    exp_title = exp.find('TITLE')
    if (exp_title != None) and (exp_title.text != None):
        if ("single cell" in exp_title.text.lower()) or ("single-cell" in exp_title.text.lower()):
            return True
        
    design_des = design.find('DESIGN_DESCRIPTION')
    if (design_des != None) and (design_des.text != None):
        if ("single cell" in design_des.text.lower()) or ("single-cell" in design_des.text.lower()):
            return True
        
    lib_constr_protocol = lib_des.find('LIBRARY_CONSTRUCTION_PROTOCOL')
    if (lib_constr_protocol != None) and (lib_constr_protocol.text != None):
        if ("single cell" in lib_constr_protocol.text.lower()) or ("single-cell" in lib_constr_protocol.text.lower()):
            return True
        
    sample_title = sample.find('TITLE')
    if (sample_title != None) and (sample_title.text != None):
        if ("single cell" in sample_title.text.lower()) or ("single-cell" in sample_title.text.lower()):
            return True
        
    sample_des = sample.find('DESCRIPTION')
    if (sample_des != None) and (sample_des.text != None):
        if ("single cell" in sample_des.text.lower()) or ("single-cell" in sample_des.text.lower()):
            return True
        
    study_desptor = study.find('DESCRIPTOR')
    study_title = study_desptor.find('STUDY_TITLE')
    if (study_title != None) and (study_title.text != None):
        if ("single cell" in study_title.text.lower()) or ("single-cell" in study_title.text.lower()):
            return True
        
    study_abstr = study_desptor.find('STUDY_ABSTRACT')
    if (study_abstr != None) and (study_abstr.text != None):
        if ("single cell" in study_abstr.text.lower()) or ("single-cell" in study_abstr.text.lower()):
            return True
        
    study_des = study_desptor.find('STUDY_DESCRIPTION')
    if (study_des != None) and (study_des.text != None):
        if ("single cell" in study_des.text.lower()) or ("single-cell" in study_des.text.lower()):
            return True
    
    return False

def get_sra_run(run_set):
    
    if run_set == None:
        return None
    
    run_accessions_list = []
    for run in run_set.findall('RUN'):
        run_accession = run.get('accession')
        if run_accession:
            run_accessions_list.append(run_accession)
            
    if run_accessions_list:
        # randomly select one accession
        return random.choice(run_accessions_list)
    else:
        return None

def check_sample_organism(sample):
    
    sample_name = sample.find('SAMPLE_NAME')
    if sample_name != None:
        scientific_name = sample_name.find('SCIENTIFIC_NAME')
        if (scientific_name != None) and (scientific_name.text == 'Homo sapiens'):
            return True
        
    return False

def get_sra_exps(root):
    
    criteria_count = 0
    biosample_count = 0
    sra_run_count = 0
    non_sinlge_cell_count = 0
    
    exp_data_list = []
    biosample_dict = {}

    for exp_pack_set in root.findall('EXPERIMENT_PACKAGE_SET'):
        for exp_pack in exp_pack_set.findall('EXPERIMENT_PACKAGE'):
            exp = exp_pack.find('EXPERIMENT')
            exp_accession = exp.get('accession')
            # make sure it has SRA Experiment accession
            if exp_accession:
                sample = exp_pack.find('SAMPLE')
                if (sample != None) and check_sample_organism(sample):
                    design = exp.find('DESIGN')
                    lib_des = design.find('LIBRARY_DESCRIPTOR')
                    platform = exp.find('PLATFORM')
                    if (lib_des.find('LIBRARY_STRATEGY').text == 'RNA-Seq') and (platform.find('ILLUMINA') != None):
                        # have confirmed our search criteria.
                        criteria_count += 1
                        
                        # make sure it has BioSample ID
                        identifiers = sample.find('IDENTIFIERS')
                        ext_ids = identifiers.findall('EXTERNAL_ID')
                        if ext_ids:
                            e_ids = [e_id for e_id in ext_ids if e_id.get('namespace') == "BioSample"]
                            if e_ids:
                                ext_id = e_ids[0]
                                biosample_id = ext_id.text
                                biosample_count += 1
                                
                                # make sure it has SRA Run accession
                                run_set = exp_pack.find('RUN_SET')
                                run_accession = get_sra_run(run_set)
                                if run_accession:
                                    sra_run_count += 1
                                    
                                    # filter out single cell RNA-seq
                                    if not check_single_cell(exp, design, lib_des, sample, exp_pack.find('STUDY')):
                                        non_sinlge_cell_count += 1
                                        
                                        # now everything is good, we can keep this record
                                        # first, get all the needed attributes for this exp
                                        selection_method = lib_des.find('LIBRARY_SELECTION').text
                                        lib_layout = lib_des.find('LIBRARY_LAYOUT')
                                        if lib_layout.find('PAIRED') != None:
                                            layout = "PAIRED"
                                        else:
                                            layout = "SINGLE"
                                        inst_model = platform.find('ILLUMINA').find('INSTRUMENT_MODEL')
                                        instrument = inst_model.text
                                        lib_constr_protocol = lib_des.find('LIBRARY_CONSTRUCTION_PROTOCOL')
                                        if (lib_constr_protocol != None) and (lib_constr_protocol.text != None):
                                            construction_protocol = lib_constr_protocol.text
                                        else:
                                            design_des = design.find('DESIGN_DESCRIPTION')
                                            if (design_des != None) and (design_des.text != None):
                                                construction_protocol = design_des.text
                                            else:
                                                construction_protocol = ""
                                    
                                        #print("SRA_Experiment=", exp_accession, ";", "BioSample=", biosample_id, ";", "SRA_Run=", run_accession, ";", "instrument=", instrument, ";", "selection_method=", selection_method, ";", "layout=", layout, ";", "construction_protocol=", construction_protocol)
                                        exp_data_list.append([exp_accession, biosample_id, run_accession, instrument, selection_method, layout, construction_protocol])
                                    
                                        # store in biosample dictionary
                                        if biosample_id in biosample_dict:
                                            biosample_dict[biosample_id].append(exp_accession+":"+run_accession)
                                        else:
                                            biosample_dict[biosample_id] = [exp_accession+":"+run_accession]

    print("Total # of qualified SRA Experiments:", len(exp_data_list))                  
    exp_df = pd.DataFrame(exp_data_list, columns = ["SRA_Experiment", "BioSample", "SRA_Run", "instrument", "selection_method", "layout", "construction_protocol"])
    print("SRA Experiments dataframe:")
    print(exp_df.info())
    
    print("Total # of used BioSamples:", len(biosample_dict))
    biosample_list = [(k, ';'.join(v)) for k, v in biosample_dict.items()]
    biosample_df = pd.DataFrame(biosample_list, columns = ['BioSample', 'SRA_Experiments'])
    print("BioSamples dataframe:") 
    print(biosample_df.info())
    
    print("met_criteria_count:", criteria_count)
    print("has_biosample_count:", biosample_count)
    print("has_sra_run_count:", sra_run_count)
    print("non_sinlge_cell_count:", non_sinlge_cell_count)
    
    return (exp_df, biosample_df, biosample_dict)


if __name__ == "__main__":

    xml_file = sys.argv[1]

    tree = ET.parse(xml_file)
    root = tree.getroot()

    exp_df, biosample_df, biosample_dict = get_sra_exps(root)
    
    f_name = xml_file[0:-4]
    
    pd.DataFrame.to_csv(exp_df, path_or_buf=f_name+"_SRA_Exps.csv", index=False)
    pd.DataFrame.to_csv(biosample_df, path_or_buf=f_name+"_BioSamples.csv", index=False)
    
    f = open(f_name+"_BioSamples_list", 'w')
    for key in biosample_dict.keys():
        f.write(key+'\n')
    f.close()
    
    print("DONE")
    

 

    
    
