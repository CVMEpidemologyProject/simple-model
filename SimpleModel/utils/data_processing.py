import os
import re
import copy
import pandas as pd
from utils.fasta_utils import *


def get_substring_between(string, start_str, end_str):
    start_index = string.find(start_str)
    if start_index == -1:
        return ""
    end_index = string.find(end_str, start_index + len(start_str))
    if end_index == -1:
        return ""
    return string[start_index + len(start_str):end_index]

def create_dataset(folder_location, antibiotic):
    """
    Params: folder_location: string
            location of the folder in which all fasta files are downloaded

    Returns: df_final: Pandas dataframe
            Pandas dataframe with X values as names of proteins, y as MIC
    """
    # mic files
    df_mic = pd.read_excel("../a4ed1601ccb774eaf3b9c5f44b1a6bc3_JCM.01260-18-s0002.xlsx",
                            skiprows=1, index_col="PATRIC ID")
    df_mic = df_mic[df_mic["Antibiotic"] == antibiotic]
    y_list = []
    # fasta files
    all_proteins = get_all_features(folder_location)
    common_protein_list = common_proteins(folder_location, all_proteins)
    unique_proteins = list(set(all_proteins)-set(common_protein_list))

    df_final = pd.DataFrame(columns=unique_proteins)

    file_list = os.listdir(folder_location)
    for i, file in enumerate(file_list):

        print(f"Creating dataset: file {i}/{len(file_list)}")
        protein_list = []
        with open(folder_location+file, "r") as file:
            for line in file:
                if line.startswith(">"):
                    protein_name = get_protein_name(line)
                    if protein_name not in protein_list:
                        protein_list.append(protein_name)


        index = get_substring_between(str(file), "features_", ".fasta'")
        df_final.loc[float(index)] = binary_protein_vector(protein_list, unique_proteins)

        
        y_indi = df_mic.loc[float(index)]["Laboratory-derived MIC"]
        y_indi = re.sub('[^0-9]', '', y_indi)
        y_list.append(y_indi)

    df_final["Target"] = y_list
    return df_final

if __name__ == "__main__":
    create_dataset("../../Features1/", "AUG")