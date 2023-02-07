import joblib
import pandas as pd
import constants as c
from kauffman.tools import file_to_s3
from kauffman.data_fetch import qwi, pep
from kauffman.tools import consistent_releases


def _pep_county_adjustments(df, region):
    if region == 'county':
        return df. \
            assign(
                fips=lambda x: x.fips.replace(
                    {'02270':'02158', '46113':'46102', '51515':'51019'}
                ),
                region=lambda x: x.region.replace('Bedford city', 'Bedford County')
            ). \
            groupby(['time', 'fips', 'region', 'geo_level']).sum(). \
            reset_index()
    else:
        return df


def raw_data_update(qwi_n_threads):
    # if not consistent_releases(n_threads=qwi_n_threads):
    #     raise Exception(
    #         'There are multiple releases currently in use for the QWI data. ' \
    #         'Please either wait for the Census to finish state updates on '
    #         'the latest release, or assemble the data manually using the ' \
    #         'files at this link: https://lehd.ces.census.gov/data/qwi/'
    #     )
    
    joblib.dump(str(pd.to_datetime('today')), c.filenamer('data/raw_data/raw_data_fetch_time.pkl'))

    qwi(['EarnBeg'], geo_level='us', private=True, annualize=True) \
        [['time', 'EarnBeg']]. \
        rename(columns={'EarnBeg': 'EarnBeg_us'}). \
        apply(pd.to_numeric). \
        to_csv(c.filenamer('data/raw_data/earnbeg_us.csv'), index=False)

    for region in ['us', 'state', 'msa', 'county']:
        qwi(['Emp', 'EmpEnd', 'EarnBeg', 'EmpS', 'EmpTotal', 'FrmJbC'], geo_level=region, private=True, firm_char=['firmage'], annualize=True, n_threads=qwi_n_threads).\
            to_csv(c.filenamer(f'data/raw_data/qwi_{region}.csv'), index=False)

        pep(region).\
            query('2001 <= time <= 2020'). \
            pipe(_pep_county_adjustments, region). \
            to_csv(c.filenamer(f'data/raw_data/pep_{region}.csv'), index=False)


def s3_update():
    files_lst = [
        'raw_data_fetch_time.pkl', 'qwi_us.csv', 'qwi_state.csv', 'qwi_msa.csv', 'qwi_county.csv',
        'pep_us.csv', 'pep_state.csv', 'pep_msa.csv', 'pep_county.csv',
        'earnbeg_us.csv'
    ]

    for file in files_lst:
        file_to_s3(c.filenamer(f'data/raw_data/{file}'), 'emkf.data.research', f'indicators/eji/raw_data/{file}')


def main():
    raw_data_update(qwi_n_threads=30)
    #s3_update()


if __name__ == '__main__':
    main()