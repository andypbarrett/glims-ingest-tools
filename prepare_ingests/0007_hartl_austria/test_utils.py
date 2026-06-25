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
            '20260701', '20260421', '20250101', '20240902'
        ],
        'image_ID1': [
            '3722, 3822, 3823',
            'Salzburg: 3722, 3822, 3823 (many sheets) / Tirol: 3822-5000, 3822-5001',
            '382348',
            '4429',
            'A2023250_4522-5203_DOM',
            '3922-5000',
            '3823-5302, 3823-5303, 3822-5100,3822-5101',
            ]
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


image_target = [
    {
        'id': '1',
        'source': 'DEM Hillshade Province of Carinthia',
        'src_date': '20260701',
        'image_id': '3722',
        'geometry': Point(1, 2)
    },
    {
        'id': '1',
        'source': 'DEM Hillshade Province of Carinthia',
        'src_date': '20260701',
        'image_id': '3822',
        'geometry': Point(1, 2)
    },
    {
        'id': '1',
        'source': 'DEM Hillshade Province of Carinthia',
        'src_date': '20260701',
        'image_id': '3823',
        'geometry': Point(1, 2)
    },
    {
        'id': '2',
        'source': 'Orthoimagery Province of Salzburg',
        'src_date': '20260421',
        'image_id': '3722',
        'geometry': Point(3, 4)
    },
    {
        'id': '2',
        'source': 'Orthoimagery Province of Salzburg',
        'src_date': '20260421',
        'image_id': '3822',
        'geometry': Point(3, 4)
    },
    {
        'id': '2',
        'source': 'Orthoimagery Province of Salzburg',
        'src_date': '20260421',
        'image_id': '3823',
        'geometry': Point(3, 4)
    },
    {
        'id': '2',
        'source': 'Orthoimagery Province of Tyrol',
        'src_date': '20260421',
        'image_id': '3822-5000',
        'geometry': Point(3, 4)
    },
    {
        'id': '2',
        'source': 'Orthoimagery Province of Tyrol',
        'src_date': '20260421',
        'image_id': '3822-5001',
        'geometry': Point(3, 4)
    },,
    {
        'id': '3',
        'source': 'PlanetScope Orthoimagery',
        'src_date': '20250101',
        'image_id': '382348',
        'geometry': Point(5, 6)
    },
    {
        'id': '4',
        'source': 'Orthoimagery Federal Office of Metrology and Surveying - data.bev.gv.at',
        'src_date': '20260701',
        'image_id': '4429',
        'geometry': Point(7, 8)
    },
    {
        'id': '5',
        'source': 'Orthoimagery Province of Salzburg',
        'src_date': '20260421',
        'image_id': 'A2023250_4522-5203_DOM',
        'geometry': Point(-1, -2)
    },
    {
        'id': '6',
        'source': 'Orthoimagery Province of Carinthia',
        'src_date': '20250101',
        'image_id': '3922-5000',
        'geometry': Point(-3, -4)
    },
    {
        'id': '7',
        'source': 'UAV-borne photogrammetric survey by Geosphere Austria',
        'src_date': '20240902',
        'image_id': '3823-5302',
        'geometry': Point(-5, -6)
    },
    {
        'id': '7',
        'source': 'UAV-borne photogrammetric survey by Geosphere Austria',
        'src_date': '20240902',
        'image_id': '3823-5303',
        'geometry': Point(-5, -6)
    },
    {
        'id': '7',
        'source': 'UAV-borne photogrammetric survey by Geosphere Austria',
        'src_date': '20240902',
        'image_id': '3822-5100',
        'geometry': Point(-5, -6)
    },
    {
        'id': '7',
        'source': 'UAV-borne photogrammetric survey by Geosphere Austria',
        'src_date': '20240902',
        'image_id': '3822-5101',
        'geometry': Point(-5, -6)
    }
]


def test_get_image_from_geodataframe():
    result = utils.get_images_from_geodataframe(test_df)
    assert result == target
