from fastcore.utils import store_attr
from typing import Dict, Generator
import jmespath as jp  # type: ignore
import jsonlines as js  # type: ignore
import json


class ExtractInfo:
    def __init__(self, input_meta: str, input_pdf: str, output_meta: str,
                 output_pdf: str) -> None:
        store_attr('input_meta, input_pdf, output_meta, output_pdf')

    def read_jsonl(self, input_file):
        """Read jsonl files"""
        with open(input_file) as f:
            for article in f:
                yield json.loads(article)

    def extract_metadata(self,
                         articles: Generator) -> Generator[Dict, None, None]:
        """Extract metadata from mv_metadata"""
        for article in articles:
            yield {
                's2orc_id':
                self.fmt_output('paper_id').search(article),
                'title':
                self.fmt_output('title').search(article),
                'abstract':
                self.fmt_output('abstract').search(article),
                'authors':
                ' '.join(
                    self.fmt_output('authors[0].[first, last]').search(
                        article)),
                'year':
                self.fmt_output('year').search(article),
                'doi':
                self.fmt_output('doi').search(article),
                'pmid':
                self.fmt_output('pubmed_id').search(article),
            }

    def extract_body_text(self,
                          articles: Generator) -> Generator[Dict, None, None]:
        """Extract body text from mv_pdf"""
        for article in articles:
            yield {
                's2orc_id':
                self.fmt_output('paper_id').search(article),
                'text':
                ' '.join(self.fmt_output('body_text[*].text').search(article)),
            }

    def fmt_output(self, data):
        """Helper for extract_* methods"""
        return jp.compile(data)

    def write_to_files(self, data, output_file):
        """Write metadata and pdf_parse to files"""
        with js.open(output_file, 'a') as f:
            [f.write(article) for article in data]


if __name__ == "__main__":
    input_pdf = '../analysis/mv_pdf.jsonl'
    input_meta = '../analysis/mv_metadata.jsonl'
    output_meta = '../analysis/mv_meta_extracted.jsonl'
    output_pdf = '../analysis/mv_pdf_extracted.jsonl'
    record = ExtractInfo(input_meta, input_pdf, output_meta, output_pdf)
    articles_pdf = record.read_jsonl(record.input_pdf)
    body_text = record.extract_body_text(articles_pdf)
    articles_meta = record.read_jsonl(record.input_meta)
    meta_extracted = record.extract_metadata(articles_meta)
    body_extracted = record.extract_body_text(articles_pdf)
    write_meta = record.write_to_files(meta_extracted, output_meta)
    write_pdf = record.write_to_files(body_extracted, output_pdf)
