#!/usr/bin/env python
import csv
import os
import time
import camelot

from pyairtable import Api
from pyairtable.formulas import match
from documentcloud import DocumentCloud

api = Api(os.environ['AIRTABLE_PAT'])
airtab = api.table(os.environ['GAGA_db'], 'GDC reports')
dc = DocumentCloud(os.environ['MUCKROCK_USERNAME'], os.environ['MUCKROCK_PW'])

def get_page_number(project_id, search_terms, page_number_field):
    """Look up page mentions for a search term and update the matching Airtable record."""
    # get_page_number('225190', 'broad crime categories', 'primary_offense_category_page_no')
    # get_page_number('225190', 'years served', 'years_served_page_no')
    # get_page_number('225190', 'current age', 'current_age_page_no')
    # get_page_number('225190', 'race group', 'race_page_no')
    # get_page_number('225190', 'County of conviction','county_of_conviction_page_no')
    # get_page_number('225190', 'Age at admission', 'age_at_admission_page_no')
    # get_page_number('225190', 'sentence in years', 'psiy_page_no')
    # project_id is 225200 for monthly reports and 225190 for others
    obj_list = dc.documents.search(f'project:{project_id} "{search_terms}"', sort='title', mentions=True)
    for search_result in obj_list:
        this_dict = {}
        page_numbers = []
        dc_id = search_result.id
        record = airtab.first(formula=match({'dc_id': dc_id}))
        mentions = search_result.mentions
        for mention in mentions:
            page_number = mention.page
            page_numbers.append(page_number)
        this_dict[page_number_field] = ",".join(page_numbers[1:])
        airtab.update(record['id'], this_dict)
        print(f"Updated record {record['fields']['dc_title']} with page numbers: {this_dict[page_number_field]}")
        time.sleep(1)

def create_csv_from_pdf(folder, view_name, report_type):
    """Extract CSV tables from monthly report PDFs using the correct page number."""
    # example folders: 'primary_offense_category', 'county_of_conviction', 'age_at_admission'
    pg_no_field = f"{folder}_page_no"
    records = airtab.all(view=view_name, fields=['report', pg_no_field])
    print(f"found {len(records)} records in the {view_name} view")
    for record in records:
        report = record['fields']['report']
        pg_no = record['fields'][pg_no_field]
        print(f"report: {report}\tpage: {pg_no}")

        if report_type == 'monthly':
            this_pdf = f'monthly_reports/pdf/monthly-report_{report}.pdf'
        elif report_type == 'annual':
            this_pdf = f'annual_reports/pdf/{report}.pdf'
        else:
            raise ValueError(f"Unsupported report type: {report_type}")

        tables = camelot.read_pdf(this_pdf, pages=pg_no)
        tables.export(f'{report_type}_reports/csv/{folder}/{report}.csv', f='csv')
        time.sleep(.5)


