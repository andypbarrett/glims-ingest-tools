"""QC and Homogenize Shapefile and extract relevant information for session.shp, 
images.shp, and input.shp"""

from pathlib import Path

import geopandas as gpd

REQUIRED_FIELDS = [
    "loc_unc_x",
    "loc_unc_y",
    "glob_unc_x",
    "glob_unc_y",
    "name",
    "orig_id",
    "acq_time",
    "inst_name",
    "data_src",
    "proc_desc",
    "anlst_surn",
    "anlst_givn",
    "3d_desc",
    "geometry",
    ]


GLACIER_REQUIRED_FIELDS = [
    "loc_unc_x",
    "loc_unc_y",
    "glob_unc_x",
    "glob_unc_y",
    "name",
    "geometry",
    ]
    
def check_required_fields(gdf: gpd.GeoDataFrame):
    """Checks that file contains required attributes"""
    required = [field not in gdf.columns for field in REQUIRED_FIELDS]
    if not all(required):
        is_required = [field for field, is_req in zip(REQUIRED_FIELDS, required)
                       if is_req]

        raise KeyError(f"Missing fields: Expects all of {', '.join(REQUIRED_FIELDS)}, "
                       f"missing {', '.join(is_required)}")
    else:
        return


def main():

    gdf = gpd.read_file(fp)

#    try:
#        check_required_fields(gdf)
    
