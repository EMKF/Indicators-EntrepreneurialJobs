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

website_fips = [
    '00', '01', '02', '04', '05', '06', '08', '09', '10', '11', '12', '13',
    '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',
    '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38',
    '39', '40', '41', '42', '44', '45', '46', '47', '48', '49', '50', '51',
    '53', '54', '55', '56',
    '12060', '12420', '12580', '13820', '14460', '15380', '16740', '16980',
    '17140', '17460', '18140', '19100', '19740', '19820', '25540', '26420',
    '26900', '27260', '28140', '29820', '31080', '31140', '32820', '33100',
    '33340', '33460', '34980', '35380', '35620', '36420', '36740', '37980',
    '38060', '38300', '38900', '39300', '39580', '40060', '40140', '40900',
    '41180', '41620', '41700', '41740', '41860', '41940', '42660', '45300',
    '47260', '47900'
]