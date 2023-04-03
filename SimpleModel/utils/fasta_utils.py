import os

def get_protein_name(line):
    protein_name = " ".join(line.split()[1:]).lower()
    return protein_name

def get_all_features(folder_location):
    """
    Params: folder_location: string
            The location of the folder which contains all the fasta files
    Returns: A list of all proteins found in all the files
    """
    file_list = os.listdir(folder_location)
    
    unique_protein_list = []

    for i, file in enumerate(file_list):
        print(f"Processing file {i}/{len(file_list)}")
        with open(folder_location+file, "r") as file:
            for line in file:
                if line.startswith(">"):
                    protein_name = get_protein_name(line)
                    if protein_name not in unique_protein_list:
                        unique_protein_list.append(protein_name)
    return unique_protein_list

def binary_protein_vector(protein_list, master_list):
    binary_vector = [1 if protein in protein_list else 0 for protein in master_list]
    return binary_vector

def common_proteins(folder_location, master_list):

    common_set = set(master_list)
    file_list = os.listdir(folder_location)
    for i, file in enumerate(file_list):
        # print(f"Processing file {i}/{len(file_list)}")
        protein_list = []
        with open(folder_location+file, "r") as file:
            for line in file:
                if line.startswith(">"):
                    protein_name = get_protein_name(line)
                    if protein_name not in protein_list:
                        protein_list.append(protein_name)

        protein_set = set(protein_list)
        common_set = common_set.intersection(protein_set)

    return list(common_set)


if __name__ == "__main__":
    folder_name = "../../Features/"
    
    get_all_features(folder_name)

