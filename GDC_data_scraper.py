#!/usr/bin/env python
import csv
import os
import time

from pyairtable import Api
from documentcloud import DocumentCloud
import camelot

api = Api(os.environ['AIRTABLE_PAT'])
airtab = api.table(os.environ['GAGA_db'], 'GDC monthly reports')
dc = DocumentCloud(os.environ['MUCKROCK_USERNAME'], os.environ['MUCKROCK_PW'])


def get_page_number():
    # use the documentcloud API to get the page number of the mention
    # obj_list = dc.documents.search('project:225200 "current age"', sort='title', mentions=True)
    # obj_list = dc.documents.search('project:225200 "race group"', sort='title', mentions=True)
    obj_list = dc.documents.search('project:225200 "Prison Sentence In Years"', sort='title', mentions=True)
    for search_result in obj_list:
        this_dict = {}
        this_dict['title'] = search_result.title
        # search_result.access = 'public'
        # search_result.put()
        search_mentions = search_result.mentions
        page_number = search_mentions[1].page
        this_dict['page_number'] = page_number
        this_dict['id'] = search_result.id
        time.sleep(3)
        print(f"{this_dict['title']}\t{this_dict['id']}\t{this_dict['page_number']}")


def create_csv_from_pdf():
    # extract csv files from the correct page of the pdfs using camelot
    records = airtab.all(view='testing', fields=['report', 'race_page_no'])
    for record in records:
        report = record['fields']['report']
        pg_no = record['fields']['race_page_no']
        print(f"report: {report}\tpage: {pg_no}")
        test_pdf = f'/Users/blakefeldman/code/GDC_data/GDC_monthly_reports/pdf/monthly-report_{report}.pdf'
        tables = camelot.read_pdf(test_pdf, pages=pg_no)
        # print(tables[0].parsing_report)
        # tables[0].df
        tables.export(f'{report}.csv', f='csv')
        time.sleep(1.5)


def PSIY_csv_data_to_airtable():
    records = airtab.all(view='testing', fields=['report', 'dc_page_number'])
    for record in records:
        report = record['fields']['report']
        pg_no = record['fields']['dc_page_number']
        print(f"report: {report}\tpage: {pg_no}")
        csv_file = f'/Users/blakefeldman/code/GDC_data/GDC_monthly_reports/csv/camelot/prison_sentence_in_years/{report}-page-{pg_no}-table-1.csv'
        this_dict = {}
        with open(csv_file, 'r') as this_file:
            reader = csv.DictReader(this_file)
            for row in reader:
                if row['Prison Sentence In Years'] == '20.1 - Over':
                    string_a = row['Total'].replace(',', '')
                    this_dict['20+'] = int(string_a)
                elif row['Prison Sentence In Years'] == 'Life':
                    string_b = row['Total'].replace(',', '')
                    this_dict['life'] = int(string_b)
                elif row['Prison Sentence In Years'] == 'Death':
                    string_c = row['Total'].replace(',', '')
                    this_dict['death'] = int(string_c)
                elif row['Prison Sentence In Years'] == 'Life Without Parole':
                    string_d = row['Total'].replace(',', '')
                    this_dict['LWOP'] = int(string_d)
                elif row['Prison Sentence In Years'] == 'Total Reported':
                    string_e = row['Total'].replace(',', '')
                    this_dict['total_pop'] = int(string_e)
        airtab.update(record['id'], this_dict)
        time.sleep(3)


