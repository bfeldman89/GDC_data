#!/usr/bin/env python
import csv

this_list = []
list_of_years = [2005, 2006, 2007, 2008, 2009,
                 2010, 2011, 2012, 2013, 2014,
                 2015, 2016, 2017, 2018, 2019,
                 2020, 2021, 2022, 2023, 2024, 2025]

def consolidate_county_of_conviction_data(data_type='Admissions'):
    for year in list_of_years:
        csv_file = f'annual_reports/csv/county_of_conviction/{data_type}_CY_{year}.csv'
        this_dict = {'CY': year}
        with open(csv_file, 'r', encoding='utf-8') as this_file:
            reader = csv.DictReader(this_file)
            for row in reader:
                county_name = row['County of Conviction'].replace(' ', '_')
                m_county_name = f'{county_name}_m'
                f_county_name = f'{county_name}_f'
                t_county_name = f'{county_name}_t'
                this_dict[m_county_name] = row['M Count'].replace(',', '')
                this_dict[f_county_name] = row['F Count'].replace(',', '')
                this_dict[t_county_name] = row['Total'].replace(',', '')
        for key, value in this_dict.items():
            try:
                this_dict[key] = int(value)
            except ValueError:
                pass
        this_list.append(this_dict)
    # Get the headers from the keys of the first dictionary
    headers = this_list[17].keys()
    output_file = f"annual_reports/csv/county_of_conviction/{data_type.lower()}.csv"
    # Write to the CSV file
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()  # Writes the header row (Name, Age, City)
        writer.writerows(this_list)  # Writes all data rows

consolidate_county_of_conviction_data()
consolidate_county_of_conviction_data('Releases')
