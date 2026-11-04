"""Module to check shapefiles submitted for ingest.  Assumes that shapefiles 
are loaded into geopandas.GeoDataFrame.
"""
from pathlib import Path
import geopandas as gpd

FILE_TYPES = [
    '.zip',
    '.shp',
    '.json',
    '.geojson',
]

MAP_ATTRIBUTES = [
    'map_name',
    'auth_pub',
    'pub_date',
    'scale',
    ]

IMAGE_ATTRIBUTES = [
    'instr_name',
    'orig_id',
    'acq_time'
]


class Rule:
    """Base class for rule to check shapefile submission"""

    def __init__(self, condition: object, message: str):
        """
        Arguments:
          condition : condition to test could be lambda or function
          message : message to use for reporting
        """
        self.condition = condition
        self.message = message

    def check(self, obj: object):
        """Runs test on GeoDataFrame using condition"""
        self.result = self.condition(obj)

    def report(self) -> str:
        """Generate report"""
        return f"{self.message}: {'Pass' if self.result else 'Fail'}"

    @property
    def status(self) -> bool:
        """Returns test result as boolean"""
        return self.result


class IsAllowedFileType(Rule):
    """Checks that file is correct type"""
    def __init__(self):
        super().__init__(
            lambda obj: obj.suffix in FILE_TYPES,
            "Is a allowed file type"
            )


class HasLocalID(Rule):
    """Tests that GeoDataFrame has local_id attribute"""
    def __init__(self):
        super().__init__(
            lambda gdf: 'local_id' in gdf,
            "Has local_id as attribute"
        )


class HasAnalystName(Rule):
    """Test that GeoDataFrame has analyst_name attribute"""
    def __init__(self):
        super().__init__(
            lambda gdf: 'analyst_name' in gdf,
            "Has analyst_name as attribute"
            )


class HasImageAttributes(Rule):
    """Test that GeoDataFrame has image attributes:
       instr_name
       orig_id
       acq_time
    """
    def __init__(self):
        super().__init__(
            lambda gdf: all([a in gdf for a in IMAGE_ATTRIBUTES]),
            "Has image attributes"
            )


class HasMapAttributes(Rule):
    """Test that GeoDataFrame has map attributes:
       map_name
       auth_pub
       pub_date
       scale
    """
    def __init__(self):
        super().__init__(
            lambda gdf: all([a in gdf for a in MAP_ATTRIBUTES]),
            "Has map attributes"
            )


class HasCRS(Rule):
    """Tests that GeoDataFrame has *C*oordinate *R*eference *S*ystem"""
    def __init__(self):
        super().__init__(
            lambda gdf: gdf.crs,
            "Has CRS"
            )


def check_submission(outline_file: Path, json_file: Path, metadata_file: Path=None):
    """Checks submission to ensure files contain required information"""

    
