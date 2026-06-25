"""Classes to parse data"""
import re
import json
import datetime as dt

from pathlib import Path

from glims_ingest_tools.sql import sqlize_value


METADATA_FIELDS = [
    "rc_id",
    "region_label",
    "contact_id",
    "file_name",
    "file_size",
    "submission_time",
    "geocoding_with_image",
    "georegistration_gpcs",
    "orthorectification_dem_dtm",
    "dn_radiance_conversion",
    "sun_elev_correction",
    "image_radiometric_correction",
    "model_radiometric_correction",
    "anisotropic_reflectance",
    "slope_aspect_correction",
    "band_ratio_linear_trans",
    "spatial_filtering",
    "geomorphological_analysis",
    "texture_analysis",
    "manual_digitization",
    "percent_manual_editing",
    "supervised_classification",
    "supervised_title",
    "unsupervised_classification",
    "unsupervised_title",
    "process_description",
    "embargo_period",
    "analysis_tools",
    "analysis_tools_other",
    ]


PEOPLE_FIELDS = [
        'contact_id',
        'surname',
        'givennames',
        'prof_title',
        'affiliation',
        'department',
        'address1',
        'address2',
        'city',
        'state_province',
        'postal_code',
        'country_code',
        'office_loc',
        'url_primary',
        'url_additional',
        'workphone_primary',
        'workphone_additional',
        'workfax',
        'homephone',
        'mobilephone',
        'email_primary',
        'email_additional',
        'prof_interest',
        'glims_role',
        'affiliation_points',
        'principal_flag',
        'comment',
        'status'
]


class RegionalCenter():

    def __init__(self, rc_id: str,
                 name: str, region: str, contact: Analyst) -> RegionalCenter:
        self.rc_id = rc_id
        self.name = name
        self.region = region
        self.contact = contact


class Steward():

    def __init__(self, ):
        pass


class Analyst():

    def __init__(self, args, institution=None, email=None):
        first, *middle, last = args
        self.first_name = first
        self.middle_name = ' '.join(middle)
        self.surname = last
        self.institution = institution
        self.email = email

    def __str__(self):
        """If print called, returns string with fullname"""
        return ' '.join([s for s in self.__dict__.values() if s != ''])

    def __repr__(self):
        return f"Analyst(first_name={self.first_name!r}, middle_name={self.middle_name!r}, surname={self.surname!r})"
        
    @property
    def full_name(self, initials=False) -> str:
        """Returns full name

        Arguments:
          initials : use initals of first and middle names instead.  Default false.

        Returns:
          String containing full name
        """
        return ' '.join([s for s in self.__dict__.values() if s != ''])

    def compare_with(self, other: Analyst) -> bool:
        """Compares analyst name based on surname and first_name or first initials"""
        if self.surname == other.surname:
            if (self.first_name == other.first_name) or (self.first_name[0] == other.first_name[0]):
                return True
        else:
            return False

    def to_dict(self, fields=['first_name','middle_name','surname']):
        return {k: self.__dict__[k] for k in fields}
        
    @classmethod
    def from_string(cls, fullname):
        """Creates analyst from string containing full name"""
        parts = fullname.split()
        return cls(parts)


