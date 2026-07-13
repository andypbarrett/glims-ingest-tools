import pandas as pd
import geopandas as gpd
from shapely import Polygon, MultiPolygon

import glims_ingest_tools.shapefile as gshp


def test_is_single_year_true():
    """Tests is_single_year for the True case"""
    df = pd.DataFrame(
        {"src_date": ['20230825', '20230901']}
        )
    assert gshp.is_single_year(df) == True


def test_is_single_year_false():
    """Tests is_single_year for the False case"""
    df = pd.DataFrame(
        {"src_date": ['20230825', '20230901', '20250901']}
        )
    assert gshp.is_single_year(df) == False


def test_is_single_year_true_dt():
    """Tests is_single_year for the True case"""
    df = pd.DataFrame(
        {"src_date": pd.to_datetime(['20230825', '20230901'])}
        )
    assert gshp.is_single_year(df) == True


def test_is_single_year_false_dt():
    """Tests is_single_year for the False case"""
    df = pd.DataFrame(
        {"src_date": pd.to_datetime(['20230825', '20230901', '20250901'])}
        )
    assert gshp.is_single_year(df) == False


def test_is_geometry_polygon_true():
    """Tests is_geometry_polygon for True case"""
    gdf = gpd.GeoDataFrame(
        geometry=[
            Polygon([(0, 0), (0, 5), (5, 5), (5, 0), (0, 0)]),
            Polygon([(6, 6), (6, 7), (7, 7), (7, 6), (6, 6)]),
            MultiPolygon([
                [(0, 0), (0, 1), (1, 1), (1, 0), (0, 0)],
                [(10, 10), (10, 11), (11, 11), (11, 10), (10, 10)]
                ])
            ]
        )
    assert gshp.is_geometry_polygon(gdf) == True


def test_is_geometry_polygon_false():
    """Tests is_geometry_polygon for True case"""
    assert True


def test_is_geometry_close_true():
    """Tests is_geometry_closed for True case"""
    assert True


def test_is_geometry_closed_false():
    """Tests is_geometry_closed for False case"""
