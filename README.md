# GDC_data

## GDC Monthly 

The Georgia Department of Corrections publishes monthly statistical reports that describe its population and admissions according to several data points, such as race, age, offense, sentence, etc. The reports are [published](https://gdc.georgia.gov/organization/about-gdc/agency-activity/research-and-reports/monthly-statistical-reports/profiles) in PDF format. This repository includes:
 - a python script used to (1) convert tables in the PDF files into csv files and (2) upload the data into an Airtable base
 - each monthly report in PDF format (available at `GDC_monthly_reports/pdf`)
 - csv tables extracted from the PDFs (available at `GDC_monthly_reports/csv/camelot`)

One of the goals of this project was to be able to visualize trends in GDC admissions and population. `csv` files of data aggregated from hundreds of monthly reports to better understand trends will be made available `GDC_monthly_reports/csv/`. Line charts and other data visualizations might also be added in the future. For now, Airtable views of aggregated data are hyperlinked in the [final section of this README document](https://github.com/bfeldman89/GDC_data/blob/main/README.md#tabular-data). 

_note that the PDFs are also available in a public [DocumentCloud project](https://www.documentcloud.org/projects/225200-gdc_monthly_reports/)_

### example

`Profile_all_inmates_2026_01.pdf` is available on GDC's website. Page 5 of the report breaks down the GDC population by race and gender. The PDF is available in the repository at `GDC_monthly_reports/pdf/monthly-report_2026-01.pdf`.

<img width="2480" height="3509" alt="monthly-report_2026-01_page-5" src="https://github.com/user-attachments/assets/439ed144-c6f3-4381-bf89-dc7b6fe63db6" />


The python script is used to extract the 3 tables from the page and create 3 csv files. I use regex "find and replace" in Visual Studio Code and a simple python script to merge table 2 (`2026-01-page-5-table-2.csv`) into table 1 `2026-01-page-5-table-1.csv` before deleting table 2. The two csv files for page 5 of the `monthly-report_2026-01.pdf` are `2026-01-page-5-table-1.csv` and `2026-01-page-5-table-3.csv`. Here is what they look like:

| **Race Group**      | **M Count** | **M Col %** | **M Row %** | **F Count** | **F Col %** | **F Row %** | **Total** | **Col %** |
|---------------------|-------------|-------------|-------------|-------------|-------------|-------------|-----------|-----------|
| **White**           | 15,982      | 32.53%      | 87.52%      | 2,279       | 55.93%      | 12.48%      | 18,261    | 34.32%    |
| **Black**           | 30,301      | 61.67%      | 94.63%      | 1,721       | 42.23%      | 5.37%       | 32,022    | 60.18%    |
| **Other**           | 24          | 0.05%       | 82.76%      | 5           | 0.12%       | 17.24%      | 29        | 0.05%     |
| **Asian**           | 155         | 0.32%       | 92.81%      | 12          | 0.29%       | 7.19%       | 167       | 0.31%     |
| **Unknown**         | 1           | 0.01%       | 100.0%      | 0           | 0%          | 0%          | 1         | 0.01%     |
| **Hispanic**        | 2,633       | 5.36%       | 97.99%      | 54          | 1.33%       | 2.01%       | 2,687     | 5.05%     |
| **Native American** | 37          | 0.08%       | 90.24%      | 4           | 0.1%        | 9.76%       | 41        | 0.08%     |
| **Native Hawaiian** | 2           | 0.01%       | 100.0%      | 0           | 0%          | 0%          | 2         | 0.01%     |
| **Total Reported**  | 49,135      | 100.00%     | 92.34%      | 4,075       | 100.00%     | 7.66%       | 53,210    | 100.00%   |
| **Not Reported**    | 0           |             |             | 0           |             |             | 0         |           |
| **Grand Total**     | 49,135      |             |             | 4,075       |             |             | 53,210    |           |


| **statistic**            | **Male** | **Female** | **Total** |
|--------------------------|----------|------------|-----------|
| **Mode (most frequent)** | Black    | White      | Black     |


This data is taken from each monthly report's "Race Group" table (mid-2005 to present) and uploaded to an Airtable Base. Here is a screenshot highlighting the data "Race Group" data for the 2026_01 report. 

<img width="1210" height="566" alt="Screenshot 2026-07-22 at 1 25 04 AM" src="https://github.com/user-attachments/assets/a04e0952-74c0-4319-a79f-8bd48ebf01e0" />

### script

`GDC_data_scraper.py`

### pdf files

`GDC_monthly_reports/pdf/`

### tabular data

| Table (as titled by GDC) | csv extracted from each PDF | data pulled from all reports (2005-07 to present) |
|--------------------------|-----------------------------|---------------------------------------------------|
| Prison sentence in years | `GDC_monthly_reports/csv/camelot/prison_sentence_in_years/` | [Airtable](https://airtable.com/appxNeOaDgZm07EhE/shr3i1YAdVlAX3XbW) |
| Current age, broken out in ten-year age groups | `GDC_monthly_reports/csv/camelot/current_age/` | [Airtable](https://airtable.com/appxNeOaDgZm07EhE/shrjripCdl7TxwEWl) |
| Race group | `GDC_monthly_reports/csv/camelot/race_group/` | [Airtable](https://airtable.com/appxNeOaDgZm07EhE/shr8EFMIix4AJ7JeT) |
