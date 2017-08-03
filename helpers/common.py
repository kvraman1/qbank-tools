import os
import pandas as pd
import collections
import helpers.general_helper as gh
import re
import pickle

DATA_DIR = os.path.realpath(os.path.dirname(__file__)) + '/../../data'
BUNDLED_DATA_DIR = os.path.realpath(os.path.dirname(__file__)) + '/../dashboard/bundled_data'
CHECKPT_DIR = DATA_DIR + '/checkpoints'

JSON_DIR = DATA_DIR + '/jsons'

SCRAPE_STATUS_CSV_FNAME = 'scraped-status.csv'

CLEAN_FULL_FPATH = DATA_DIR + '/clean-full.csv'
CLEAN_LIGHT_FPATH = DATA_DIR + '/clean-light.csv'
PROBLEM_REPORTS_DIR = DATA_DIR + '/problem-reports'


def get_pickle_obj_fpath(name):
    path = '{}/{}.pkl'.format(CHECKPT_DIR, name)

    if os.path.exists(path):
        return path

    return '{}/{}.pkl'.format(BUNDLED_DATA_DIR, name)


def save_obj(obj, name):
    with open(get_pickle_obj_fpath(name), 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(name):
    with open(get_pickle_obj_fpath(name), 'rb') as f:
        return pickle.load(f)


def get_survey_name_map():
    sdf = pd.read_excel(DATA_DIR + '/survey-names.xlsx', index_col=0)
    d = sdf['Survey Name'].to_dict()
    return collections.defaultdict(lambda: None, d)


def get_json_fpaths():
    jsons = [f for f in os.listdir(JSON_DIR) if f.endswith('.json')]
    jsons.sort()

    return [JSON_DIR + '/' + j for j in jsons]


def get_json_fpath(pattern=''):
    jsons = [f for f in os.listdir(JSON_DIR) if re.search(pattern, f) is not None and f.endswith('.json')]

    return JSON_DIR + '/' + jsons[0]


def get_validated_json_fpaths(scrape_status_csv_fname=SCRAPE_STATUS_CSV_FNAME):
    df = pd.read_csv(DATA_DIR + '/' + scrape_status_csv_fname)
    vdf = df[df['Validated?'].notnull()]
    validated = list(vdf['Filename (includes formtype)'])

    jsons = [f for f in get_json_fpaths() if any(v in f for v in validated)]

    return jsons


def load_clean_df(full=False, fpath=None):
    if fpath is None:
        fpath = CLEAN_LIGHT_FPATH
        if full:
            fpath = CLEAN_FULL_FPATH

    df = pd.read_csv(fpath, index_col=0)

    return df


if __name__ == '__main__':
    print('\n'.join(get_validated_json_fpaths()))