class NewSubmission():
    """Class to hold new submission"""

    def __init__(self, attributes: dict={}):

        required_fields = [
            "rc_id",
            "region_label",
            "contact_id",
            "file_name",
            ]
    
        if not attributes:
            raise ValueError("Expects dictionary containing at least: "
                             f"{','.join(required_fields)}")
        is_required = [field in attributes for field in required_fields]
        if not all(is_required):
            raise KeyError("Expects dictionary containing at least: "
                           f"{', '.join(required_fields)}. "
                           f"Missing: {', '.join([f for f, b in zip(required_fields, is_required) if not b])}")

        # Should booleans also have a None?
        
        self.rc_id = attributes.get("rc_id", "")
        self.region_label = attributes.get("region_label", "")
        self.contact_id = attributes.get("contact_id", "")
        self.file_name = attributes.get("file_name", "")
        self.file_size = attributes.get("file_size", 0)
        self.submission_time = attributes.get("submission_time", "") # parse to datetime
        self.geocoding_with_image = attributes.get("geocoding_with_image", False)
        self.georegistration_gpcs = attributes.get("georegistration_gpcs", False)
        self.orthorectification_dem_dtm = attributes.get("orthorectification_dem_dtm", False)
        self.dn_radiance_conversion = attributes.get("dn_radiance_conversion", False)
        self.sun_elev_correction = attributes.get("sun_elev_correction", False)
        self.image_radiometric_correction = attributes.get("image_radiometric_correction", False)
        self.model_radiometric_correction = attributes.get("model_radiometric_correction", False)
        self.anisotropic_reflectance = attributes.get("anisotropic_reflectance", False)
        self.slope_aspect_correction = attributes.get("slope_aspect_correction", False)
        self.band_ratio_linear_trans = attributes.get("band_ratio_linear_trans", False)
        self.spatial_filtering = attributes.get("spatial_filtering", False)
        self.geomorphological_analysis = attributes.get("geomorphological_analysis", False)
        self.texture_analysis = attributes.get("texture_analysis", False)
        self.manual_digitization = attributes.get("manual_digitization", True)
        self.percent_manual_editing = attributes.get("percent_manual_editing", 100)
        self.supervised_classification = attributes.get("supervised_classification", False)
        self.supervised_title = attributes.get("supervised_title", "")
        self.unsupervised_classification = attributes.get("unsupervised_classification", False)
        self.unsupervised_title = attributes.get("unsupervised_title", "")
        self.process_description = attributes.get("process_description", "")
        self.embargo_period = attributes.get("embargo_period", 0)
        self.analysis_tools = attributes.get("analysis_tools", "")
        self.analysis_tools_other = attributes.get("analysis_tools_other", "")


    def __str__(self):
        return '\n'.join([f"{k}: {v!r}" for k, v in self.__dict__.items()])

    def __repr__(self):
        return f"NewSubmission({','.join([f'{k!r}: {v!r}' for k, v in self.__dict__.items()])})"

    def print_metadata_file(self):
        s = []
        for k, v in self.__dict__.items():
            if k not in METADATA_FIELDS:
                continue
            if isinstance(v, bool):
                if v:
                    s.append(f"{k}= yes")
                else:
                    s.append(f"{k}= no")
            elif isinstance(v, dt.datetime):
                s.append(f"{k}= {v.strftime('%Y%m%d_%h%M%s')}")
            else:
                if (k == "embargo_period") and (v == 0):
                    s.append(f"{k}= None")
                else:
                    s.append(f"{k}= {v}")
        print('\n'.join(s))

    def write_metadata_file(self, fp: Path):
        """Create metadata.txt"""
        s = []
        for k, v in self.__dict__.items():
            if k not in METADATA_FIELDS:
                continue
            if isinstance(v, bool):
                if v:
                    s.append(f"{k}= yes")
                else:
                    s.append(f"{k}= no")
            elif isinstance(v, dt.datetime):
                s.append(f"{k}= {v.strftime('%Y%m%d_%h%M%s')}")
            else:
                if (k == "embargo_period") and (v == 0):
                    s.append(f"{k}= None")
                else:
                    s.append(f"{k}= {v}")
        with open(fp, "w") as f:
            f.write("\n".join(s))
        return

    def set_submission_time(self, submission_time: str):
        """Sets submission_time

        Arguments:
          submission_time: time of submission (YYYYMMDD_HHMMSS)

        Returns:
          Updates submission time
        """
        if not re.match(r"\d{8}_\d{6}", submission_time):
            raise ValueError(f"Expects submission_time as YYYYMMDD_HHMMSS, "
                             f"got {submission_time}")
        self.submission_time = dt.datetime.strptime(submission_time,
                                                    "%Y%m%d_%h%M%s")

    @classmethod
    def from_json(cls, fp: Path):
        with open(fp, "r") as f:
            attributes = json.load(f)
        return cls(attributes)


