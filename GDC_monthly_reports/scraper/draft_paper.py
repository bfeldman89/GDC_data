#!/usr/bin/env python
import csv
import json
import os
import time

from pyairtable import Api
from documentcloud import DocumentCloud
import camelot

api = Api(os.environ['AIRTABLE_PAT'])
airtab = api.table(os.environ['GAGA_db'], 'DC monthly reports')
dc = DocumentCloud(os.environ['MUCKROCK_USERNAME'], os.environ['MUCKROCK_PW'])


def get_page_number():
    # use the documentcloud API to get the page number of the mention
    # obj_list = dc.documents.search('project:225200', mentions=True)
    obj_list_2 = dc.documents.search('user:17279 "Prison Sentence In Years"', sort='title', page=1, per_page=50, mentions=True)
    for search_result in obj_list_2:
        this_dict = {}
        this_dict['title'] = search_result.title
        search_result.access = 'public'
        search_result.put()
        search_mentions = search_result.mentions
        page_number = search_mentions[1].page
        this_dict['page_number'] = page_number
        this_dict['id'] = search_result.id
        time.sleep(3)
        print(f"{this_dict['title']}\t{this_dict['id']}\t{this_dict['page_number']}")


def create_csv_from_pdf():
    # extract csv files from the correct page of the pdfs using camelot
    records = airtab.all(view='testing', fields=['report', 'dc_page_number'])
    for record in records:
        report = record['fields']['report']
        pg_no = record['fields']['dc_page_number']
        print(f"report: {report}\tpage: {pg_no}")
        test_pdf = f'/Users/blakefeldman/code/GDC_data/GDC_monthly_reports/pdf/monthly-report_{report}.pdf'
        tables = camelot.read_pdf(test_pdf, pages=pg_no)
        # print(tables[0].parsing_report)
        # tables[0].df
        tables.export(f'camelot_{report}.csv', f='csv')
        time.sleep(2)


def csv_data_to_airtable():
    records = airtab.all(view='testing', fields=['report', 'dc_page_number'])
    for record in records:
        report = record['fields']['report']
        pg_no = record['fields']['dc_page_number']
        print(f"report: {report}\tpage: {pg_no}")
        csv_file = f'/Users/blakefeldman/code/GDC_data/GDC_monthly_reports/csv/camelot/camelot_{report}-page-{pg_no}-table-1.csv'
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

