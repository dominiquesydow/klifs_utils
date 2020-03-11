"""
klifs_utils
Utility functions to work with KLIFS data

Get interaction details.
"""

from bravado.client import SwaggerClient

from klifs_utils.util import abc_idlist_to_dataframe

KLIFS_API_DEFINITIONS = "http://klifs.vu-compmedchem.nl/swagger/swagger.json"
KLIFS_CLIENT = SwaggerClient.from_url(KLIFS_API_DEFINITIONS, config={'validate_responses': False})


def interaction_types():
    """
    Get KLIFS interaction types.

    Returns
    -------
    pandas.DataFrame
        KLIFS interaction types.
    """

    result = KLIFS_CLIENT.Interactions.get_interactions_get_types().response().result

    return abc_idlist_to_dataframe(result)


def interaction_fingerprint(structure_ids):
    """
    Get interaction fingerprint from KLIFS structure ID(s).

    Parameters
    ----------
    structure_ids : int or list of int
        KLIFS structure ID(s).

    Returns
    -------
    pandas.DataFrame
        KLIFS interaction fingerprint(s).
    """

    if isinstance(structure_ids, int):
        structure_ids = [structure_ids]

    result = KLIFS_CLIENT.Interactions.get_interactions_get_IFP(
        structure_ID=structure_ids
    ).response().result

    return abc_idlist_to_dataframe(result)


def klifs_pocket_numbering(structure_id):
    """
    Get KLIFS pocket numbering (PDB vs. KLIFS numbering).

    Parameters
    ----------
    structure_id : int
        KLIFS structure ID.

    Returns
    -------
    pandas.DataFrame
        KLIFS pocket numbering.
    """

    result = KLIFS_CLIENT.Interactions.get_interactions_match_residues(
        structure_ID=structure_id
    ).response().result

    return abc_idlist_to_dataframe(result)