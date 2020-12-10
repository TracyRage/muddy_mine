from hypothesis import given, strategies as st
from typing import List
import pytest


@given(data_list=st.from_type(List[str]), taxa_rank=st.characters())
def test_build_dict(cls_mv_data_mine, data_list, taxa_rank):
    output_dict = cls_mv_data_mine._build_dict(data_list, taxa_rank)
    assert isinstance(output_dict, dict)


@pytest.mark.parametrize('text_type', ['abstract', 'text'])
def test_mv_data_mine(cls_mv_data_mine, tab_df_merged, text_type):
    texts, pmids = cls_mv_data_mine.get_data(tab_df_merged, text_type)
    assert isinstance(texts, list)


@pytest.mark.parametrize('text_type', ['abstract', 'text'])
def test_mv_data_mine_2(cls_mv_data_mine, tab_df_merged, text_type):
    texts, pmids = cls_mv_data_mine.get_data(tab_df_merged, text_type)
    assert isinstance(pmids, list)


@pytest.mark.parametrize('text_type', ['abstract', 'text'])
def test_mv_data_mine_3(cls_mv_data_mine, tab_df_merged, text_type):
    texts, pmids = cls_mv_data_mine.get_data(tab_df_merged, text_type)
    assert isinstance(texts[0], str)


@pytest.mark.parametrize('text_type', ['abstract', 'text'])
def test_mv_data_mine_4(cls_mv_data_mine, tab_df_merged, text_type):
    texts, pmids = cls_mv_data_mine.get_data(tab_df_merged, text_type)
    assert isinstance(pmids[0], int)
