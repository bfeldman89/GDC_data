#!/usr/bin/env python
import glob
import os
import time

# Check your current directory
print("Before:", os.getcwd())

# Change to a new directory (relative path)
os.chdir('GDC_monthly_reports/csv/age_at_admission')
print("After:", os.getcwd())

# Using '*' pattern to find all files starting with '2005-09-page-'
this_list = glob.glob('2005-09-page-*')
# Sort the list of files to ensure they are in order
this_list.sort()
with open('2005-09.csv', "a", encoding='utf-8') as new_file_for_table:
    for this_file in this_list:
        archive_path = ''
        print(this_file)
        with open(this_file, 'r', encoding='utf-8') as f:
            # first_line = f.readline()
            # print(f"First line of {this_file}: {first_line.strip()}")
            this_file_content = f.read()
            if this_file_content.find('Age At Admission') != -1:
                print(f"Adding {this_file} to 2005-09.csv")
                new_file_for_table.write(this_file_content)
                archive_path = f'archive/{this_file}'
            elif this_file_content.find('Not Reported') != -1:
                print(f"Adding {this_file} to 2005-09.csv")
                new_file_for_table.write(this_file_content)
                archive_path = f'archive/{this_file}'
            else:
                print(f"Skipping {this_file} bc doesn't contain 'Age At Admission' or 'Not Reported'")
        if archive_path:
            os.rename(this_file, archive_path)
        time.sleep(1)
