"""Tests prepare ingest functions"""
import datetime as dt

import geopandas as gpd
from shapely import Polygon, MultiPolygon

import prepare_ingest_files as prep

test_input_gpd = gpd.GeoDataFrame(
    {
        'id': {0: 1800900},
        'year': {0: 2023},
        'name': {0: 'Schwarzmilz Ferner'},
        'data_type': {0: 'aerial image'},
        'src_date': {0: '20230905'},
        'source': {0: '\nPortal Tirol\nLBA\n'},
        'image_ID1': {0: '40641'},
        'flightstr': {0: '0020'},
        'state': {0: 'Tyrol'},
        'region': {0: 'Allgaeuer_Alpen'},
        'url': {0: 'https://www.tirol.gv.at/statistik-budget/tiris/tiris-geodatendienste/'},
        'analyst': {0: 'M. Kaucher'},
        'img_qf': {0: 0.0},
        'outline_qf': {0: 0.0},
        'crevs': {0: 1.0},
        'debris': {0: 0.0},
        'comment': {0: 'outlines high certainity due to additionally used pictures (older images and DEM'},
        'data_type2': {0: 'hillshade2019'},
        'source_2': {0: ''},
        'src_date_2': {0: ''},
        'ROGI': {0: 0},
        'van_fragm': {0: None},
        'nr_frag': {0: 1},
        'median_elev': {0: 2429.0},
        'max_elev': {0: 2454.0},
        'min_elev': {0: 2409.0},
        'area': {0: 19941},
        },
    geometry=[
        Polygon(((0., 0.), (0., 1.), (1., 1.), (1., 0.), (0., 0.))),
        ],
    )


expected_types = {
    'local_id': ['str'],
    'name': ['str'],
    'src_date': ['str'],
    'area_m2': ['int64', 'float64'],
    'geometry': ['Polygon', 'MultiPolygon'],
    'source': ['str'],
    'loc_unc_y': ['float64'],
    'loc_unc_x': ['float64'],
    'glob_unc_y': ['float64'],
    'glob_unc_x': ['float64'],
    }


def test_make_shapefile_columns():
    """Tests that shapefile contains correct columns"""
    result = prep.make_glacier_shapefile(test_input_gpd)
    assert set(result.columns) == set(expected_types.keys())


def test_make_shapefile_types():
    """Tests that shapefile contains correct types"""
    result = prep.make_glacier_shapefile(test_input_gpd)
    for col in result.columns:
        if col == 'geometry':
            assert result['geometry'].geom_type.isin(expected_types['geometry']).all()
        else:
            assert result[col].dtype in expected_types[col]
