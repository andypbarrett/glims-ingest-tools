"""Utilities for creating SQL"""
import re

def to_point(coords: tuple, crs: str="4326"):
    """Return PostgreSQL formatted Point

    Arguments:
      coords : tuple containing latitude and longitude
      crs : coordinate reference system as EPSG code
    """
    return f"GeomFromEWKT('SRID={crs};POINT({coords[0]} {coords[1]} 0)')"


def set_missing(value):
    """Sets empty fields to NULL

    Arguments:
      value : value

    Return:
      string with NULL if empty
    """
    if (
            (str(value) == "") or
            (str(value) == '""') or
            (str(value) == "''")
            ):
        return "NULL"
    else:
        return str(value)


def sqlize_quotes(value):
    """Protects single and double quotes"""
    value = str(value).replace("'", "''")
    value = str(value).replace('"', '\\"')
    return value


def is_empty(value):
    """Checks for empty string"""
    if (
            (str(value) == "") or
            (str(value) == '""') or
            (str(value) == "''")
    ):
        return True
    else:
        return False


def is_number(value):
    """Checks if string is number"""
    return re.match(r"^-?\d+\.?\d*$", value)


def is_geom(value):
    """Checks if value is Geometry string"""
    return re.match(r"^Geom", value)


def is_default(value):
    """Returns True is value is DEFAULT"""
    return re.match(r"^DEFAULT$", value)


def is_boolean_str(value):
    """Returns True if value is string containing True or False
    It is case insensitive
    """
    if (
            re.match(r"^true$", value, re.IGNORECASE) or
            re.match(r"^false$", value, re.IGNORECASE)
    ):
        return True
    else:
        return False


def is_null(value):
    """Returns True is value is NULL"""
    return re.match(r"^NULL$", value)


def is_reserved(value):
    """Returns True is value is reserved word"""
    if (
            is_default(value) or
            is_boolean_str(value) or
            is_null(value)
    ):
        return True
    else:
        return False


def sqlize_value(value):
    """Parses value to conform to SQL

    Arguments:
      value : value to be parsed

    Returns:
      SQLized value
    """

    value = str(value)

    if is_empty(value):
        return "NULL"

    if not (
            is_number(value) or
            is_geom(value) or
            is_reserved(value)
    ):
        return f"'{sqlize_quotes(value)}'"  # quote value

    return value