class Person():
    """Class to hold GLIMS DB people table data"""

    def __init__(self, params: dict):
        """Instantiate Person

        Arguments:
          params: dictionary containing at least `surname` and `given_names`
            for person.

        Parameters
          Required:
            surname : family name of Person
            givennames : first name and middle names of Person

          Additional:
            prof_title : e.g. Professor, Dr
            affiliation : University or organization
            department : e.g. institute, department, center within main affiliated organization
            address1 : first component of address, often same as `department`
            address2 : second component of address, often affiliated organization
            city : city or town of affiliated organization or department
            state_province : name or state, province or region within country
            postal_code : postal code
            country_code : two letter country code (ISO 3166-1 alpha-2)
            office_loc : office number or location code
            url_primary : URL of primary web page
            url_additional : URL of any additional web page
            workphone_primary : primary work phone
            workphone_additional : additional work phone
            workfax : fax number
            homephone : home phone number
            mobilephone : mobile phone number
            email_primary : primary email
            email_additional : secondary email
            prof_interest : area of expertise or professional interest; e.g. mountain glaciers
            glims_role : role within GLIMS
            affiliation_points : "lat/lon" for location of affiliated organization in WGS84 (EPSG:4326)
            principal_flag : principal member of GLIMS
            comment : additional comments
            status : status (Active=1, Innactive=2, Removed from GLIMS=3, Retired=4, Deceased=5)

            rc_id : ID of Regional Center
        """

        required_fields = ['surname', 'givennames']
        if any([field not in params for field in required_fields]):
            raise KeyError(f"`params` must contain {', '.join(required_fields)}")

        self.contact_id = params.get('contact_id', None)
        self.surname = params.get('surname', '')
        self.givennames = params.get('givennames', '')
        self.prof_title = params.get('prof_title', '')
        self.affiliation = params.get('affiliation', '')
        self.department = params.get('department', '')
        self.address1 = params.get('address1', '')
        self.address2 = params.get('address2', '')
        self.city = params.get('city', '')
        self.state_province = params.get('state_province', '')
        self.postal_code = params.get('postal_code', '')
        self.country_code = params.get('country_code', '')
        self.office_loc = params.get('office_loc', '')
        self.url_primary = params.get('url_primary', '')
        self.url_additional = params.get('url_additional', '')
        self.workphone_primary = params.get('workphone_primary', '')
        self.workphone_additional = params.get('workphone_additional', '')
        self.workfax = params.get('workfax', '')
        self.homephone = params.get('homephone', '')
        self.mobilephone = params.get('mobilephone', '')
        self.email_primary = params.get('email_primary', '')
        self.email_additional = params.get('email_additional', '')
        self.prof_interest = params.get('prof_interest', '')
        self.glims_role = params.get('glims_role', '')
        self.affiliation_points = params.get('affiliation_points', '')  # should be shapely Point
        self.principal_flag = params.get('principal_flag', False)
        self.comment = params.get('comment', '')
        self.status = params.get('status', 1)

        self.rc_id = params.get('rc_id', '')


# Figure out what to do about add date
#        'add_date': (None, dt.date.today().isoformat()),
#        'mod_date': (None, dt.date.today().isoformat()),

    def __str__(self):
        s = ''.join([f"{k}: {v}\n" for k, v in self.__dict__.items()])
        return s

    def __repr__(self):
        return (f"<Person(contact_id={self.contact_id}, "
                f"surname={self.surname}, "
                f"given_names={self.givennames})>")

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, "r") as f:
            return cls(json.load(f))

    def make_people_sql(self):
        """Create SQL line for people"""
#        s = ('INSERT INTO people (' +
#             ','.join(self.__dict__.keys()) +
#             ') VALUES (' +
#             ','.join([sqlize_value(v) for v in self.__dict__.values()]) +
#             ');')
#        s = f"({','.join([sqlize_value(v) for v in self.__dict__.values()])})"
        s = f"({','.join([sqlize_value(getattr(self, field)) for field in PEOPLE_FIELDS])})"
        return s

    def make_rc_sql(self):
        s = f"({','.join([sqlize_value(self.rc_id), sqlize_value(self.contact_id), '1'])})"
        return s


class Address():

    def __init__(self, **kwargs):
        """Initialize Address object

        Expects kwargs to contain one or more of:

        house: The name or identifier of the building or residence.
        house_number: The specific number assigned to the building on a street.
        road: The name of the street or road.
        settlement_part: A subdivision within a town or city, like a neighborhood or borough.
        settlement: The town, city, or village where the address is located.
        postcode: A postalcode (ZIP code) (numeric, alphanumeric, or otherwise) used for sorting and delivering mail.
        region_part: A smaller administrative area within a larger region, such as a county or district.
        region: A larger administrative area, like a state, province, or region.
        country: The country in which the address is located, crucial for international mail.

        https://www.geoapify.com/address-formats-by-country-json/#address-compoments
        """

        self.department = kwargs.get('department', '')
        self.institution = params.get('institution', '')
        self.house = kwargs.get('house', '')
        self.house_number = kwargs.get('house_number', '')
        self.road = kwargs.get('road', '')
        self.settlement_part = kwargs.get('settlement_part', '')
        self.settlement = kwargs.get('settlement', '')
        self.postcode = kwargs.get('postcode', '')
        self.region_part = kwargs.get('region_part', '')
        self.region = kwargs.get('region', '')
        self.country = kwargs.get('country', '')

    def __str__(self):
        return '\n'.join([f'{k}: {v}' for k, v in self.__dict__.items() if v != ''])

    def __repr__(self):
        attrs = ', '.join([f'{k}={v}' for k, v in self.__dict__.items() if v != ''])
        return f"<Address({attrs})>"

    def strformat(self, fmt: str=None) -> str:
        """Returns an address string formatted using fmt

        Arguments:
          fmt : format string for address.  If fmt is None, the default format is returned.

                fmt = "[house]\n[road] [house_number]\n[postcode] [settlement]\n[country]"

        Returns:
          formatted address string
        """
        pass

    @classmethod
    def strparse(cls, address_str, fmt):
        """Parses address string using fmt"""

        pass
