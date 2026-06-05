"""Write files for ingest"""

import pyproj
import datetime as dt


GMT_VERSION = "# @VGMT1.0 @GPOINT"


def make_region_str(bbox: tuple) -> str:
    """Returns a GMT format region string"""
    return f"# @R{bbox[0]:.4f}/{bbox[1]:.4f}/{bbox[2]:.4f}/{bbox[3]:.4f}"


def make_crs_str(crs_wkt: str) -> str:
    """Returns a GMT format CRS WKT string"""
    return f'# @Jw{crs_wkt}'


def make_feature_data_str(regional_center: str, analysis_time: str,
                          data_source: str, process_description: str,
                          analyst_surname: str, analyst_given: str,
                          description_3d: str, centroid: tuple) -> str:
    """Return a feature data GMT formatted string"""
    return (f'# @D{regional_center}|{analysis_time.strftime("%Y-%m-%d")}|'
            f'\"{data_source}\"|\"{process_description}\"|'
            f'{analyst_surname}|{analyst_given}|\"{description_3d}\"\n'
            f'{centroid[0]:.1f} {centroid[1]:.1f}')


def session_to_gmt(
        bbox: tuple,
        crs_wkt: str,
        regional_center: str,
        analysis_time: dt.datetime,
        data_source: str,
        process_description: str,
        analyst: list,
        description_3d: str,
) -> str:
    """Write a session_input.gmt file

    Arguments:
      bbox : tuple containing bounding box for regions (lon_min, lon_max, lat_min, lat_max)
      crs_wkt : CRS in WKT format
      regional_center : regional center id
      analysis_time : analysis time - this may be general
      data_source : description of data source
      process_description : description of mapping process; e.g. manual digitization
      analyst : list of analysts as tuples (surname, given_name)
      description_3d : description of 3-dimensional data source

    Returns:
      formatted string object containing a session file
    """

    DATA_HEADER = [
        '# @Nrc_id|analy_time|data_src|proc_desc|anlst_surn|anlst_givn|3d_desc',
        '# @Tstring|string|string|string|string|string|string'
        ]
    
    result = [GMT_VERSION]
    result.append(make_region_str(bbox))

    
