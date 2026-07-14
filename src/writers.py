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
            f'\"{analyst_surname}\"|\"{analyst_given}\"|\"{description_3d}\"\n'
            f'{centroid[0]:.1f} {centroid[1]:.1f}')


def make_session_gmt(
        bbox: tuple,
        crs_wkt: str,
        regional_center: str,
        analysis_time: dt.datetime,
        data_source: str,
        process_description: str,
        analyst: list,
        description_3d: str,
        centroid: tuple,
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
      centroid : centroid of region

    Returns:
      formatted string object containing a session file
    """

    DATA_HEADER = [
        '# @Nrc_id|analy_time|data_src|proc_desc|anlst_surn|anlst_givn|3d_desc',
        '# @Tstring|string|string|string|string|string|string'
        ]

    result = [GMT_VERSION]
    result.append(make_region_str(bbox))
    result.append(make_crs_str(crs_wkt))
    result += DATA_HEADER
    result.append('# FEATURE_DATA')

    for analyst_surname, analyst_given in analyst:
        if len(analyst) > 1:
            result.append(">")
        result.append(
            make_feature_data_str(
                regional_center,
                analysis_time,
                data_source,
                process_description,
                analyst_surname,
                analyst_given,
                description_3d,
                centroid,
                )
            )

    return '\n'.join(result)


def make_image_feature_data(img: dict) -> str:
    """Creates a GMT format image data string

    Arguments:
      img : a dict of the format

        {
            "source_date": dt.datetime of source date of image,
            "instrument": short-name of instrument
            "image_id": original id for image
            "centroid": (lat, lon) centroid of image
        }

    Returns:
      string object formatted as GMT point feature data
    """
    required_keys = [
        "source_date",
        "instrument_short_name",
        "image_id",
        "centroid"
        ]
    if not any([key in img for key in required_keys]):
        raise KeyError(f"img must have keys {', '.join(required_keys)}, "
                       f" got {', '.join(img.keys())}")

    s = "# @D"
    s += img["source_date"].strftime('%Y-%m-%d')
    s += '|'
    s += img["instrument_short_name"]
    s += '|'
    s += img["image_id"] if img["image_id"] else 'unknown'
    s += '\n'
    s += f'{img["centroid"].x:.1f} {img["centroid"].y:.1f}'

    return s


def make_image_gmt(bbox: tuple, crs_wkt: str, image: list) -> str:
    """Makes image.gmt file string

    Arguments:
      bbox : bounding box of region
      crs_wkt : CRS in WKT format
      image : list of image data as dict.  Dict expected to contain source_date,
         instrument, image_id, and centroid of image as tuple (lat, lon)

    Returns:
      string object formated as image.gmt file
    """

    DATA_HEADER = [
        '# @Nacq_time|inst_name|orig_id',
        '# @Tstring|string|string'
    ]

    result = [GMT_VERSION]
    result.append(make_region_str(bbox))
    result.append(make_crs_str(crs_wkt))
    result += DATA_HEADER
    result.append('# FEATURE_DATA')

    for img in image:
        if len(image) > 1:
            result.append(">")
        result.append(make_image_feature_data(img))

    return '\n'.join(result)


def make_metadata():
    pass
