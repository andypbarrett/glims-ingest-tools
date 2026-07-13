"""Parses people.txt"""

import re
import datetime as dt
from collections import namedtuple
from pathlib import Path

from glims_ingest_tools.classes import Person, PEOPLE_FIELDS
from glims_ingest_tools.services import get_next_ids

Analyst = namedtuple("Person", ['surname', 'givennames', 'department',
                                'institute', 'postcode', 'city',
                                'country', 'email'])


country_code_lookup = {
    "Austria": "AT",
    }


def get_entry_parts(line):
    """Parses one line - only extracts strings in ''"""
    m = re.findall(r"'(.*?)'", line)
    if m:
        if len(m) == 2:
            contact, address = m
            email = ''
        elif len(m) == 3:
            contact, address, email = m
        else:
            raise ValueError(f"Unexpected number of fields returned, "
                             f"expected 2 or 3, got {len(m)}")
    return contact, address, email


def parse_contact(contact):
    """Parses contact into surname and given name"""
    surname, givennames = re.split(r', *', contact)
    return surname, givennames


def parse_address(address):
    """Parses address"""
#    parts = address.split(',')
    parts = re.split(r', *', address)
    if len(parts) == 2:
        department = ''
        institute = ''
        postcode, settlement = parts[0].split()
        country = parts[1]
    elif len(parts) == 3:
        department = ''
        institute = parts[0]
        postcode, settlement = parts[1].split()
        country = parts[2]
    else:
        department = parts[0]
        institute = parts[1]
        postcode, settlement = parts[2].split()
        country = parts[3]
    return department, institute, postcode, settlement, country


def parse_entry(line):
    """Parses entry in people.txt"""
    try:
        contact, address, email = get_entry_parts(line)
    except:
        print(line)

    try:
        surname, givennames = parse_contact(contact)
    except:
        print(contact)

    try:
        department, institute, postcode, settlement, country = parse_address(address)
    except:
        print(address)

#    return Analyst(surname, givennames, department, institute, postcode, settlement, country, email)
    return {
        'surname': surname,
        'givennames': givennames,
        'department': department,
        'affiliation': institute,
        'address1': department,
        'address2': institute,
        'postal_code': postcode,
        'city': settlement,
        'country_code': country_code_lookup.get(country, ''),
        'primary_email': email,
        }


def make_add_person_sql(people):
    """Create SQL to add new people"""
    lines = ""
    lines += "BEGIN;\n"
    lines += "INSERT INTO people\n"
    lines += f"  ({', '.join(PEOPLE_FIELDS)})\n"
    lines += "VALUES\n"
    lines += f"  {',\n  '.join([person.make_people_sql() for person in people])}"
    lines += ";\n"
    lines += "INSERT INTO rc_people\n"
    lines += "  (rc_id, contact_id, status)\n"
    lines += "VALUES\n"
    lines += f"  {',\n  '.join([person.make_rc_sql() for person in people])}"
    lines += ";\n"
    return lines


def parse_people(outfile: Path):

    people_path = Path.home() / "src" / "glims-ingest-tools" / "prepare_ingests" / "0007_hartl_austria" / "people.txt"

    new_contact_id = get_next_ids().contact_id
#    new_contact_id = 1067
    rc_id = 34

    with open(people_path, "r") as f:
        lines = f.readlines()

    people = []
    for line, contact_id in zip(lines, range(new_contact_id, new_contact_id+len(lines))):
        if line.strip().endswith('current'):
            continue
        person = Person(parse_entry(line))
        person.contact_id = contact_id
        person.rc_id = rc_id
        person.add_date = dt.date.today().isoformat()
        person.mod_date = dt.date.today().isoformat()

        people.append(person)

    with open(outfile, "w") as fo:
        fo.write(make_add_person_sql(people))


if __name__ == "__main__":
    outfile = Path("./prepare_ingests/0007_hartl_austria/add_people_agi.sql")

    parse_people(outfile)
