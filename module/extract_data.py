from fastcore.utils import store_attr  # type: ignore
from typing import Dict, Generator
import jmespath as jp  # type: ignore
import jsonlines as js  # type: ignore
import json
import typer


class ExtractInfo:
    """Synopsis: ExtractInfo class is dedicated to extraction of specific
    data fields from previously extracted S2ORC entries (metadata and pdf)"""
    def __init__(self, input_meta: str, input_pdf: str, output_meta: str,
                 output_pdf: str) -> None:
        store_attr('input_meta, input_pdf, output_meta, output_pdf')

    def read_jsonl(self, input_file):
        """Synopsis: Read jsonl files
        Input: jsonl files extracted by GettingPMID
        and GettingPDFs classes"""
        with open(input_file) as f:
            for article in f:
                yield json.loads(article)

    def extract_metadata(self,
                         articles: Generator) -> Generator[Dict, None, None]:
        """Synopsis: Extract specific data from S2ORC metadata jsonl files
        Fields of interest: paper_id, title, abstract,
        authors, year, doi, pubmed_id"""
        typer.secho('Extracting fields of interest from metadata jsonl',
                    bold=True)
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
        """Synopsis: Extract specific data from S2ORC pdf jsonl files
        Fields of interest: paper_id, body_text"""
        typer.secho('Extracting fields of interest from pdf parse jsonl',
                    bold=True)
        for article in articles:
            yield {
                's2orc_id':
                self.fmt_output('paper_id').search(article),
                'text':
                ' '.join(self.fmt_output('body_text[*].text').search(article)),
            }

    def fmt_output(self, data):
        """Dependecy: Helper for extract_* methods
        Synopsis: jmespath compiler"""
        return jp.compile(data)

    def write_to_files(self, data, output_file):
        """Synopsis: Write extracted fields of interest to files"""
        with js.open(output_file, 'a') as f:
            [f.write(article) for article in data]
