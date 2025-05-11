#!/bin/bash

curl https://porssisahko.net/api/internal/excel-export --output ../data/porssisahko.xlsx

# checks if the file was downloaded successfully
if [ $? -ne 0 ]; then
    echo "Failed to download the file"
    exit 1
fi

input_file="../data/porssisahko.xlsx"

# check if input file exists
if [ ! -f "$input_file" ]; then
    echo "Input file not found!"
    exit 1
fi

# use ssconvert to convert the file to csv format in temp_file.csv
ssconvert "$input_file" temp_file.csv

# output filename is same as input file with .csv extension
output_file="${input_file%.*}.csv"

# remove first 3 rows from temp_file.csv
sed -i '1,3d' temp_file.csv

# save the modified file as output_file
mv temp_file.csv "$output_file"

# remove the temporary file
rm -f temp_file.csv # (comment for debugging)
# print success message
echo "File converted and saved as $output_file"

# run python script to process the csv file
python clean_porssisahko.py "$output_file"
# the new name has "_cleaned.csv" appended to the original name
rm -f "$output_file" # (comment for debugging)
# rename the cleaned file
mv "${output_file%.csv}_cleaned.csv" "$output_file"

# run the populate_porssisahko.py script
python populate_porssisahko.py "$output_file"
# print success message
echo "File populated and saved as $output_file"
# remove the original file
#rm -f "$input_file" # (comment for debugging)