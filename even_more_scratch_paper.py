#!/usr/bin/env python
import glob
import os
import time

import requests

from pyairtable import Api
from documentcloud import DocumentCloud

api = Api(os.environ['AIRTABLE_PAT'])
airtab = api.table(os.environ['GAGA_db'], 'GDC monthly reports')
airtab2 = api.table(os.environ['GAGA_db'], 'reports')

dc = DocumentCloud(os.environ['MUCKROCK_USERNAME'], os.environ['MUCKROCK_PW'])

def merge_csv_files_variation(folder):
    # I used this vatiation for several folders (see lines 71-73)
    os.chdir(f'../{folder}')
    records = airtab.all(view=folder, fields=['report'])
    total_records = len(records)
    for record in records:
        report = record['fields']['report']
        print(f"Processing report: {report}")
        # doing this instead of merging method
        this_list = glob.glob(f'{report}-page-*')
        this_list.sort()
        print(f"Found {len(this_list)} files to merge for report '{report}': {this_list}")
        time.sleep(1)  # Sleep for .5 seconds before starting the merge
        if len(this_list) == 3:
            merged_file = f'{report}.csv'
            f1 = this_list[0]
            f2 = this_list[1]
            with open(merged_file, "a", encoding='utf-8') as outfile:
                with open(f1, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                time.sleep(.5)
                os.rename(f1, f'archive/{f1}')
                with open(f2, 'r', encoding='utf-8') as infile2:
                    outfile.write(infile2.read())
                time.sleep(.5)
                os.rename(f2, f'archive/{f2}')
        else:
            print(f"Skipping report '{report}' because it does not have 3 files in this directory.")
        # keeping these two lines to print the countdown tho :)
        remaining_records = total_records - records.index(record) - 1
        print(f"Remaining records to process: {remaining_records}")

merge_csv_files_variation('primary_offense_category')
merge_csv_files_variation('years_served')
merge_csv_files_variation('prison_sentence_in_years')

def rename_csv_of_first_table_on_first_page():
    # this variation might be preferable to making copies and archives
    # this example was used in the `race_group` folder
    os.chdir('../race_group')
    records = airtab.all(view='race_group', fields=['report', 'race_page_no'])
    for record in records:
        report = record['fields']['report']
        print(f"Processing report: {report}")
        pg_no = record['fields']['race_page_no']
        old_file_name = f"{report}-page-{pg_no}-table-1.csv"
        new_file_name = f"{report}.csv"
        os.rename(old_file_name, new_file_name)
        time.sleep(.5)

def merge_tables_3_and_4(folder):
    # find all the files in the PSIY folder that end with "table-4"
    # if there is a "table-3" file from the same page number of the same report
    # then merge copy and paste the text from the t4 file into the t3 file
    # then archive the t4 file
    os.chdir(f'../{folder}')
    this_list = glob.glob('*table-4.csv')
    for t4 in this_list:
        print(t4)
        t3 = t4.replace('table-4', 'table-3')
        if os.path.isfile(t3):
            print("table 3 exist!")
            # Append the contents of t4 directly into t3
            with open(t3, 'a', encoding='utf-8') as outfile:
                with open(t4, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
            # os.rename(t4, f'archive/{t4}')
        else:
            print("table 3 doesn't exist.")
        time.sleep(1)

merge_tables_3_and_4('current_age')
merge_tables_3_and_4('prison_sentence_in_years')
merge_tables_3_and_4('primary_offense_category')

def simple_rename_function_if_only_one_t1_per_report():
    # this function only works when the directory only includes one
    # file that ends in "table-1" for each monthly report
    # which should be the case if only one page was extracted via camelot or
    # the other "table-1" files from subsequent pages have been renamed or
    # moved into an `archive` or `stats` subfolder
    this_list = glob.glob('*table-1.csv')
    for long_fn in this_list:
        new_file_name = f"{long_fn[:7]}.csv"
        print(f"Let's rename {long_fn} -----> {new_file_name}")
        os.rename(long_fn, new_file_name)
        time.sleep(.5)

def idk_1():
    os.chdir('../current_age')
    records = airtab.all(view='current_age', fields=['report'])
    for record in records:
        report = record['fields']['report']
        print(f"Processing report: {report}")
        # doing this instead of merging method
        new_first_file_name = f'{report}.csv'
        this_list = glob.glob(f'{report}-page-*')
        this_list.sort()
        print(f"Found {len(this_list)} files to merge for report '{report}': {this_list}")
        time.sleep(.5)  # Sleep for .5 seconds before starting the merge
        if len(this_list) == 2:
            first_file = this_list[0]
            os.rename(first_file, new_first_file_name)
        else:
            print(f"Skipping report '{report}' because it does not have 2 files in this directory.")

def idk_2():
    os.chdir('../age_at_admission')
    records = airtab.all(view='age_at_admission', fields=['report'])
    for record in records:
        report = record['fields']['report']
        print(f"Processing report: {report}")
        this_list = glob.glob(f'{report}-page-*.csv')
        this_list.sort()
        if len(this_list) == 1:
            this_fn = this_list[0]
            print("there's just one additional file, and i'm moving it to `stats`")
            os.rename(this_fn, f'stats/{this_fn}')
        elif len(this_list) == 2:
            first_file = this_list[0]
            second_file = this_list[1]
            print("there are TWO additional files.")
            print("we'll move a merged file to `stats` & the other to `archive`")
            with open(first_file, 'a', encoding='utf-8') as outfile:
                with open(second_file, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
            time.sleep(1.5)
            os.rename(first_file, f'stats/{first_file}')
            os.rename(second_file, f'archive/{second_file}')
        else:
            print(f"hmmm there are {len(this_list)} additional files for {report}")
            print(this_list)
        time.sleep(1)

def idk_3():
    records = airtab.all(view='years_served', fields=['report'])
    total_records = len(records)
    for record in records:
        report = record['fields']['report']
        print(f"Processing report: {report}")
        # doing this instead of merging method
        this_list = glob.glob(f'{report}-page-*')
        this_list.sort()
        print(f"Found {len(this_list)} files to merge for report '{report}': {this_list}")
        time.sleep(1)  # Sleep for .5 seconds before starting the merge
        if len(this_list) == 3:
            merged_file = f'{report}.csv'
            f1 = this_list[0]
            f2 = this_list[1]
            with open(merged_file, "a", encoding='utf-8') as outfile:
                with open(f1, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
                time.sleep(.5)
                os.rename(f1, f'archive/{f1}')
                with open(f2, 'r', encoding='utf-8') as infile2:
                    outfile.write(infile2.read())
                time.sleep(.5)
                os.rename(f2, f'archive/{f2}')
        else:
            print(f"Skipping report '{report}' because it does not have 3 files in this directory.")
        # keeping these two lines to print the countdown tho :)
        remaining_records = total_records - records.index(record) - 1
        print(f"Remaining records to process: {remaining_records}")


def airtab_to_pdf():
    records = airtab2.all(view='links')
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    for record in records:
        pdf_url = record['fields']['url']
        output_filename = f"{record['fields']['file_name']}.pdf"
        # 1. Send an HTTP GET request to the URL with streaming enabled
        response = requests.get(pdf_url, headers=headers, stream=True)
        # 2. Check if the server responded with a successful status code (200 OK)
        if response.status_code == 200:
            # 3. Open a local file in Write-Binary ('wb') mode
            with open(output_filename, 'wb') as file:
                # 4. Write the file data in chunks of 8KB to save RAM
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"Success! Saved as {output_filename}")
        else:
            print(f"Failed to download. HTTP Status Code: {response.status_code}")
        time.sleep(2)


def pdf_to_dc():
    records = airtab2.all(view='links')
    for record in records:
        this_pdf = f"{record['fields']['path']}/{record['fields']['file_name']}.pdf"
        try:
            obj = dc.documents.upload(this_pdf, access='public', source='GDC', project='225190')
        except requests.exceptions.ReadTimeout:
            time.sleep(5)
            continue
        obj = dc.documents.get(obj.id)
        while obj.status != 'success':
            time.sleep(5)
            obj = dc.documents.get(obj.id)
        this_dict = {}
        this_dict["dc_id"] = str(obj.id)
        print(f"successfully uploaded {obj.title}. . .")
        this_dict["dc_title"] = obj.title
        this_dict["dc_access"] = obj.access
        this_dict["dc_pages"] = obj.pages
        this_dict["dc_canonical_url"] = obj.canonical_url
        airtab2.update(record["id"], this_dict)
