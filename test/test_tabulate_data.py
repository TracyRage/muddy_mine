import pandas as pd
import pytest


def test_merge_df(cls_tabulate, tab_df_1, tab_df_2, tab_df_merged):
    result = cls_tabulate.merge_df(tab_df_1, tab_df_2)
    pd.testing.assert_frame_equal(result, tab_df_merged)


def test_merge_df_2(cls_tabulate, tab_df_1):
    with pytest.raises(ValueError):
        assert cls_tabulate.merge_df(tab_df_1, tab_df_1)