def PSIY_csv_data_to_airtable(report_type, view_name):
    records = airtab.all(view=view_name, fields=['report'])
    print(len(records))
    time.sleep(3)
    for record in records:
        report = record['fields']['report']
        csv_file = f'{report_type}_reports/csv/prison_sentence_in_years/{report}.csv'
        this_dict = {}
        with open(csv_file, 'r', encoding='utf-8') as this_file:
            reader = csv.DictReader(this_file)
            for row in reader:
                if row['Prison Sentence In Years'] == '20.1 - Over':
                    this_dict['PSIY_20.1+'] = row['Total'].replace(',', '')
                    this_dict['PSIY_20.1+_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_20.1+_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == 'Life':
                    this_dict['PSIY_life'] = row['Total'].replace(',', '')
                    this_dict['PSIY_life_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_life_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == 'Death':
                    this_dict['PSIY_death'] = row['Total'].replace(',', '')
                    this_dict['PSIY_death_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_death_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == 'Life Without Parole':
                    this_dict['PSIY_LWOP'] = row['Total'].replace(',', '')
                    this_dict['PSIY_LWOP_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_LWOP_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == 'Total Reported':
                    this_dict['PSIY_total_reported'] = row['Total'].replace(',', '')
                    this_dict['PSIY_total_reported_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_total_reported_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == 'Not Reported':
                    this_dict['PSIY_not_reported'] = row['Total'].replace(',', '')
                    this_dict['PSIY_not_reported_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_not_reported_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == '0 - 1':
                    this_dict['PSIY_0-1'] = row['Total'].replace(',', '')
                    this_dict['PSIY_0-1_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_0-1_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == '1.1 - 2':
                    this_dict['PSIY_1.1-2'] = row['Total'].replace(',', '')
                    this_dict['PSIY_1.1-2_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_1.1-2_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == '2.1 - 3':
                    this_dict['PSIY_2.1-3'] = row['Total'].replace(',', '')
                    this_dict['PSIY_2.1-3_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_2.1-3_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == '3.1 - 4':
                    this_dict['PSIY_3.1-4'] = row['Total'].replace(',', '')
                    this_dict['PSIY_3.1-4_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_3.1-4_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == '4.1 - 5':
                    this_dict['PSIY_4.1-5'] = row['Total'].replace(',', '')
                    this_dict['PSIY_4.1-5_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_4.1-5_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == '5.1 - 6':
                    this_dict['PSIY_5.1-6'] = row['Total'].replace(',', '')
                    this_dict['PSIY_5.1-6_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_5.1-6_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == '6.1 - 7':
                    this_dict['PSIY_6.1-7'] = row['Total'].replace(',', '')
                    this_dict['PSIY_6.1-7_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_6.1-7_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == '7.1 - 8':
                    this_dict['PSIY_7.1-8'] = row['Total'].replace(',', '')
                    this_dict['PSIY_7.1-8_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_7.1-8_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == '8.1 - 9':
                    this_dict['PSIY_8.1-9'] = row['Total'].replace(',', '')
                    this_dict['PSIY_8.1-9_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_8.1-9_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == '9.1 - 10':
                    this_dict['PSIY_9.1-10'] = row['Total'].replace(',', '')
                    this_dict['PSIY_9.1-10_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_9.1-10_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == '10.1 - 12':
                    this_dict['PSIY_10.1-12'] = row['Total'].replace(',', '')
                    this_dict['PSIY_10.1-12_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_10.1-12_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == '12.1 - 15':
                    this_dict['PSIY_12.1-15'] = row['Total'].replace(',', '')
                    this_dict['PSIY_12.1-15_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_12.1-15_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == '15.1 - 20':
                    this_dict['PSIY_15.1-20'] = row['Total'].replace(',', '')
                    this_dict['PSIY_15.1-20_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_15.1-20_f'] = row['F Count'].replace(',', '')
                elif row['Prison Sentence In Years'] == 'Youthful Offenders':
                    this_dict['PSIY_YO'] = row['Total'].replace(',', '')
                    this_dict['PSIY_YO_m'] = row['M Count'].replace(',', '')
                    this_dict['PSIY_YO_f'] = row['F Count'].replace(',', '')
                else:
                    print(f"Unrecognized Prison Sentence In Years value: {row['Prison Sentence In Years']}")
        # now convert all those strings to integers
        for key, value in this_dict.items():
            this_dict[key] = int(value)
        airtab.update(record['id'], this_dict)
        time.sleep(3)


def race_csv_data_to_airtable(report_type, view_name, folder):
    records = airtab.all(view=view_name, fields=['report'])
    for record in records:
        report = record['fields']['report']
        csv_file = f'{report_type}_reports/csv/{folder}/{report}.csv'
        this_dict = {}
        with open(csv_file, 'r', encoding='utf-8') as this_file:
            reader = csv.DictReader(this_file)
            for row in reader:
                if row['Race Group'] == 'White':
                    this_dict['white_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['white_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['white_pop'] = row['Total'].replace(',', '')
                elif row['Race Group'] == 'Black':
                    this_dict['black_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['black_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['black_pop'] = row['Total'].replace(',', '')
                elif row['Race Group'] == 'Indian':
                    this_dict['indian_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['indian_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['indian_pop'] = row['Total'].replace(',', '')
                elif row['Race Group'] == 'Asian':
                    this_dict['asian_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['asian_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['asian_pop'] = row['Total'].replace(',', '')
                elif row['Race Group'] == 'Unknown':
                    this_dict['race_unknown_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['race_unknown_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['race_unknown_pop'] = row['Total'].replace(',', '')
                elif row['Race Group'] == 'Not Reported':
                    this_dict['race_not_reported_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['race_not_reported_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['race_not_reported_pop'] = row['Total'].replace(',', '')
                elif row['Race Group'] == 'Total Reported':
                    this_dict['race_reported_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['race_reported_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['race_reported'] = row['Total'].replace(',', '')
                elif row['Race Group'] == 'Hispanic':
                    this_dict['hispanic_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['hispanic_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['hispanic_pop'] = row['Total'].replace(',', '')
                elif row['Race Group'] == 'Native American':
                    this_dict['native_american_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['native_american_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['native_american_pop'] = row['Total'].replace(',', '')
                elif row['Race Group'] == 'Native Hawaiian':
                    this_dict['native_hawaiian_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['native_hawaiian_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['native_hawaiian_pop'] = row['Total'].replace(',', '')
                elif row['Race Group'] == 'Other':
                    this_dict['race_other_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['race_other_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['race_other_pop'] = row['Total'].replace(',', '')
        # now convert all those strings to integers
        for key, value in this_dict.items():
            this_dict[key] = int(value)
        airtab.update(record['id'], this_dict)
        time.sleep(3)


def current_age_csv_data_to_airtable(report_type, view_name, folder):
    records = airtab.all(view=view_name, fields=['report'])
    print(f"records: {len(records)}")
    time.sleep(3)
    for record in records:
        report = record['fields']['report']
        csv_file = f'{report_type}_reports/csv/{folder}/{report}.csv'
        this_dict = {}
        with open(csv_file, 'r', encoding='utf-8') as this_file:
            reader = csv.DictReader(this_file)
            for row in reader:
                age_group = row['Current Age'][:5]
                print(age_group)
                if age_group == 'Teens':
                    this_dict['teens_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['teens_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['teens_pop'] = row['Total'].replace(',', '')
                elif age_group == 'Twent':
                    this_dict['twenties_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['twenties_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['twenties_pop'] = row['Total'].replace(',', '')
                elif age_group == 'Thirt':
                    this_dict['thirties_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['thirties_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['thirties_pop'] = row['Total'].replace(',', '')
                elif age_group == 'Forti':
                    this_dict['forties_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['forties_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['forties_pop'] = row['Total'].replace(',', '')
                elif age_group == 'Fifti':
                    this_dict['fifties_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['fifties_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['fifties_pop'] = row['Total'].replace(',', '')
                elif age_group == 'Sixti':
                    this_dict['sixties_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['sixties_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['sixties_pop'] = row['Total'].replace(',', '')
                elif age_group == 'Seven':
                    this_dict['70_plus_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['70_plus_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['70_plus_pop'] = row['Total'].replace(',', '')
                elif age_group == 'Grand':
                    this_dict['total_male_pop'] = row['M Count'].replace(',', '')
                    this_dict['total_female_pop'] = row['F Count'].replace(',', '')
                    this_dict['total_pop'] = row['Total'].replace(',', '')
                elif age_group == 'Not R':
                    this_dict['current_age_not_reported_male'] = row['M Count'].replace(',', '')
                    this_dict['current_age_not_reported_female'] = row['F Count'].replace(',', '')
                    this_dict['current_age_not_reported'] = row['Total'].replace(',', '')
                elif age_group == 'Total':
                    this_dict['current_age_reported_male'] = row['M Count'].replace(',', '')
                    this_dict['current_age_reported_female'] = row['F Count'].replace(',', '')
                    this_dict['current_age_reported'] = row['Total'].replace(',', '')
        # now convert all those strings to integers
        for key, value in this_dict.items():
            this_dict[key] = int(value)
        airtab.update(record['id'], this_dict)
        time.sleep(3)

def append_csv2_to_csv1():
    records = airtab.all(view='testing', fields=['report', 'age_page_no', 'race_page_no', 'psiy_page_no'])
    for record in records:
        report = record['fields']['report']
        pg_no = record['fields']['race_page_no']
        print(f"report: {report}\tpage: {pg_no}")
        fn1 = f'monthly_reports/csv/race_group/{report}-page-{pg_no}-table-1.csv'
        fn2 = f'monthly_reports/csv/race_group/{report}-page-{pg_no}-table-2.csv'
        # Append the contents of file2 directly into file1
        with open(fn1, 'a', encoding='utf-8') as outfile:
            with open(fn2, 'r', encoding='utf-8') as infile:
                outfile.write('\n' + infile.read())