def race_csv_data_to_airtable():
    records = airtab.all(view='current_age', fields=['report', 'current_age_page_no', 'race_page_no', 'psiy_page_no'])
    for record in records:
        report = record['fields']['report']
        pg_no = record['fields']['race_page_no']
        print(f"report: {report}\tpage: {pg_no}")
        csv_file = f'/Users/blakefeldman/code/GDC_data/GDC_monthly_reports/csv/camelot/race_group/{report}-page-{pg_no}-table-1.csv'
        this_dict = {}
        with open(csv_file, 'r') as this_file:
            reader = csv.DictReader(this_file)
            for row in reader:
                if row['Race Group'] == 'White':
                    white_m_string = row['M Count'].replace(',', '')
                    white_f_string = row['F Count'].replace(',', '')
                    white_string = row['Total'].replace(',', '')
                    this_dict['white_male_pop'] = int(white_m_string)
                    this_dict['white_female_pop'] = int(white_f_string)
                    this_dict['white_pop'] = int(white_string)
                elif row['Race Group'] == 'Black':
                    black_m_string = row['M Count'].replace(',', '')
                    black_f_string = row['F Count'].replace(',', '')
                    black_string = row['Total'].replace(',', '')
                    this_dict['black_male_pop'] = int(black_m_string)
                    this_dict['black_female_pop'] = int(black_f_string)
                    this_dict['black_pop'] = int(black_string)
                elif row['Race Group'] == 'Indian':
                    indian_m_string = row['M Count'].replace(',', '')
                    indian_f_string = row['F Count'].replace(',', '')
                    indian_string = row['Total'].replace(',', '')
                    this_dict['indian_male_pop'] = int(indian_m_string)
                    this_dict['indian_female_pop'] = int(indian_f_string)
                    this_dict['indian_pop'] = int(indian_string)
                elif row['Race Group'] == 'Asian':
                    asian_m_string = row['M Count'].replace(',', '')
                    asian_f_string = row['F Count'].replace(',', '')
                    asian_string = row['Total'].replace(',', '')
                    this_dict['asian_male_pop'] = int(asian_m_string)
                    this_dict['asian_female_pop'] = int(asian_f_string)
                    this_dict['asian_pop'] = int(asian_string)
                elif row['Race Group'] == 'Unknown':
                    unknown_m_string = row['M Count'].replace(',', '')
                    unknown_f_string = row['F Count'].replace(',', '')
                    unknown_string = row['Total'].replace(',', '')
                    this_dict['race_unknown_male_pop'] = int(unknown_m_string)
                    this_dict['race_unknown_female_pop'] = int(unknown_f_string)
                    this_dict['race_unknown_pop'] = int(unknown_string)
                elif row['Race Group'] == 'Not Reported':
                    not_reported_m_string = row['M Count'].replace(',', '')
                    not_reported_f_string = row['F Count'].replace(',', '')
                    not_reported_string = row['Total'].replace(',', '')
                    this_dict['race_not_reported_male_pop'] = int(not_reported_m_string)
                    this_dict['race_not_reported_female_pop'] = int(not_reported_f_string)
                    this_dict['race_not_reported_pop'] = int(not_reported_string)
                elif row['Race Group'] == 'Hispanic':
                    hispanic_m_string = row['M Count'].replace(',', '')
                    hispanic_f_string = row['F Count'].replace(',', '')
                    hispanic_string = row['Total'].replace(',', '')
                    this_dict['hispanic_male_pop'] = int(hispanic_m_string)
                    this_dict['hispanic_female_pop'] = int(hispanic_f_string)
                    this_dict['hispanic_pop'] = int(hispanic_string)
                elif row['Race Group'] == 'Native American':
                    native_american_m_string = row['M Count'].replace(',', '')
                    native_american_f_string = row['F Count'].replace(',', '')
                    native_american_string = row['Total'].replace(',', '')
                    this_dict['native_american_male_pop'] = int(native_american_m_string)
                    this_dict['native_american_female_pop'] = int(native_american_f_string)
                    this_dict['native_american_pop'] = int(native_american_string)
                elif row['Race Group'] == 'Native Hawaiian':
                    native_hawaiian_m_string = row['M Count'].replace(',', '')
                    native_hawaiian_f_string = row['F Count'].replace(',', '')
                    native_hawaiian_string = row['Total'].replace(',', '')
                    this_dict['native_hawaiian_male_pop'] = int(native_hawaiian_m_string)
                    this_dict['native_hawaiian_female_pop'] = int(native_hawaiian_f_string)
                    this_dict['native_hawaiian_pop'] = int(native_hawaiian_string)
                elif row['Race Group'] == 'Other':
                    other_m_string = row['M Count'].replace(',', '')
                    other_f_string = row['F Count'].replace(',', '')
                    other_string = row['Total'].replace(',', '')
                    this_dict['race_other_male_pop'] = int(other_m_string)
                    this_dict['race_other_female_pop'] = int(other_f_string)
                    this_dict['race_other_pop'] = int(other_string)
        airtab.update(record['id'], this_dict)
        time.sleep(3)


