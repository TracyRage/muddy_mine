from fastcore.utils import store_attr  # type: ignore
import pandas as pd  # type: ignore


class TabulateData:
    """Synopsis: TabulateData class is dedicated to conversion of
    jsonline to csv tables
    Input: jsonl files with extracted fields of interest
    Ouput: jsonl files corresponding csv tables"""
    def __init__(self, extract_meta: str, extract_pdf: str,
                 merged_tbl: str) -> None:
        store_attr('extract_meta,extract_pdf,merged_tbl')

    def read_jsonl(self, file):
        """Synopsis: Read extracted data in meta & pdf jsonl files"""
        return pd.read_json(file, lines=True)

    def merge_df(self, meta_df: pd.DataFrame,
                 pdf_df: pd.DataFrame) -> pd.DataFrame:
        """Synopsis: Merge metadata and pdf_parse data"""
        raw_df = meta_df.merge(pdf_df, on='s2orc_id', how='left')
        return raw_df.reindex(columns=[
            's2orc_id', 'title', 'abstract', 'text', 'authors', 'year', 'pmid',
            'doi'
        ])

    def write_table(self, merged_df: pd.DataFrame):
        """Synopsis: Write merged dataframe to a file"""
        merged_df.to_csv(self.merged_tbl, na_rep='N/A', index=False)
