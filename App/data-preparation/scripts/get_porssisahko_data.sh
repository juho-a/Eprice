#!/bin/bash
# this script is used to get the data from the Porssisahko website

curl https://porssisahko.net/api/internal/excel-export --output ../data/porssisahko.xlsx

# checks if the file was downloaded successfully
if [ $? -ne 0 ]; then
    echo "Failed to download the file"
    exit 1
fi
