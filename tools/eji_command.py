import os
import shutil
import joblib
import numpy as np
import pandas as pd
import constants as c
from kauffman.data_fetch import qwi, pep
from kauffman.tools import consistent_releases


def _fetch_data_earnbeg_us(fetch_data):
    if fetch_data:
        df = qwi(['EarnBeg'], geo_level='us', private=True, annualize=True) \
            [['time', 'EarnBeg']]. \
            rename(columns={'EarnBeg': 'EarnBeg_us'})
    else:
        df = pd.read_csv(c.filenamer(f'data/raw_data/earnbeg_us.csv')).astype({'time': 'int'})
    joblib.dump(df, c.filenamer(f'data/temp/earnbeg_us.pkl'))


def _fetch_data_qwi(region, fetch_data, qwi_n_threads):
    if fetch_data:
        print(f'\tcreating dataset neb/data/temp/qwi_{region}.pkl')
        df = qwi(geo_level=region, firm_char=['firmage'], n_threads=qwi_n_threads)
    else:
        df = pd.read_csv(c.filenamer(f'data/raw_data/qwi_{region}.csv')). \
            astype({'fips': 'str', 'time': 'int'})
    joblib.dump(df, c.filenamer(f'data/temp/qwi_{region}.pkl'))


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


def _fetch_data_pep(region, fetch_data):
    if fetch_data:
        print(f'\tcreating dataset neb/data/temp/pep_{region}.pkl')
        df = pep(region). \
            query('2001 <= time <= 2020'). \
            pipe(_pep_county_adjustments, region). \
            astype({'time': 'int', 'population': 'int'})
    else:
        df = pd.read_csv(c.filenamer(f'data/raw_data/pep_{region}.csv')). \
            astype({'fips': 'str', 'time': 'int'})
    joblib.dump(df, c.filenamer(f'data/temp/pep_{region}.pkl'))


def _raw_data_fetch(fetch_data, qwi_n_threads):
    if fetch_data and not consistent_releases(n_threads=qwi_n_threads):
        raise Exception(
            'There are multiple releases currently in use for the QWI data. ' \
            'Please either wait for the Census to finish state updates on '
            'the latest release, or assemble the data manually using the ' \
            'files at this link: https://lehd.ces.census.gov/data/qwi/'
        )

    if os.path.isdir(c.filenamer('data/temp')):
        _raw_data_remove(remove_data=True)
    os.mkdir(c.filenamer('data/temp'))

    _fetch_data_earnbeg_us(fetch_data)
    for region in ['us', 'state', 'msa', 'county']:
        _fetch_data_qwi(region, fetch_data, qwi_n_threads)
        _fetch_data_pep(region, fetch_data)


def _raw_data_merge(region):
    return joblib.load(c.filenamer(f'data/temp/qwi_{region}.pkl')) \
        .merge(
            joblib.load(c.filenamer(f'data/temp/pep_{region}.pkl')) \
                .drop(columns=['region', 'geo_level']),
            how='left',
            on=['time', 'fips']
        ) \
        .merge(
            joblib.load(c.filenamer(f'data/temp/earnbeg_us.pkl')), 
            how='left', 
            on='time'
        )


def _missing_obs(df):
    """Identify certain data as NA's rather than 0's"""
    df.loc[df['EmpTotal'] == 0, 'constancy'] = np.nan
    df.loc[df['EarnBeg'] == 0, 'compensation'] = np.nan
    df.loc[df['EmpMid'] == 0, 'contribution'] = np.nan
    return df


def _indicators_create(df):
    """
    Calculate the four indicators.

    Parameters
    ----------
    df : DataFrame
        The raw data

    region : str
        The geographical level of the data. Options: 'us', 'state', 'county', 'msa'

    us_med : DataFrame
        Unconditional US-level earnings

    start_year : int
        First year to be included in the final EJI csv

    end_year : int
        Last year to be included in the final EJI csv

    Returns
    -------
    DataFrame
        Indicators data
    """
    print('indicators_create...')

    return df.\
        assign(
            # tee up values: I return a nan instead of the total if all age categories are not reported.
            EmpMid=lambda x: (x['Emp'] + x['EmpEnd']) / 2,
            total_emp=lambda x: x[['EmpMid', 'fips', 'time']].groupby(['fips', 'time']).transform(lambda y: y.sum() if y.count() == 5 else np.nan),
        ).\
        assign(
            # indicators create
            contribution=lambda x: x['EmpMid'] / x['total_emp'],
            compensation=lambda x: x['EarnBeg'] / x['EarnBeg_us'],
            constancy=lambda x: (x['EmpS'] / x['EmpTotal']),
            creation=lambda x: (x['EmpEnd'] - x['Emp'])/ x['population'] * 1000,
        ). \
        pipe(_missing_obs).\
        query(f'{c.qwi_start_year} <= time <= {c.qwi_end_year}') \
        [['fips', 'geo_level', 'firmage', 'time', 'contribution', 'compensation', 'constancy', 'creation']].\
        sort_values(['fips', 'time', 'firmage']).\
        reset_index(drop=True)


def _fips_formatter(df, region):
    """
    Format the fips column.

    Parameters
    ----------
    df : DataFrame
        Raw indicators data

    region : str
        The geographical level of data. Options: 'us', 'state', 'county', 'msa'

    Returns
    -------
    DataFrame
        Indicators data with formatted fips column
    """
    if region == 'us':
        return df.assign(fips='00')
    elif region == 'state':
        return df.assign(fips=lambda x: x['fips'].apply(lambda row: row if len(row) == 2 else '0' + row))
    else:
        return df.assign(fips=lambda x: x['fips'].apply(lambda row: '00' + row if len(row) == 3 else '0' + row if len(row) == 4 else row))


