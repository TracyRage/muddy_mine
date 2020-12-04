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
    """Synopsis: GettingPDFs class is dedicated to the collection
    of the entries from S2ORC pdf archives based on S2ORC ids"""
    def __init__(self, input_file: str, archive_paths: str,
                 extracted_output: str) -> None:
        store_attr('input_file, extracted_output')
        self.archive_paths = Path(archive_paths).glob('**/*.gz')

    @property
    def open_input(self) -> List[str]:
        """Synopsis: Read S2ORC metadata jsonl file from previous S2ORC
        metadata scan
        Input: jsonl file with all the metadata extracted from S2ORC metadata
        archives which are related to your query of interest (mud volcano)
        Output: List with all the relevant S2ORC ids"""
        with open(self.input_file) as f:
            articles = (json.loads(article) for article in f)
            papers_ids = [
                jmespath.search('paper_id', p_id) for p_id in articles
            ]
            return papers_ids

    def get_articles(self, ids_list: List[str]) -> List[Generator]:
        """Synopsis: Process each S2ORC pdf archive and extract
        entries of interest based on S2ORC ids fetched from
        S2ORC metadata
        Input: List of S2ORC ids
        Output: List of generators which contain S2ORC pdf entries"""
        typer.secho('Extracting pdf entries from S2ORC', bold=True)
        first = typer.style('Number of s2orc ids to search for', bold=True)
        second = typer.style(f"{len(ids_list)}",
                             blink=True,
                             fg=typer.colors.GREEN,
                             bold=True)
        typer.echo(first + second)
        interests = [
            self._open_s2rc(str(archive), ids_list)
            for archive in self.archive_paths
        ]
        return interests

    def _get_art_list(self, article_generator: Generator) -> None:
        """Dependency: Helper for parallel_process method
        Synopsis: Append articles pdf data to a new jsonl file"""
        final_list = list(article_generator)
        with jsonlines.open(self.extracted_output, 'a') as f:
            [f.write(article) for article in final_list]

    def parallel_process(self, interests_articles: List[Generator]) -> None:
        """Synopsis: Extract pdf entries of interest
        from S2ORC pdf archives in parallel"""
        typer.secho('Working with archives (it could take a while): ',
                    bold=True)
        with click_spinner.spinner():
            parallel(self._get_art_list,
                     interests_articles,
                     threadpool=True,
                     n_workers=4)

    def _open_s2rc(self, archive, ids_list: List[str]) -> Generator:
        """Dependency: Helper for get_articles method
        Synopsis: Open individual S2ORC pdf archive"""
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
