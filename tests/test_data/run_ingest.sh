#!/bin/bash

base='patagonia_falaschi_huber'
metadata='metadata_template.txt'
do_glims_ingest.py -m $metadata \
                    > $base.sql 2> $base.err

# Make KML from resulting SQL to visualize and check
echo "Making KML from $base.sql ..."
sql_to_kml.py $base.sql

#base='patagonia_falaschi_huber'
#metadata='metadata_template.txt'
#do_glims_ingest -m $metadata \
#                -v  \
#                -K  $base.kml   \
#                -p  $base.ps    \
#                > $base.sql 2> $base.err
#
# Try running without -I.  It should grab the instrument from the images shapefile.
#                -I  TM5    \
