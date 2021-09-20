import sys
import boto3
import joblib
import pandas as pd
import constants as c
from kauffman.tools import file_to_s3
from kauffman.data import qwi, pep

pd.set_option('max_columns', 1000)
pd.set_option('max_info_columns', 1000)
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 30000)
pd.set_option('max_colwidth', 4000)
pd.set_option('display.float_format', lambda x: '%.3f' % x)
pd.set_option('chained_assignment',None)


def raw_data_update():
    joblib.dump(str(pd.to_datetime('today')), c.filenamer('data/raw_data/raw_data_fetch_time.pkl'))

    qwi(['EarnBeg'], obs_level='us', private=True, annualize=True) \
        [['time', 'EarnBeg']]. \
        rename(columns={'EarnBeg': 'EarnBeg_us'}). \
        apply(pd.to_numeric). \
        to_csv(c.filenamer('data/raw_data/earnbeg_us.csv'), index=False)

    for region in ['us', 'state', 'msa', 'county']:
        qwi(['Emp', 'EmpEnd', 'EarnBeg', 'EmpS', 'EmpTotal', 'FrmJbC'], obs_level=region, private=True, strata=['firmage'], annualize=True).\
            to_csv(c.filenamer(f'data/raw_data/qwi_{region}.csv'), index=False)

        pep(region).\
            rename(columns={'POP': 'population'}). \
            to_csv(c.filenamer(f'data/raw_data/pep_{region}.csv'), index=False)





def s3_update():
    files_lst = [
        'raw_data_fetch_time.pkl', 'qwi_us.csv', 'qwi_state.csv', 'qwi_msa.csv', 'qwi_county.csv',
        'pep_us.csv', 'pep_state.csv', 'pep_msa.csv', 'pep_county.csv',
        'earnbeg_us.csv'
    ]

    for file in files_lst:
        file_to_s3(c.filenamer(f'data/raw_data/{file}'), 'emkf.data.research', f'indicators/mpj/raw_data/{file}')


def main():
    raw_data_update()
    s3_update()


if __name__ == '__main__':
    main()
