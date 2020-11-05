from fastcore.utils import store_attr
import pandas as pd


class TabulateData:
    """Class dedicated to conversion of
    jsonline to csv tables"""
    def __init__(self, extract_meta: str, extract_pdf: str,
                 merged_tbl: str) -> None:
        store_attr('extract_meta,extract_pdf,merged_tbl')

    def read_jsonl(self, file):
        """Read extracted data in meta & pdf jsonl files"""
        return pd.read_json(file, lines=True)

    def merge_df(self, meta_df, pdf_df):
        """Merge metadata and pdf_parse data"""
        raw_df = meta_df.merge(pdf_df, on='s2orc_id', how='left')
        return raw_df.reindex(columns=[
            's2orc_id', 'title', 'abstract', 'text', 'authors', 'year', 'pmid',
            'doi'
        ])

    def write_table(self, merged_df):
        """Write merged dataframe to a file"""
        merged_df.to_csv(self.merged_tbl, na_rep='N/A', index=False)


if __name__ == "__main__":
    ext_meta = '../analysis/mv_meta_extracted.jsonl'
    ext_pdf = '../analysis/mv_pdf_extracted.jsonl'
    tbl_merged = '../analysis/merged_tbl.csv'
    record = TabulateData(ext_meta, ext_pdf, tbl_merged)
    pdf_data = record.read_jsonl(record.extract_pdf)
    tbl_meta = record.read_jsonl(record.extract_meta)
    merged_tb = record.merge_df(tbl_meta, pdf_data)
    record.write_table(merged_tb)
