# Overview
Python code for generating the csv files containing the Kauffman Foundation's Multi-Dimensional Jobs (MPJ) indicators data (see https://indicators.kauffman.org/series/). 

# Files
The repository has two subdirectories:
### 1. `data`
This directory contains a raw_data folder with source data (nine csv files and a `pkl` file of a string of a timestamp when the data was
pulled), output (six csv files available after running `mpj_command.py`), and a `TEMP` directory with data files created when `mpj_command.py` is run. 

### 2. `tools` 
Within this directory there are three files:
1.  `mpj_command.py`: Running this file will generate the data using the function `mpj_data_create_all`, which has three parameters:
    * `raw_data_fetch`, which allows the user to specify whether to fetch the raw data from source (see below) or use the data in `data/raw_data`.
    * `raw_data_remove`, which allows the user to specify whether to remove the temporary data files.
    * `aws_filepath`, which allows the user to specify whether to stash the data in S3.   

    The output consists of six csv files: one formatted the same as the file available for download on the webpage (see *replace this when path becomes available*), and five (one for each indicator) that are used to create the visualizations on the webpage. The data consists of annual values for each indicator by state (including Washington DC) and U.S. The U.S. level data is further subset by type (ex: age, race, sex, etc.) and category (for type = age, categories include: 'Ages 20-34', 'Ages 35-44', etc.)

2. `mpj_raw_data_fetch.py`: This file generates the data in the directory `data > raw_data`. It is used to update the data for the yearly MPJ indicators update.
    * `raw_data_update()`, generates the US- and state-level datafiles, formated as csv, and the data timestamp.
    * `s3_update()`, stashes the csvs and timestamp in S3.

3. `constants.py`: A file with constant values used in `mpj_command.py` and `mpj_raw_data_fetch.py` 


# Feedback
Questions or comments can be directed to indicators@kauffman.org.


# Disclaimer
The content presented in this repository is presented as a courtesy to be used only for informational purposes. The 
content is provided “As Is” and is not represented to be error free. The Kauffman Foundation makes no representation or 
warranty of any kind with respect to the content and any such representations or warranties are hereby expressly 
disclaimed.