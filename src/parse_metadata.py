"""Parses metadata.json into a metadata_template.txt format"""
from pathlib import Path
import json


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


