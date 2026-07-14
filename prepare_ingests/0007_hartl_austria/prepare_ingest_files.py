"""Prepare Austrian Glacier Inventory Ingest Files

The Austrian Glacier Inventory has separate files for each of the 20 regions.  

Currently, GLIMS is set up to ingest files by year.  So the 20 GeoJSONS are merged and split into separate years.
"""

from pathlib import Path
import re
import json
import datetime as dt
import warnings

#from itertools import chain

import geopandas as gpd
import pandas as pd

from glims_ingest_tools.writers import make_image_gmt, make_session_gmt
from glims_ingest_tools.classes import NewSubmission
#from glims_ingest_tools.shapefile import GLACIER_REQUIRED_FIELDS
from glims_ingest_tools.shapefile import (is_single_year,
                                          is_geometry_polygon,
                                          is_geometry_closed,
                                          is_multipolygon,
                                          multipolygon2polygon)

from utils import get_images_from_geodataframe


DATAPATH = Path.home() / "Data" / "GLIMS" / "submissions" / "0007_hartl_austria" / "GI5_v2"
SUBMISSON_PATH = DATAPATH / "submission"
FOR_INGEST_PATH = DATAPATH / "for_ingest"
PREPROCESSED_PATH = DATAPATH / "preprocessed"

write_file = True  # Set True to write files

analysis_time = dt.datetime(2025,11,1)  # we use November 2025 as suggested by Lea Hartl
session_data_source = "Aerial orthoimagery, high-resolution satellite images and Lidar DEMs"
session_process_description = "Manual Digitization"


def get_region_name_from_filepath(filepath: Path) -> str:
    """Returns region name as string"""
    region = re.search(r'(.+)_GI5_proc2.geojson', filepath.name)  # Get region name
    return region.group(1)


def load_metadata(fp: Path) -> dict:
    """Returns dict containing metadata"""
    with open(fp, "r") as f:
        metadata = json.load(f)
    return metadata


def load_subregions(fp: Path) -> dict:
    """Returns dict containing subregion metadata"""
    with open(fp, "r") as f:
        subregions = json.load(f)
    return subregions


def load_source_lookup() -> dict:
    """Returns lookup table to translate and homogenize image source names"""
    with open('geojson_abbreviations_lookup.json', 'r') as f:
        source_lookup = json.load(f)
    return source_lookup


