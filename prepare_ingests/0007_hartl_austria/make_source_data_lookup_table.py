"""Script creates a lookup table used to homogenize source data names in AGI5 shapefiles"""

import re
import json

from config import DATAPATH

FILEPATH = DATAPATH / "submission" / "documentation" / "geojson_abbreviations_LH.fixed.txt"


def main():

    source_lookup = {}

    with open(FILEPATH, "r") as f:
        for line in f.readlines():
            if re.search(r"\w+ = \w+", line):
                key, value = line.split("=")
                if key in source_lookup:
                    if source_lookup[key] != value:
                        raise ValueError(f"Duplicate Key with different value: "
                                         f"original value for {key} is "
                                         f"{source_lookup[key]}, got {value}")
                source_lookup[key.strip()] = value.strip()

#    source_lookup["Planet Labs"] = "PlanetScope"

    with open('geojson_abbreviations_lookup.json', 'w') as f:
        json.dump(source_lookup, f, indent=4)


if __name__ == "__main__":
    main()
