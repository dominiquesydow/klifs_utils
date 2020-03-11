"""
klifs_utils
Utility functions to work with KLIFS data

Select a set of kinase groups, kinase families, kinase names, or kinase KLIFS IDs.
"""

from bravado.client import SwaggerClient
import pandas as pd

from klifs_utils.util import abc_idlist_to_dataframe

KLIFS_API_DEFINITIONS = "http://klifs.vu-compmedchem.nl/swagger/swagger.json"
KLIFS_CLIENT = SwaggerClient.from_url(KLIFS_API_DEFINITIONS, config={'validate_responses': False})


def kinase_groups():
    """
    Get all kinase groups.

    Returns
    -------
    list of str
        Kinase group names.
    """

    return KLIFS_CLIENT.Information.get_kinase_groups().response().result


def kinase_families(kinase_group=None):
    """
    Get all kinase families for a kinase group.

    Parameters
    ----------
    kinase_group : None or str
        Kinase group name.

    Returns
    -------
    list of str
        Kinase family names.
    """

    return KLIFS_CLIENT.Information.get_kinase_families(
        kinase_group=kinase_group
    ).response().result


def kinase_names(kinase_group=None, kinase_family=None, species=None):
    """
    Get all kinase names for kinases belonging to a given kinase group, kinase family and/or species.

    Parameters
    ----------
    kinase_group : str
        Kinase group name.
    kinase_family : str
        Kinase family name.
    species : str
        Species name.

    Returns
    -------
    pandas.DataFrame
        Kinase names with details.
    """

    results = KLIFS_CLIENT.Information.get_kinase_names(
        kinase_group=kinase_group,
        kinase_family=kinase_family,
        species=species
    ).response().result

    return abc_idlist_to_dataframe(results)


def kinase_from_kinase_name(kinase_name, species=None):
    """
    Get all kinases belonging to a given kinase group, kinase family, species and/or with a given kinase name.

    Parameters
    ----------
    kinase_name : str
        Kinase name.
    species : None or str
        Species name.

    Returns
    -------
    pandas.DataFrame
        Kinase(s) details.
    """

    results = KLIFS_CLIENT.Information.get_kinase_ID(
        kinase_name=kinase_name,
        species=species
    ).response().result

    return abc_idlist_to_dataframe(results)


def kinase_from_kinase_ids(kinase_ids):
    """
    Get all kinases for KLIFS kinase ID(s).

    Parameters
    ----------
    kinase_ids : int or list of int
        KLIFS kinase ID(s).

    Returns
    -------
    pandas.DataFrame
        Kinase(s) details.
    """

    if isinstance(kinase_ids, int):
        kinase_ids = [kinase_ids]

    results = []

    for kinase_id in kinase_ids:

        result = KLIFS_CLIENT.Information.get_kinase_information(
            kinase_ID=[kinase_id]
        ).response().result
        result_df = abc_idlist_to_dataframe(result)
        result_df.insert(0, 'ligand_id', kinase_id, True)
        results.append(result_df)

    return pd.concat(results)