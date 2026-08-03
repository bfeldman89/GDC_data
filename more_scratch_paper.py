#!/usr/bin/env python
import glob
import os
import time

from pyairtable import Api

api = Api(os.environ['AIRTABLE_PAT'])
airtab = api.table(os.environ['GAGA_db'], 'GDC monthly reports')

# Check your current directory
print("the current directory is:", os.getcwd())
# Change to a new directory (relative path)
os.chdir('GDC_monthly_reports/csv/age_at_admission')
print("now we're in this directory:", os.getcwd())

def merge_csv_files(report):
    """Merge CSV files for a given report into a single file.

    Only files containing 'Age At Admission' or 'Not Reported' are appended,
    and those files are moved into an archive subdirectory afterward.
    """
    merged_file = f'{report}.csv'
    # Using '*' pattern to find all files starting with 'YYYY-MM-page-'
    this_list = glob.glob(f'{report}-page-*')
    # Sort the list of files to ensure they are in order
    this_list.sort()
    print(f"Found {len(this_list)} files to merge for report '{report}': {this_list}")
    time.sleep(.5)  # Sleep for .5 seconds before starting the merge
    with open(merged_file, "a", encoding='utf-8') as new_file_for_table:
        for this_file in this_list:
            archive_path = ''
            with open(this_file, 'r', encoding='utf-8') as f:
                this_file_content = f.read()
                # if the file contains "Age At Admission," then add the text to the new file
                if this_file_content.find('Age At Admission') != -1:
                    print(f"Adding {this_file} to {merged_file}")
                    new_file_for_table.write(this_file_content)
                    # after copying the text into the new file,
                    # send this file to the archive subdirectory
                    archive_path = f'archive/{this_file}'
                # if it didn't contain the phrase above, check for "Not Reported"
                # and if it contains this phease, add it to the new file
                elif this_file_content.find('Not Reported') != -1:
                    print(f"Adding {this_file} to {merged_file}")
                    new_file_for_table.write(this_file_content)
                    # after copying the text into the new file, move this file to the archive
                    archive_path = f'archive/{this_file}'
                else:
                    print(f"Skipping {this_file} bc doesn't contain either trigger phrase")
                time.sleep(.5)  # Sleep for .5 seconds before moving to the next file
            if archive_path:
                os.rename(this_file, archive_path)
            time.sleep(.5)  # Sleep for .5 seconds before moving to the next file



def simple_merge_csv_files(report, folder, report_type):
    """Merge CSV files for a given report into a single file.
    Only files containing 'Age At Admission' or 'Not Reported' are appended,
    and those files are moved into an archive subdirectory afterward.
    """
    os.chdir(f'{report_type}_reports/csv/{folder}')
    print("now we're in this directory:", os.getcwd())
    merged_file = f'{report}.csv'
    # Using '*' pattern to find all files starting with 'YYYY-MM-page-'
    this_list = glob.glob(f'{report}-page-*')
    # Sort the list of files to ensure they are in order
    this_list.sort()
    print(f"Found {len(this_list)} files to merge for report '{report}'")
    time.sleep(1)  # Sleep for 1 second before starting the merge
    with open(merged_file, "a", encoding='utf-8') as new_file_for_table:
        for this_file in this_list:
            archive_path = ''
            with open(this_file, 'r', encoding='utf-8') as f:
                this_file_content = f.read()
                print(f"Adding {this_file} to {merged_file}")
                new_file_for_table.write(this_file_content)
                # after copying the text into the new file,
                # send this file to the archive subdirectory
            archive_path = f'archive/{this_file}'
            os.rename(this_file, archive_path)
            time.sleep(1)  # Sleep for 1 second before moving to the next file


folders = ['age_at_admission',
'county_of_conviction',
'current_age',
'primary_offense_category',
'prison_sentence_in_years',
'race_group',
'years_served']

records = airtab.all(view='Grid 11', fields=['report'])
total_records = len(records)
for record in records:
    this_report = record['fields']['report']
    print(f"Processing report: {this_report}")
    for folder in folders:
        print(f"Processing folder: {folder}")
        simple_merge_csv_files(this_report, folder, 'annual')
        print(f"Finished processing folder: {folder}")
        os.chdir('../../..')  # Change back to the root directory after processing each folder
    print(f"Finished processing report: {this_report}")
    time.sleep(5)
    # merge_csv_files(this_report)
    # remaining_records = total_records - records.index(record) - 1
    # print(f"Remaining records to process: {remaining_records}")
