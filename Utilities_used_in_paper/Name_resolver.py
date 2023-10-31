def species_name_resolver(species_1,desired_type = 'common'):
    """[Takes ambiguous form of species name and returns desired type]

    Args:
        species_1 ([str]): [Ambigious Species Name]
        desired_type (str, optional): [One of common, scientific, or taxa_id]. Defaults to 'common'.

    Returns:
        [str]: [Specified Species ID]
    """

    import pandas as pd
    
    # Assert 
    assert (desired_type in ['common','scientific','taxa_id']), 'Desired type should be common, scientific, or taxa_id'
   
    #Set up variable 
    fc_mapper = pd.read_csv('/data/passala/Generated_Tables/Reference_tables/Species_name_resolver.csv')

    #Convert Taxa to common names if NCBI taxa ID
    if type(species_1) == int:
        species_1 = fc_mapper['Common Name'].loc[fc_mapper['Taxa ID'] == species_1].item()

    #Convert scientific name to common names if given scientific
    if ' ' in species_1:
        species_1 = fc_mapper['Common Name'].loc[fc_mapper['Species'] == species_1].item()

    #Get Scientific Name
    scientific_1 = fc_mapper['Species'].loc[fc_mapper['Common Name'] == species_1].item()
    taxa_id_1 = fc_mapper['Taxa ID'].loc[fc_mapper['Common Name'] == species_1].item()

    if desired_type == 'common':
        return species_1
    elif desired_type =='scientific':
        return scientific_1
    elif desired_type == 'Taxa ID':
        return taxa_id_1