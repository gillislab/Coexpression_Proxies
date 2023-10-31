def get_go_annotations_as_panda(species):
    """[Takes a Species name in Any Format, and returns a matrix of Genes x Go Terms in binarized format]

    Args:
        species ([str]): [A species in Cococonet]

    Returns:
        [Panda Dataframe]: [Genes x Go terms in binarized format]
    """
    import pandas as pd
    import Name_resolver as nr
    ## TAXA_ID to species_name

    assert (type(species) == str ), 'Species Must Be A String'

    species = nr.species_name_resolver(species_1= species, desired_type='common')

    ## Get file_location
    file_location = '/data/CoCoCoNet/gene2go/' + species + '_gene2go.csv'
    original_csv = pd.read_csv(file_location, sep=' ')

    ## Check File Location has annotations
    if len(original_csv) == 0:
        raise NameError('No Annotations for this Species :(')
    ## Clean and Output    
    original_csv = original_csv.dropna()
    original_csv['Present'] = 1
    matrixed_version = original_csv.pivot(index='NetworkIDs',
                                          columns='GO_term',
                                          values='Present')
    filled_matrixed_version = matrixed_version.fillna(value=0)
    return filled_matrixed_version