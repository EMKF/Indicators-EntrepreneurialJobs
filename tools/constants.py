import os
import pandas as pd
import numpy as np

def filenamer(path):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(ROOT_DIR, '../' + path)

index_vars_dict = {
    'contribution': {'polarity': 'pos'},
    'compensation': {'polarity': 'pos'},
    'constancy': {'polarity': 'pos'}
}

age_category_dict = {
    0: 'Total',
    1: 'Ages 0 to 1',
    2: 'Ages 2 to 3',
    3: 'Ages 4 to 5',
    4: 'Ages 6 to 10',
    5: 'Ages 11+'
}

qwi_start_year = 2001
qwi_end_year = 2020

geography_universe = pd.read_csv('https://lehd.ces.census.gov/data/schema/latest/label_geography.csv').\
    query('geo_level in ["N", "S", "M", "C"]').\
    assign(
        state=lambda x: x.geography.str[0:2],
        fips=lambda x: np.where(x.geo_level == 'M', x.geography.str[2:], x.geography),
        name=lambda x: x.label.str.split('(').str[0].\
            str.rstrip().replace({'National':'United States'})
    ).\
    query('fips != "99999" and state != "72"').\
    reset_index(drop=True)

region_to_code = {
    'us':'N',
    'state':'S',
    'msa':'M',
    'county':'C'
}