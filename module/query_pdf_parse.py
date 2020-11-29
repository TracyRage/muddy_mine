from fastcore.utils import parallel, store_attr  # type: ignore
from typing import Generator, List
import click_spinner  # type: ignore
from pathlib import Path
import jmespath  # type: ignore
import jsonlines  # type: ignore
import gzip
import typer
import json


class GettingPDFs:
    """Class dedicated to the collection of the PMIDs, related
    to the papers which are mainly focused on mud volcanoes"""
    def __init__(self, input_file: str, archive_paths: str,
                 extracted_output: str) -> None:
        store_attr('input_file, extracted_output')
        self.archive_paths = Path(archive_paths).glob('**/*.gz')

    @property
    def open_input(self) -> List[str]:
        """Read S2ORC metadata jsonl file from previous S2ORC
        metadata scan"""
        with open(self.input_file) as f:
            articles = (json.loads(article) for article in f)
            papers_ids = [
                jmespath.search('paper_id', p_id) for p_id in articles
            ]
            return papers_ids

    def get_articles(self, ids_list: List[str]) -> List[Generator]:
        """Process each archive and extract aricles of
        interest based on paper_ids fetched from S2ORC metadata"""
        interests = [
            self._open_s2rc(str(archive), ids_list)
            for archive in self.archive_paths
        ]
        return interests

    def _get_art_list(self, article_generator: Generator) -> None:
        """Helper for parallel_process method (append articles
        metadata to a new jsonl file)"""
        final_list = list(article_generator)
        with jsonlines.open(self.extracted_output, 'a') as f:
            [f.write(article) for article in final_list]

    def parallel_process(self, interests_articles: List[Generator]) -> None:
        """Extract articles of inteteres from archives in parallel"""
        typer.secho('Working with archives (it could take a while): ',
                    bold=True)
        with click_spinner.spinner():
            parallel(self._get_art_list,
                     interests_articles,
                     threadpool=True,
                     n_workers=4)

    def _open_s2rc(self, archive, ids_list: List[str]) -> Generator:
        """Open individual S2ORC archive (pdf_parse)"""
        try:
            with gzip.open(archive) as f:
                articles = (json.loads(article) for article in f)
                for article in articles:
                    if jmespath.search('paper_id', article) in ids_list:
                        yield article
        except EOFError:
            header = typer.style("Invalid archive: ", bold=True)
            invalid_archive = typer.style(f"{archive}",
                                          fg=typer.colors.RED,
                                          bold=True)
            typer.echo(header + invalid_archive)


if __name__ == "__main__":
    input_file = '../analysis/mv_metadata.jsonl'
    archives = '../20200705v1/full/pdf_parses/'
    output_file = '../analysis/mv_pdf.jsonl'
    record = GettingPDFs(input_file, archives, output_file)
    ids = record.open_input
    articles_interest = record.get_articles(ids)
    record.parallel_process(articles_interest)
