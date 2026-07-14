#!/bin/bash

# Prepares SQL for GLIMS ingest
# Expects metadata.txt, images.gmt, session.gmt and preprocessed_outlines are in directory

# Convert gmt files to Shapefiles
ogr2ogr -f 'ESRI Shapefile' session.shp session.gmt
ogr2ogr -f 'ESRI Shapefile' images.shp images.gmt

# Get existing GLIMS outlines from database
get_GLIMS_data.py -i preprocessed_outlines.shp

# Prepare outlines
ready_input_files.sh -i preprocessed_outlines.shp


