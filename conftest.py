from module.tabulate_data import TabulateData
from module.mv_data_mine import ExtractData
from hypothesis import strategies as st
from pytest import fixture
import pandas as pd


@fixture(scope='module')
def cls_tabulate():
    return TabulateData(
        st.characters(),
        st.characters(),
        st.characters(),
    )


@fixture(scope='module')
def cls_mv_data_mine():
    return ExtractData(
        st.characters(),
        st.characters(),
        st.characters(),
        st.characters(),
    )


@fixture(scope='module')
def tab_df_1():
    return pd.DataFrame({
        's2orc_id': [1, 2, 3],
        'title': ['t1', 't2', 't3'],
        'abstract': ['a1', 'a2', 'a3'],
        'authors': ['au1', 'au2', 'au3'],
        'year': [1970, 1980, 2010],
        'pmid': [2344, 4532, 5634],
        'doi': ['doi1', 'doi2', 'doi3']
    })


@fixture(scope='module')
def tab_df_2():
    return pd.DataFrame({
        's2orc_id': [1, 2, 3],
        'text': ['txt1', 'txt2', 'txt3'],
    })


@fixture(scope='module')
def tab_df_merged():
    return pd.DataFrame({
        's2orc_id': [1, 2, 3],
        'title': ['t1', 't2', 't3'],
        'abstract': ['a1', 'a2', 'a3'],
        'text': ['txt1', 'txt2', 'txt3'],
        'authors': ['au1', 'au2', 'au3'],
        'year': [1970, 1980, 2010],
        'pmid': [2344, 4532, 5634],
        'doi': ['doi1', 'doi2', 'doi3']
    })
