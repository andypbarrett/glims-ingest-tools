import datetime as dt

import geopandas as gpd

from shapely.geometry import Point

import utils


# Test GeoDataFrame
test_df = gpd.GeoDataFrame(
    {
        'id': ['1', '2', '3', '4', '5', '6', '7'],
        'source': [
            'DEM Hillshade Province of Carinthia',
            'Orthoimagery Province of Tyrol',
            'PlanetScope Orthoimagery',
            'Orthoimagery Federal Office of Metrology and Surveying - data.bev.gv.at',
            'Orthoimagery Province of Salzburg',
            'Orthoimagery Province of Carinthia',
            'UAV-borne photogrammetric survey by Geosphere Austria'
        ],
        'source2': [
            None,
            'Orthoimagery Province of Salzburg',
            None,
            None,
            None,
            None,
            None,
        ],
        'src_date': [
            '20260701', '20260421', '20250101',
            '20260701', '20260421', '20250101', '20240902',
        ],
        'image_ID1': [
            '3722, 3822, 3823',
            'Salzburg: 3722, 3822, 3823 (many sheets) / Tirol: 3822-5000, 3822-5001',
            '382348',
            '4429',
            'A2023250_4522-5203_DOM',
            '3922-5000',
            '3823-5302, 3823-5303, 3822-5100,3822-5101',
            ],
        'geometry': [
            Point(1,2),
            Point(3,4),
            Point(5,6),
            Point(7,8),
            Point(-1,-2),
            Point(-3,-4),
            Point(-5,-6),
        ],
    }
)


target = [
    {
        'local_id': '1',
        'instrument': 'DEM Hillshade Province of Carinthia',
        'instrument_short_name': 'CarinthDEM',
        'source_date': dt.datetime(2026, 7, 1),
        'image_id': '3722',
        'centroid': Point(1, 2)
    },
    {
        'local_id': '1',
        'instrument': 'DEM Hillshade Province of Carinthia',
        'instrument_short_name': 'CarinthDEM',
        'source_date': dt.datetime(2026, 7, 1),
        'image_id': '3822',
        'centroid': Point(1, 2)
    },
    {
        'local_id': '1',
        'instrument': 'DEM Hillshade Province of Carinthia',
        'instrument_short_name': 'CarinthDEM',
        'source_date': dt.datetime(2026, 7, 1),
        'image_id': '3823',
        'centroid': Point(1, 2)
    },
    {
        'local_id': '2',
        'instrument': 'Orthoimagery Province of Salzburg',
        'instrument_short_name': 'Aerial22',
        'source_date': dt.datetime(2026, 4, 21),
        'image_id': '3722',
        'centroid': Point(3, 4)
    },
    {
        'local_id': '2',
        'instrument': 'Orthoimagery Province of Salzburg',
        'instrument_short_name': 'Aerial22',
        'source_date': dt.datetime(2026, 4, 21),
        'image_id': '3822',
        'centroid': Point(3, 4)
    },
    {
        'local_id': '2',
        'instrument': 'Orthoimagery Province of Salzburg',
        'instrument_short_name': 'Aerial22',
        'source_date': dt.datetime(2026, 4, 21),
        'image_id': '3823',
        'centroid': Point(3, 4)
    },
    {
        'local_id': '2',
        'instrument': 'Orthoimagery Province of Tyrol',
        'instrument_short_name': 'Aerial20',
        'source_date': dt.datetime(2026, 4, 21),
        'image_id': '3822-5000',
        'centroid': Point(3, 4)
    },
    {
        'local_id': '2',
        'instrument': 'Orthoimagery Province of Tyrol',
        'instrument_short_name': 'Aerial20',
        'source_date': dt.datetime(2026, 4, 21),
        'image_id': '3822-5001',
        'centroid': Point(3, 4)
    },
    {
        'local_id': '3',
        'instrument': 'PlanetScope Orthoimagery',
        'instrument_short_name': 'SuperDove',
        'source_date': dt.datetime(2025, 1, 1),
        'image_id': '382348',
        'centroid': Point(5, 6)
    },
    {
        'local_id': '4',
        'instrument': 'Orthoimagery Federal Office of Metrology and Surveying - data.bev.gv.at',
        'instrument_short_name': 'Aerial24',
        'source_date': dt.datetime(2026, 7, 1),
        'image_id': '4429',
        'centroid': Point(7, 8)
    },
    {
        'local_id': '5',
        'instrument': 'Orthoimagery Province of Salzburg',
        'instrument_short_name': 'Aerial22',
        'source_date': dt.datetime(2026, 4, 21),
        'image_id': 'A2023250_4522-5203_DOM',
        'centroid': Point(-1, -2)
    },
    {
        'local_id': '6',
        'instrument': 'Orthoimagery Province of Carinthia',
        'instrument_short_name': 'Aerial21',
        'source_date': dt.datetime(2025, 1, 1),
        'image_id': '3922-5000',
        'centroid': Point(-3, -4)
    },
    {
        'local_id': '7',
        'instrument': 'UAV-borne photogrammetric survey by Geosphere Austria',
        'instrument_short_name': 'GeosphUAV',
        'source_date': dt.datetime(2024, 9, 2),
        'image_id': '3823-5302',
        'centroid': Point(-5, -6)
    },
    {
        'local_id': '7',
        'instrument': 'UAV-borne photogrammetric survey by Geosphere Austria',
        'instrument_short_name': 'GeosphUAV',
        'source_date': dt.datetime(2024, 9, 2),
        'image_id': '3823-5303',
        'centroid': Point(-5, -6)
    },
    {
        'local_id': '7',
        'instrument': 'UAV-borne photogrammetric survey by Geosphere Austria',
        'instrument_short_name': 'GeosphUAV',
        'source_date': dt.datetime(2024, 9, 2),
        'image_id': '3822-5100',
        'centroid': Point(-5, -6)
    },
    {
        'local_id': '7',
        'instrument': 'UAV-borne photogrammetric survey by Geosphere Austria',
        'instrument_short_name': 'GeosphUAV',
        'source_date': dt.datetime(2024, 9, 2),
        'image_id': '3822-5101',
        'centroid': Point(-5, -6)
    }
]


def test_get_image_from_geodataframe():
    result = utils.get_images_from_geodataframe(test_df)
    assert result == target
