"""Utilities for preparing Austrian Glacier Inventory"""

from itertools import chain
import re
import datetime as dt

import geopandas as gpd

instrument_short_names = {
    "DEM Hillshade Province of Carinthia": 'CarinthDEM',
    "DEM Hillshade Province of Salzburg": 'SalzbgDEM',
    "DEM Hillshade Province of Tyrol": 'TyrolDEM',
    "PlanetScope Orthoimagery": 'SuperDove',
    "Orthoimagery Federal Office of Metrology and Surveying - data.bev.gv.at": 'Aerial24',
    "Orthoimagery Province of Tyrol": 'Aerial20',
    "Orthoimagery Province of Salzburg": 'Aerial22',
    "Orthoimagery Province of Carinthia": 'Aerial21',
    "Orthoimagery Province of Vorarlberg": 'Aerial23',
    "UAV-borne photogrammetric survey by Geosphere Austria": 'GeosphUAV',
    }


def split_image_id(s):
    """Split image_id string"""
    if re.search(r'/', s):
        return s.split('/')
    else:
        return re.split(', ?', s)


def image_object(local_id, source, short_name,
                 source_date, image_id, geometry):
    return {
        "local_id": local_id,
        "instrument": source,
        "instrument_short_name": short_name,
        "source_date": dt.datetime.strptime(source_date, "%Y%m%d"),
        'image_id': image_id,
        'centroid': geometry,
    }


def parse_images(x):
    if re.search(r'/', x["image_ID1"]):
        # for two sources of image_id
        result = []
        for s in re.split(r'/', x["image_ID1"]):

            m = re.search(r'^([A-Za-z]+): (([0-9\-]+,* *)+)', s.strip())
            province, ids, _ = m.groups()

            # Determine source
            if province.lower() in x["source"].lower():
                source = x["source"]
            elif province.lower() in x["source2"].lower():
                source = x["source2"]
            else:
                source = x["source"]

            try:
                short_name = instrument_short_names[source]
            except KeyError as err:
                print(f"No short name mapping found for {source}")
                raise

            result += [
                image_object(
                    x["id"],
                    source,
                    short_name,
                    x["src_date"],
                    iid,
                    x["geometry"]
                ) for iid in re.split(', ?', ids.strip())
                ]
        return result

    else:
        return [
            image_object(
                x["id"],
                x["source"],
                instrument_short_names[x["source"]],
                x["src_date"],
                iid,
                x["geometry"].centroid
            ) for iid in re.split(', ?', x["image_ID1"])
            ]


def get_images_from_geodataframe(df: gpd.GeoDataFrame) -> list[dict[str, str, str, Point]]:
    """Extracts image source, source date, id and geometry from
    a geopandas.GeoDataFrame object

    Arguments:
      df : pandas.GeoDataFrame with source, src_date, image_ID1, and geometry columns

    Returns:
      list of dicts that contain local glacier id, name of image source, date of source image,
      image id and shapeley.geometry.Point
    """
    required_columns = [
        'source',
        'src_date',
        'image_ID1',
        'geometry',
    ]
    if not all([k in df for k in required_columns]):
        raise KeyError(f"Requires GeoDataFrame to have columns {', '.join(required_columns)}")

    return list(chain.from_iterable([parse_images(d) for d in df.to_dict(orient='records')]))