def _final_jobs_formatter(df, region):
    """
    Format the raw indicator dataframe.

    Parameters
    ----------
    df : DataFrame
        The data

    region : str
        The geographical level of the data. Options: 'us', 'state', 'county', 'msa'

    Returns
    -------
    DataFrame
        The formatted indicators data
    """
    return df. \
        astype({'firmage': 'int'}).\
        pipe(_fips_formatter, region).\
        assign(
            demographic=lambda x: pd.Categorical(x['firmage'].map(c.age_category_dict), ['Ages 0 to 1', 'Ages 2 to 3', 'Ages 4 to 5', 'Ages 6 to 10', 'Ages 11+']),
            type='Age of Business'
        ).\
        rename(columns={'time': 'year', 'type':'demographic-type', 'firmage':'demographic-code'}).\
        sort_values(['fips', 'year', 'demographic']). \
        reset_index(drop=True)


def _enforce_geo_universe(df, region):
    """
    Enforce the presence of the entire universe of counties/msas/states for each year/firmage combo.

    Parameters
    ----------
    df : DataFrame
        The data

    region : str
        The geographical level of the data. Options: 'us', 'state', 'county', 'msa'

    Returns
    -------
    DataFrame
        The complete data, with every fips code (within the input region) by year and firmage.
    """
    firmages = list(range(1,6))

    return c.geography_universe[['fips', 'geo_level', 'name']].\
        query(f'geo_level == "{region}"').\
        drop_duplicates().\
        assign(
            year=lambda x: [[y for y in range(2001,2021)]]*len(x),
            type='Age of Business',
            code=lambda x: [firmages]*len(x)
        ).\
        explode('year').explode('code').\
        assign(demographic=lambda x: x.code.map(c.age_category_dict)).\
        rename(columns={'type':'demographic-type', 'code':'demographic-code'}).\
        merge(df, on=['fips', 'geo_level', 'demographic-type', 'year', 'demographic', 'demographic-code'], how='left')


def final_data_transform(df, region):
    """
    Perform some final cleanup on the indicators dataframe: Format the columns, add the region name as a column, and enforce the presence of the entire universe of counties/msas/states for each year/firmage combo.

    Parameters
    ----------
    df : DataFrame
        The data

    region : str
        The geographical level of the data. Options: 'us', 'state', 'county', 'msa'

    Returns
    -------
    DataFrame
        The formatted data
    """
    print('final_data_transform')
    return df.\
        pipe(_final_jobs_formatter, region).\
        pipe(_enforce_geo_universe, region) \
        [[
            'fips', 'name', 'geo_level', 'year', 'demographic-type', 
            'demographic-code', 'demographic', 'contribution', 'compensation',
            'constancy', 'creation'
        ]]


def _region_all_pipeline(region):
    return _raw_data_merge(region).\
            pipe(_indicators_create).\
            pipe(final_data_transform, region)


def _download_csv_save(df, aws_filepath):
    """Saves download-version of data to a csv."""
    df.to_csv(c.filenamer('data/eji_download.csv'), index=False)
    if aws_filepath:
        df.to_csv(f'{aws_filepath}/eji_download.csv', index=False)
    return df


def _temp_formatter(df, index_cols):
    return df.\
        append(
            df.query('demographic == "Ages 0 to 1"').\
            assign(demographic='')
        ).\
        sort_values(index_cols).reset_index(drop=True).\
        drop(columns=['name', 'geo_level', 'demographic-code']).\
        rename(columns={'fips':'region'})


def _download_to_alley_formatter(df, outcome):
    index_cols = [
        'fips', 'name', 'geo_level', 'demographic-type', 'demographic-code', 
        'demographic'
    ]
    return df.\
        pivot(index=index_cols, columns='year', values=outcome).\
        reset_index().\
        pipe(_temp_formatter, index_cols)


def _website_csvs_save(df, aws_filepath):
    for indicator in ['contribution', 'compensation', 'constancy', 'creation']:
        df_out = df.pipe(_download_to_alley_formatter, indicator)

        df_out.to_csv(c.filenamer(f'data/eji_website_{indicator}.csv'), index=False)
        if aws_filepath:
            df_out.to_csv(f'{aws_filepath}/eji_website_{indicator}.csv', index=False)


def _raw_data_remove(remove_data=True):
    if remove_data:
        shutil.rmtree(c.filenamer('data/temp'))  # remove unwanted files


def eji_data_create_all(raw_data_fetch, raw_data_remove, qwi_n_threads, aws_filepath=None):
    """
    Create and save EJI data. This is the main function of eji_command.py. 

    Fetch raw QWI, PEP, and MSA-crosswalk data, transform it, and save it to two csv's: One for 
    user download, and one formatted for upload to the Kauffman site.
    """
    _raw_data_fetch(raw_data_fetch, qwi_n_threads)

    pd.concat(
        [
            _region_all_pipeline(region) for region in ['us', 'state', 'msa', 'county']
        ]
    ).\
        pipe(_download_csv_save, aws_filepath). \
        pipe(_website_csvs_save, aws_filepath)

    _raw_data_remove(raw_data_remove)


if __name__ == '__main__':
    eji_data_create_all(
        raw_data_fetch=False,
        raw_data_remove=True,
        qwi_n_threads=30
        #aws_filepath='s3://emkf.data.research/indicators/eji/data_outputs'
    )