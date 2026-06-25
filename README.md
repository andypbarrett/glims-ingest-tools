# `glims-ingest-tools`

Tools for ingesting data into GLIMS Glacier Database

## File Structure For Ingest

Suggest creating a submission directory that has the format

`<issue_number>_<contact_surname>_<region>`

Within this directory have the following structure:

```
|--submitted-|
|            |--<submitted-vector-file>
|            |--submission-form.json
|
|--preprocessed-|
|               |--session.gmt
|               |--images.gmt
|               |--glaciers.shp
|               |--metadata.txt
|
|--scripts
|
|--for_ingest
```

Where `submitted` contains all of the original files, `preprocessed` contains any

For now create these using the following bash script.  We could also use cookiecutter

```
!#/bash

mkdir -m 755 -p <submission-directory>/submitted
mkdir -m 755 -p <submission-directory>/preprocessed
mkdir -m 755 -p <submission-directory>/for_ingest
```

## Copying processed files


