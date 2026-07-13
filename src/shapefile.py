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
    "geometry",
    ]


def has_required_fields(gdf: gpd.GeoDataFrame) -> bool:
    """Checks that file contains required attributes"""
    required = [field not in gdf.columns for field in REQUIRED_FIELDS]
    if not all(required):
        is_required = [
            field
            for field, is_req in zip(REQUIRED_FIELDS, required)
            if is_req
        ]

        raise KeyError(f"Missing fields: Expects all of "
                       f"{', '.join(REQUIRED_FIELDS)}, "
                       f"missing {', '.join(is_required)}")
    else:
        return True


def is_geometry_polygon(gdf: gpd.GeoDataFrame) -> bool:
    """Returns True if geometry is Polygon or
    MutliPolygon"""
    gtypes = ['Polygon', 'MultiPolygon']
    return gdf.geometry.geom_type.isin(gtypes).all()


def is_geometry_closed(gdf: gpd.GeoDataFrame) -> bool:
    """Returns True if all geometries are closed"""
    return gdf.geometry.exterior.is_closed.all()


def is_single_year(gdf: gpd.GeoDataFrame) -> bool:
    """Returns True if all source dates are for single year"""
    if "src_date" in gdf:
        if gdf.src_date.dtype.kind == 'M':
            if len(gdf.src_date.dt.year.unique()) > 1:
                return False
            else:
                return True
        else:
            year = pd.to_datetime(gdf.src_date).dt.year
            if len(np.unique(year)) > 1:
                return False
            else:
                return True
    else:
        raise KeyError("src_date not found in columns")
    return False


def load_shapefile(
        filepath: str | Path,
        rename_columns: dict | None = None,
        drop_variables: list[str] = [],
        check_geometry: bool = True,
        check_years: bool = True,
) -> gpd.GeoDataFrane:
    """Loads a Shapefile or GeoJSON file and returns a geopandas.GeoDataFrame

    Arguments:
      filepath : path for file
      rename_columns : a dictionary containing a mapping for column names
      drop_variables: list of strings containing column names to drop
      check_geometry: if True (default), checks that geometry are Polygon
            or MultiPolygon and all polygons are closed.
      check_years: if True (default) checks that shapefile only contains
            features from a single year.

    Returns:
      geopandas.GeoDataFrame
    """
    gdf = gpd.read_file(filepath)

    if rename_columns:
        gdf.rename(columns=rename_columns, inplace=True)

    if drop_variables:
        gdf.drop(columns=drop_variables, inplace=True)

    if check_geometry:
        if not is_geometry_polygon(gdf):
            warnings.warn("Geometry column contains one or more geometries "
                          "that are not Polygon or MultiPolygon")

        if not is_geometry_closed(gdf):
            warnings.warn("One or more polygons are not closed")

    if check_years:
        if not is_single_year(gdf):
            warnings.warn(f"{filepath} contains outlines from multiple years.")

    return gdf
