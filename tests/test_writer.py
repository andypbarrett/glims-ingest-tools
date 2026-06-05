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
