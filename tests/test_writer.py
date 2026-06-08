"""Test functions for writer.py"""
import datetime as dt

import glims_ingest_tools.writers as writers


def test_make_region_str():
    bbox = (-123.7742, -123.1238, 47.5231, 47.9104)
    target = '# @R-123.7742/-123.1238/47.5231/47.9104'
    assert writers.make_region_str(bbox) == target


def test_make_crs_wkt_str():
    crs_wkt = '"GEOGCS[\"GCS_WGS_1984\",DATUM[\"WGS_1984\",SPHEROID[\"WGS_84\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"'
    target = '# @Jw"GEOGCS[\"GCS_WGS_1984\",DATUM[\"WGS_1984\",SPHEROID[\"WGS_84\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"'
    assert writers.make_crs_str(crs_wkt) == target


def test_make_feature_data_str():
    regional_center = '507'
    analysis_time = dt.datetime(2017, 10, 24)
    data_source = 'NAIP imagery and LiDAR data'
    process_description = 'Manual digitization'
    analyst_surname = 'Mozer'
    analyst_given = 'Max'
    description_3d = ''
    centroid = (-123.4, 47.6)

    target = '''# @D507|2017-10-24|"NAIP imagery and LiDAR data"|"Manual digitization"|Mozer|Max|""
-123.4 47.6'''
    result = writers.make_feature_data_str(
        regional_center,
        analysis_time,
        data_source,
        process_description,
        analyst_surname,
        analyst_given,
        description_3d,
        centroid,
        )
    print(result)

    assert result == target


def test_make_session_gmt():

    target = """# @VGMT1.0 @GPOINT
# @R-123.7742/-123.1238/47.5231/47.9104
# @Jw"GEOGCS[\"GCS_WGS_1984\",DATUM[\"WGS_1984\",SPHEROID[\"WGS_84\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"
# @Nrc_id|analy_time|data_src|proc_desc|anlst_surn|anlst_givn|3d_desc
# @Tstring|string|string|string|string|string|string
# FEATURE_DATA
>
# @D507|2017-10-24|"NAIP imagery and LiDAR data"|"Manual digitization"|Mozer|Max|""
-123.4 47.6
>
# @D507|2017-10-24|"NAIP imagery and LiDAR data"|"Manual digitization"|Pflug|Justin|""
-123.4 47.6"""

    bbox = (-123.7742, -123.1238, 47.5231, 47.9104)
    crs_wkt = '"GEOGCS[\"GCS_WGS_1984\",DATUM[\"WGS_1984\",SPHEROID[\"WGS_84\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"'
    regional_center = '507'
    analysis_time = dt.datetime(2017, 10, 24)
    data_source = 'NAIP imagery and LiDAR data'
    process_description = 'Manual digitization'
    analyst = [('Mozer', 'Max'), ('Pflug', 'Justin')]
    description_3d = ''
    centroid = (-123.4, 47.6)

    result = writers.make_session_gmt(
        bbox,
        crs_wkt,
        regional_center,
        analysis_time,
        data_source,
        process_description,
        analyst,
        description_3d,
        centroid,
        )

    assert result == target


def test_make_image_gmt():

# # @Jw"GEOGCS[\"GCS_WGS_1984\",DATUM[\"WGS_1984\",SPHEROID[\"WGS_84\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.017453292519943295]]"

    target = """# @VGMT1.0 @GPOINT
# @R-123.7742/-123.1238/47.5231/47.9104
# @Jw"GEOGCS[\"GCS_WGS_1984\",DATUM[\"WGS_1984\",SPHEROID[\"WGS_84\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"
# @Nacq_time|inst_name|orig_id
# @Tstring|string|string
# FEATURE_DATA
# @D2015-08-01|naip2015|unknown
-123.4 47.6"""

    bbox = (-123.7742, -123.1238, 47.5231, 47.9104)
    crs_wkt = '"GEOGCS[\"GCS_WGS_1984\",DATUM[\"WGS_1984\",SPHEROID[\"WGS_84\",6378137.0,298.257223563]],PRIMEM[\"Greenwich\",0.0],UNIT[\"Degree\",0.0174532925199433]]"'
    image = [
        {
            "source_date": dt.datetime(2015, 8, 1),
            "instrument": "naip2015",
            "image_id": None,
            "centroid": (47.6, -123.4),
            }
        ]

    result = writers.make_image_gmt(
        bbox,
        crs_wkt,
        image,
        )

    assert result == target


def test_make_image_feature_data():

    target = """# @D2015-08-01|naip2015|unknown
-123.4 47.6"""

    img = {
        "source_date": dt.datetime(2015, 8, 1),
        "instrument": "naip2015",
        "image_id": None,
        "centroid": (47.6, -123.4),
        }

    result = writers.make_image_feature_data(img)

    assert result == target
