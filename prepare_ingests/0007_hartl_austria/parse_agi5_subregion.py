"""Parses subregion.txt for Austra Glacier Inventory v5"""

import re
import json
from pathlib import Path

from classes import Analyst

DATAPATH = Path.home() / "Data" / "GLIMS" / "submissions" / "0007_hartl_austria" / "GI5_v2"

# Regex
start_of_region = re.compile(r"^\s+(\d{1,2})\. ([\w\s/-]+)$")
analyst_line = re.compile(r"^\s+analysts?:")
contact_line = re.compile(r"^\s+contacts?:")
institution_line = re.compile(r"^\s+institution:")


def parse_analyst(s: str) -> list:
    """Parse an analyst line and return list of analyst objects"""
    analysts = s.split(":")[1]
    analysts = [w.strip() for w in analysts.split(',')]  # Split into individual analyst
    analysts = [a.split('(')[0].strip() for a in analysts]  # remove affiliation
    return [Analyst(a.split()) for a in analysts]


def main():
    
    region_metadata = []

    with open(f"{DATAPATH}/submission/documentation/subregions.txt", "r") as f:
        for line in f:
            m = start_of_region.search(line)  # Start of metadata for region
            if m:
                # Get region number and name
                region_number, region_name = m.groups()

                # Get analysts
                line = f.readline()
                m = analyst_line.match(line)
                if m:
                    analysts = parse_analyst(line)
                else:
                    raise ValueError(f"Expected line with `analyst`: got {line}")

                # Get contact info
                line = f.readline()
                m = contact_line.match(line)
                if m:
                    contacts = line.split(':')[-1].strip().split(',')
                else:
                    raise ValueError(f"Expected line with `contact`: got {line}")

                # Get institution
                line = f.readline()
                m = institution_line.match(line)
                if m:
                    institutes = line.split(':')[-1].strip()
                else:
                    raise ValueError(f"Expected line with `institute`: got {line}")

                # create analyst object
                if len(analysts) != len(contacts):
                    contacts = contacts * len(analysts)  # Assumes contacts is either 1 or same as analysts
                analyst_list = []
                for analyst, contact in zip(analysts, contacts):
                    analyst_list.append(
                        {
                            "analyst": analyst.to_dict(),
                        }
                    )

                region_metadata.append(
                    {
                        "number": region_number,
                        "name": region_name.strip(),
                        "contact": contact,
                        "institute": institutes,
                        "analysts": analyst_list
                    }
                )

    with open(DATAPATH / "for_ingest" / "subregions.json", "w") as f:
        f.write(json.dumps(region_metadata, indent=4))


if __name__ == "__main__":
    main()
