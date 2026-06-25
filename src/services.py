"""Querys glims.org/services"""

import requests
from collections import namedtuple

ROOT_URL = "https://www.glims.org/services"

NextIDs = namedtuple(
    'NextIDs',
    [
        'analysis_id',
        'contact_id',
        'image_id',
        'map_id',
        'rc_id',
        'submission_id'
    ]
)


def query_service(query_str: str):
    """Send query to glims.org/services"""

    try:
        r = requests.get(query_str)
        r.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    return r.json()


def get_people(name: str = None) -> list[dict]:
    """Returns list of people from GLIMS DB

    Arguments:
      name : a name to search for.  If None, returns all names

    Returns:
      List of names
    """

    names = name.split()
    if len(names) == 1:
        surname = names[0]
    elif len(names) == 2:
        surname, given_name = names
    else:
        raise ValueError(f"Expected either surname or surname "
                         f"and given name, got {name}")

    query = f"{ROOT_URL}/people/{surname.lower()}"

    response = query_service(query)

    return response


def get_next_ids(id_type: str = None) -> list(dict):
    """Returns Ordered Tuple with next ids for
    analysis_id, contact_id, image_id, map_id, rc_id,
    and submission_id

    Arguments:
      id_type : name of id to return.  If None (default) returns all

    Returns:
      ordered tuple containing ids
    """

    query = f"{ROOT_URL}/next_ids"

    response = query_service(query)

    return NextIDs._make(response.values())
