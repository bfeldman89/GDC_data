# GDC_data

## GDC Monthly Reports

### summary

The Georgia Department of Corrections publishes monthly statistical reports that describe its population and admissions according to several data points, such as race, age, offense, sentence, etc. The reports are [published](https://gdc.georgia.gov/organization/about-gdc/agency-activity/research-and-reports/monthly-statistical-reports/profiles) in PDF format. This repository includes:

- a python script used to (1) convert tables in the PDF files into csv files and (2) upload the data into an Airtable base
- each monthly report in PDF format (available at `monthly_reports/pdf`)
- csv tables extracted from the PDFs (available at `monthly_reports/csv`)

One of the goals of this project was to be able to visualize trends in GDC admissions and population. `csv` files of data aggregated from hundreds of monthly reports to better understand trends will be made available `monthly_reports/csv`. Line charts and other data visualizations might also be added in the future. For now, Airtable views of aggregated data are hyperlinked in the [final section of this README document](https://github.com/bfeldman89/GDC_data/blob/main/README.md#tabular-data).

_note that the PDFs are also available in a public [DocumentCloud project](https://www.documentcloud.org/projects/225200-gdc_monthly_reports/)_

### example

#### pdf

`Profile_all_inmates_2026_01.pdf` is available on GDC's website. Page 5 of the report breaks down the GDC population by race and gender. The PDF is available in the repository at `monthly_reports/pdf/monthly-report_2026-01.pdf`.

<img width="2480" height="3509" alt="monthly-report_2026-01_page-5" src="https://github.com/user-attachments/assets/439ed144-c6f3-4381-bf89-dc7b6fe63db6" />
<br/>
<br/>

#### extracted csv files

The python script is used to extract the 3 tables from the page and create 3 csv files. I use regex "find and replace" in Visual Studio Code and a simple python script to merge table 2 (`2026-01-page-5-table-2.csv`) into table 1 `2026-01-page-5-table-1.csv` before deleting table 2. The two csv files for page 5 of the `monthly-report_2026-01.pdf` are `reace_group/2026-01.csv` and `race_group/stats/2026-01-page-5-table-3.csv`. Here is what they look like:

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

#### airtable

This data is taken from each monthly report's "Race Group" table (mid-2005 to present) and uploaded to an Airtable Base. Here is a screenshot highlighting the "Race Group" data for the 2026_01 report.

<img width="1210" height="566" alt="Screenshot 2026-07-22 at 1 25 04 AM" src="https://github.com/user-attachments/assets/a04e0952-74c0-4319-a79f-8bd48ebf01e0" />
<br/>
<br/>

### script

`GDC_data_scraper.py`

### pdf files

`monthly_reports/pdf/`

`annual_reports/pdf/`

`other_reports`

### tabular data

#### Data from Monthly Reports

| Table (as titled by GDC)                                    | csv extracted from each PDF                     | data pulled from all reports                                                                                                                                                                 |
|-------------------------------------------------------------|-------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Prison sentence in years                                    | `monthly_reports/csv/prison_sentence_in_years/` | [Airtable](https://airtable.com/appxNeOaDgZm07EhE/shr3JAcBIP6dqRYxR) / [csv](https://github.com/bfeldman89/GDC_data/blob/main/monthly_reports/csv/prison_sentence_in_years/consolidated.csv) |
| Current age, broken out in ten-year age groups              | `monthly_reports/csv/current_age/`              | [Airtable](https://airtable.com/appxNeOaDgZm07EhE/shrjripCdl7TxwEWl) / [csv](https://github.com/bfeldman89/GDC_data/blob/main/monthly_reports/csv/current_age/consolidated.csv)              |
| Race group                                                  | `monthly_reports/csv/race_group/`               | [Airtable](https://airtable.com/appxNeOaDgZm07EhE/shr8EFMIix4AJ7JeT) / [csv](https://github.com/bfeldman89/GDC_data/blob/main/monthly_reports/csv/race_group/consolidated.csv)               |
| Primary offense, broken out into six broad crime categories | `monthly_reports/csv/primary_offense_category/` | [Airtable](https://airtable.com/appxNeOaDgZm07EhE/shr07wH3tMwmNX9Tc) / [csv](https://github.com/bfeldman89/GDC_data/blob/main/monthly_reports/csv/primary_offense_category/consolidated.csv) |
| Years served (jail + prison) in this incarceration          | `monthly_reports/csv/years_served/`             | [Airtable](https://airtable.com/appxNeOaDgZm07EhE/shrdzQiCBwiF2CKFs)                                                                                                                         |
| Age at admission                                            | `monthly_reports/csv/age_at_admission/`         | [Airtable](https://airtable.com/appxNeOaDgZm07EhE/shrObdjcnb1KLljJd)                                                                                                                         |
| County of conviction of primary offense                     | `monthly_reports/csv/county_of_conviction/`     | [Airtable](https://airtable.com/appxNeOaDgZm07EhE/shrDGfiNtpEw36t1f)                                                                                                                         |

#### Data from Annual Reports

| Table (as titled by GDC)                                    | csv extracted from each PDF                     | data pulled from all reports                                                                                                                                                                 |
|-------------------------------------------------------------|-------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Prison sentence in years                                    | `annual_reports/csv/prison_sentence_in_years/`  | [Airtable](https://airtable.com/appxNeOaDgZm07EhE/shrrkz9DjtXwCOJaX) / [csv](https://github.com/bfeldman89/GDC_data/blob/main/annual_reports/csv/prison_sentence_in_years/consolidated.csv)  |
| Current age, broken out in ten-year age groups              | `annual_reports/csv/current_age/`               | [Airtable](https://airtable.com/appxNeOaDgZm07EhE/shrpX4hZLnp2jrkZy) / [csv](https://github.com/bfeldman89/GDC_data/blob/main/annual_reports/csv/current_age/consolidated.csv)               |
| Race group                                                  | `annual_reports/csv/race_group/`                | [Airtable](https://airtable.com/appxNeOaDgZm07EhE/shrxPLbtOQCo61SVm) / [csv](https://github.com/bfeldman89/GDC_data/blob/main/annual_reports/csv/race_group/consolidated.csv)                |
| Primary offense, broken out into six broad crime categories | `annual_reports/csv/primary_offense_category/`  | [Airtable](https://airtable.com/appxNeOaDgZm07EhE/shr3XWAVrVTpQpKD9) / [csv](https://github.com/bfeldman89/GDC_data/blob/main/annual_reports/csv/primary_offense_category/consolidated.csv)  |
| Years served (jail + prison) in this incarceration          | `annual_reports/csv/years_served/`              |                                                                                                                                                                                              |
| Age at admission                                            | `annual_reports/csv/age_at_admission/`          |                                                                                                                                                                                              |
| County of conviction of primary offense                     | `annual_reports/csv/county_of_conviction/`      |                                                                                                                                                                                              |
