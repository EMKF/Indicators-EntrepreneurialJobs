import joblib
import pandas as pd
import constants as c
from kauffman.tools import file_to_s3
from kauffman.data import qwi, pep


def raw_data_update(qwi_n_threads):
    joblib.dump(str(pd.to_datetime('today')), c.filenamer('data/raw_data/raw_data_fetch_time.pkl'))

    qwi(['EarnBeg'], obs_level='us', private=True, annualize=True) \
        [['time', 'EarnBeg']]. \
        rename(columns={'EarnBeg': 'EarnBeg_us'}). \
        apply(pd.to_numeric). \
        to_csv(c.filenamer('data/raw_data/earnbeg_us.csv'), index=False)

    for region in ['us', 'state', 'msa', 'county']:
        qwi(['Emp', 'EmpEnd', 'EarnBeg', 'EmpS', 'EmpTotal', 'FrmJbC'], obs_level=region, private=True, firm_char=['firmage'], annualize=True, n_threads=qwi_n_threads).\
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
    raw_data_update(qwi_n_threads=5)
    #s3_update()


if __name__ == '__main__':
    main()