def homogenize_image_source_name(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Returns homogenized GeoDataFrame with consistent image source names

    Arguments:
      gdf : raw GeoDataFrame loaded from AGI5 GeoJSON

    Returns:
      homogenized GDF
    """
    source_lookup = load_source_lookup()

    # Some source names for Land Tirol have multiple references.  These are
    # set to just LBA
    gdf["source"] = gdf["source"].where(gdf.source.str.contains("LBA") == False, "LBA")

    # Split `source` with two valid sources between `source` and `source_2`
    tmp_index = gdf.source == 'Land Salzburg, Land Tirol'
    gdf.loc[tmp_index, "source"] = "Land Tirol"
    gdf.loc[tmp_index, "source_2"] = "Land Salzburg"

    # Homogenize source and source 2 using `source_lookup`
    gdf["source"] = gdf.source.map(source_lookup)
    gdf["source_2"] = gdf.source_2.map(source_lookup)

    return gdf


def fix_source_date_string(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Fix source_date datestrings

    Arguments:
      gdf : raw GeoDataFrame loaded from AGI5 GeoJSON

    Returns:
      homogenized GDF

    Dates that have XX as day are set to 01
    Dates that just assign year are set to 1 Jan (e.g. YYYY0101)
    """
    gdf['src_date'] = gdf.src_date.str.replace(r'XX', '01')
    gdf['src_date'] = gdf.src_date.where(gdf.src_date.str.match(r'^\d{8}$'), gdf.src_date + '0101')

    assert len(gdf) == gdf.src_date.str.match(r'^\d{8}$').sum()  # Assume either correct or two incorrect date formats

    return gdf


def assign_uncertainty(gdf):
    """Returns GeoDataFrame with local and global uncertainties assigned
    based on source image type.  These uncertainties are estimated from
    Hartl et al. 2026.

    Estimates of local uncertainty in `x` and `y` directions are based on pixel sizes.  
    We take the upper bound of uncertainty for each source.

    Estimates of global uncertainty are based on 2 pixel widths (heights) for each source-type.

    |Source-Type|Local Uncertainty (m)|Global Uncertainty (m)|
    |-----------|----------|---------|
    |Aerial Orthoimagery| 0.10 to 0.25 |0.5|
    |DEM Hillshade| 0.5 to 1.0 |2.0|
    |Pleiades| 0.5 |1.0|
    |Planetscope|3.0|6.0|

    Where multiple image sources are used, we assign the uncertainty associated with the largest uncertainty.
    """

    uncertainty_lookup = {
        'orthoimagery': {
            'local': 0.25,
            'global': 0.5,
            },
        'pleiades': {
            'local': 0.5,
            'global': 1.0,
            },
        'dem': {
            'local': 1.0,
            'global': 2.0,
            },
        'planetscope': {
            'local': 3.0,
            'global': 6.0,
            },
        }

    def source_type(x):
        if (
                ('orthoimage' in x.source.lower()) &
                ('dem' not in x.source.lower()) &
                ('planetscope' not in x.source.lower())
        ):
            return 'orthoimagery'
        elif ('orthoimage' in x.source.lower()) & ('dem' in x.source.lower()):
            return 'dem'
        elif (
                ('dem' in x.source.lower()) &
                ('orthoimage' not in x.source.lower())
        ):
            return 'dem'
        elif ('planetscope' in x.source.lower()):
            return 'planetscope'
        elif ('photogrammetric' in x.source.lower()):
            return 'orthoimagery'

    gdf['loc_unc_x'] = gdf.apply(source_type, axis=1).map(
        {
            k: v['local'] for k, v in uncertainty_lookup.items()
        }, axis=1
    )
    gdf['loc_unc_y'] = gdf.apply(source_type, axis=1).map(
        {
            k: v['local'] for k, v in uncertainty_lookup.items()
        }, axis=1
    )
    gdf['glob_unc_x'] = gdf.apply(source_type, axis=1).map(
        {
            k: v['global'] for k, v in uncertainty_lookup.items()
        }, axis=1
    )
    gdf['glob_unc_y'] = gdf.apply(source_type, axis=1).map(
        {
            k: v['global'] for k, v in uncertainty_lookup.items()
        }, axis=1
    )

    return gdf


def make_glacier_shapefile(gdf: gpd.GeoDataFrame,
                           split_multipolygon: bool = False) -> gpd.GeoDataFrame:
    """Creates GeoDataFrame for glaciers.shp

    Arguments:
      gdf : GeoDataFrame object for original GeoJSON
      split_multipolygon : split MultiPolygons

    Returns:
      GeoDataFrame with columns and structure of glacier.shp

    `glaciers.shp` requires the following fields.
    - `loc_unc_x`  The local positional uncertainty of _x_ in m,
                   based on grid cell size
    - `loc_unc_y`  The local positional uncertainty of _y_ in m,
                   based on grid cell size
    - `glob_unc_x` Positional uncertainty of _x_ in m based on
                   geolocation uncertainty
    - `glob_unc_y` Positional uncertainty of _y_ in m based on
                   geolocation uncertainty
    - `name`  Name of glacier if one exists, "" if no name exists.

    As well as geometry column.

    For AGI5, the local glacier id is retained as `local_id`.  The glacier area
    is also retained.

    For AGI5 local and global uncertainties are assigned based on source
    image type.
    """

    # mappable for old-to-new column names
    glacier_column_names = {
        'id': 'local_id',         # glacier ID number for AGI
        'name': 'name',           # glacier name as per AGI
        'src_date': 'src_date',   # date of image/data acquisition.
        'area': 'area_m2',        # glacier area in m2, computed original CRS
    }
    glacier_gdf = gdf.rename(columns=glacier_column_names)[
        list(glacier_column_names.values()) + ['geometry', 'source']
    ]

    glacier_gdf['local_id'] = glacier_gdf['local_id'].astype(str)

    glacier_gdf = assign_uncertainty(glacier_gdf)

    glacier_gdf["src_date"] = glacier_gdf.src_date.dt.strftime("%Y%m%d")

    if split_multipolygon:
        if glacier_gdf.apply(is_multipolygon, axis=1).any():
            multipolygon2polygon(glacier_gdf)

    return glacier_gdf


def prepare_one_region(filepath: Path) -> None:
    """Prepares ingest files for one region

    Arguments:
      filepath : Path to glacier outline GeoJSON
    """

    # Load ancilliary data
    metadata = NewSubmission.from_json(
        PREPROCESSED_PATH / "metadata_template.json"
    )
    subregions = load_subregions(PREPROCESSED_PATH / "subregions.json")

    # Get region metadata for region of interest
    region_name = get_region_name_from_filepath(filepath)

    region_metadata = [
        subregion for subregion in subregions
        if subregion["name"] == ' '.join(region_name.split('_'))
    ][0]

    # Load GeoJSON with glacier outlines
    gdf = load_shapefile(filepath)

    # For each year loop through outlines
    for year, group in gdf.groupby(gdf.src_date.dt.year):

        # Make directory under FOR_INGEST_PATH to hold region files
        REGION_INGEST_PATH = PREPROCESSED_PATH / region_name.lower() / str(year)
        REGION_INGEST_PATH.mkdir(parents=True, exist_ok=True)

        # Extract region metadata in WGS84
        dataset_centroid = (
            gpd.GeoSeries(
                [group.centroid.union_all().centroid],
                crs=group.crs
            ).to_crs(4326)[0].x,
            gpd.GeoSeries(
                [group.centroid.union_all().centroid],
                crs=group.crs
                ).to_crs(4326)[0].y
            )  # Done in native CRS to avoid complications of centroid in ll

        group = group.to_crs(4326)
        shapefile_bounds = group.total_bounds

        # Extract GeoJSON of Images
        images = get_images_from_geodataframe(group)

        # Create `image.gmt`
        image_gmt_str = make_image_gmt(shapefile_bounds, group.crs.to_wkt(), images)
        if write_file:
            with open(REGION_INGEST_PATH / "images.gmt", "w") as fo:
                fo.write(image_gmt_str)
        else:
            print(image_gmt_str)

        # Create `session.gmt`
        analysts = [
            (analyst["analyst"]["surname"], analyst["analyst"]["first_name"])
            for analyst in region_metadata["analysts"]
        ]
        analysts.append(("Hartl", "Lea"))  # Add Lea Hartl
        session_gmt_str = make_session_gmt(
            shapefile_bounds,
            group.crs.to_wkt(),
            metadata.rc_id,
            analysis_time,
            session_data_source,
            session_process_description,
            analysts,
            "",
            dataset_centroid,
        )
        if write_file:
            with open(REGION_INGEST_PATH / "session.gmt", "w") as fo:
                fo.write(session_gmt_str)
        else:
            print(session_gmt_str)

        # Create metadata.txt
        metadata.file_name = filepath.name
        metadata.file_size = filepath.stat().st_size
        if write_file:
            metadata.write_metadata_file(REGION_INGEST_PATH / "metadata.txt")
        else:
            metadata.print_metadata_file()

        # Create glaciers.shp
        glacier_group = make_glacier_shapefile(group)

        if write_file:
            glacier_group.to_file(REGION_INGEST_PATH / "preprocessed_outlines.shp")


def load_shapefile(fp):
    """Loads and homogenizes shapefile"""
    gdf = gpd.read_file(fp)
    gdf = homogenize_image_source_name(gdf)
    gdf = fix_source_date_string(gdf)
    gdf.src_date = pd.to_datetime(gdf.src_date)
    return gdf


def prepare_ingest_files():
    """Generates ingest files for all regions of Austrian Glacier Inventory"""
    OUTLINE_FILES = sorted(
        [
            f for f in SUBMISSON_PATH.glob("*.geojson")
            if "vanishing" not in f.name
        ]
    )

    for fp in OUTLINE_FILES:
        print(f"Processing {fp.name}")
        prepare_one_region(fp)


if __name__ == "__main__":
    prepare_ingest_files()
