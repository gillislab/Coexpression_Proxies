def read_cococonet(species_1):
    """[Takes a species name in any format, and returns a CoCoConet for that species]

    Args:
        species_1 ([str]): [Species in CoCoCoNet]

    Returns:
        [Panda Dataframe]: [GenexGene Matrix]
    """
    import h5py
    import pandas as pd
    import Name_resolver as nr

    assert (type(species_1) == str ), 'Species Must Be A String'

    common_name_of_species = nr.species_name_resolver(species_1= species_1, desired_type='common')


    cococonet_map = pd.read_csv('/data/passala/Generated_Tables/Reference_tables/All_CoCoCoNet_Paths.csv')
    file_location = cococonet_map['Path'].loc[cococonet_map['Common Name'] == common_name_of_species].item()

    net = h5py.File(file_location,'r')
    agg_dataset = net['agg'] 
    row_dataset = net['row']
    col_dataset = net['col']
    row_gene_list = []
    for gene in row_dataset:
        row_gene_list.append(gene.decode('UTF-8'))
    col_gene_list = []
    for gene in col_dataset: 
        col_gene_list.append(gene.decode('UTF-8'))
    net_df = pd.DataFrame(data = agg_dataset[:,:], index = row_gene_list, columns = col_gene_list)
    net.close()
    return net_df 