#!/bin/bash

while getopts "d:v" opts; do
  case ${opts} in
    d) root_submission_dir="$OPTARG" ;; # $OPTARG grabs the value after -f
    v) verbose=true ;;   # Standard true/false switch
    *) echo "Invalid option" ;;
  esac
done

submitted_dir="$root_submission_dir/submitted"
preprocessed_dir="$root_submission_dir/preprocessed"
ingest_dir="$root_submission_dir/for_ingest"
script_dir="$root_submission_dir/scripts"

if [[ $verbose ]]; then
   echo "Creating $submitted_dir"
fi
mkdir -m 755 -p $submitted_dir
   
if [[ $verbose ]]; then
   echo "Creating $preprocessed_dir"
fi
mkdir -m 755 -p $preprocessed_dir

if [[ $verbose ]]; then
   echo "Creating $ingest_dir"
fi
mkdir -m 755 -p $ingest_dir

if [[ $verbose ]]; then
   echo "Creating $script_dir"
fi
mkdir -m 755 -p $script_dir