def current_age_csv_data_to_airtable():
    records = airtab.all(view='current_age', fields=['report', 'current_age_page_no', 'race_page_no', 'psiy_page_no'])
    print(f"records: {len(records)}")
    for record in records:
        report = record['fields']['report']
        pg_no = record['fields']['current_age_page_no']
        print(f"report: {report}\tpage: {pg_no}")
        csv_file = f'/Users/blakefeldman/code/GDC_data/GDC_monthly_reports/csv/camelot/current_age/{report}-page-{pg_no}-table-1.csv'
        this_dict = {}
        with open(csv_file, 'r') as this_file:
            reader = csv.DictReader(this_file)
            for row in reader:
                age_group = row['Current Age'][:5]
                print(age_group)
                if age_group == 'Teens':
                    teens_m_string = row['M Count'].replace(',', '')
                    teens_f_string = row['F Count'].replace(',', '')
                    teens_string = row['Total'].replace(',', '')
                    this_dict['teens_male_pop'] = int(teens_m_string)
                    this_dict['teens_female_pop'] = int(teens_f_string)
                    this_dict['teens_pop'] = int(teens_string)
                elif age_group == 'Twent':
                    twenties_m_string = row['M Count'].replace(',', '')
                    twenties_f_string = row['F Count'].replace(',', '')
                    twenties_string = row['Total'].replace(',', '')
                    this_dict['twenties_male_pop'] = int(twenties_m_string)
                    this_dict['twenties_female_pop'] = int(twenties_f_string)
                    this_dict['twenties_pop'] = int(twenties_string)
                elif age_group == 'Thirt':
                    thirties_m_string = row['M Count'].replace(',', '')
                    thirties_f_string = row['F Count'].replace(',', '')
                    thirties_string = row['Total'].replace(',', '')
                    this_dict['thirties_male_pop'] = int(thirties_m_string)
                    this_dict['thirties_female_pop'] = int(thirties_f_string)
                    this_dict['thirties_pop'] = int(thirties_string)
                elif age_group == 'Forti':
                    forties_m_string = row['M Count'].replace(',', '')
                    forties_f_string = row['F Count'].replace(',', '')
                    forties_string = row['Total'].replace(',', '')
                    this_dict['forties_male_pop'] = int(forties_m_string)
                    this_dict['forties_female_pop'] = int(forties_f_string)
                    this_dict['forties_pop'] = int(forties_string)
                elif age_group == 'Fifti':
                    fifties_m_string = row['M Count'].replace(',', '')
                    fifties_f_string = row['F Count'].replace(',', '')
                    fifties_string = row['Total'].replace(',', '')
                    this_dict['fifties_male_pop'] = int(fifties_m_string)
                    this_dict['fifties_female_pop'] = int(fifties_f_string)
                    this_dict['fifties_pop'] = int(fifties_string)
                elif age_group == 'Sixti':
                    sixties_m_string = row['M Count'].replace(',', '')
                    sixties_f_string = row['F Count'].replace(',', '')
                    sixties_string = row['Total'].replace(',', '')
                    this_dict['sixties_male_pop'] = int(sixties_m_string)
                    this_dict['sixties_female_pop'] = int(sixties_f_string)
                    this_dict['sixties_pop'] = int(sixties_string)
                elif age_group == 'Seven':
                    seventy_plus_m_string = row['M Count'].replace(',', '')
                    seventy_plus_f_string = row['F Count'].replace(',', '')
                    seventy_plus_string = row['Total'].replace(',', '')
                    this_dict['70_plus_male_pop'] = int(seventy_plus_m_string)
                    this_dict['70_plus_female_pop'] = int(seventy_plus_f_string)
                    this_dict['70_plus_pop'] = int(seventy_plus_string)
                elif age_group == 'Grand':
                    total_m_pop_string = row['M Count'].replace(',', '')
                    total_f_pop_string = row['F Count'].replace(',', '')
                    total_string = row['Total'].replace(',', '')
                    this_dict['total_male_pop'] = int(total_m_pop_string)
                    this_dict['total_female_pop'] = int(total_f_pop_string)
                    this_dict['total_pop_2'] = int(total_string)
                elif age_group == 'Not R':
                    not_reported_m_string = row['M Count'].replace(',', '')
                    not_reported_f_string = row['F Count'].replace(',', '')
                    not_reported_string = row['Total'].replace(',', '')
                    this_dict['current_age_not_reported_male'] = int(not_reported_m_string)
                    this_dict['current_age_not_reported_female'] = int(not_reported_f_string)
                    this_dict['current_age_not_reported'] = int(not_reported_string)
                elif age_group == 'Total':
                    total_reported_m_pop_string = row['M Count'].replace(',', '')
                    total_reported_f_pop_string = row['F Count'].replace(',', '')
                    total_reported_string = row['Total'].replace(',', '')
                    this_dict['current_age_reported_male'] = int(total_reported_m_pop_string)
                    this_dict['current_age_reported_female'] = int(total_reported_f_pop_string)
                    this_dict['current_age_reported'] = int(total_reported_string)
        airtab.update(record['id'], this_dict)
        time.sleep(3)

