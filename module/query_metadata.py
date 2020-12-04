from fastcore.utils import store_attr, parallel  # type: ignore
from typing import Generator, List
import click_spinner  # type: ignore
from pathlib import Path
from Bio import Entrez  # type: ignore
import jmespath  # type: ignore
import jsonlines  # type: ignore
import gzip
import typer
import json


class GettingPMID:
    """Synopsis: GettingPMID class is dedicated to the collection of the
    PMIDs (from Entrez) related to the papers which are mainly focused
    on mud volcanoes (default value)"""
    def __init__(self,
                 email: str,
                 archive_paths: str,
                 extracted_output: str,
                 query: str = 'mud[TIAB] AND volcano[TIAB]') -> None:
        store_attr('email, query')
        self.archive_paths = Path(archive_paths).glob('**/*.gz')
        self.extracted_output = Path(extracted_output)

    @property
    def get_pmid(self) -> List[str]:
        """Synopsis: Fetch PMIDs of mud volcano articles (from Entrez)
        Input: Pubmed query string e.g. mud[TIAB] AND volcano[TIAB]
        Output: List of PMIDs"""
        # Header comment
        typer.secho('Getting PMIDs of iterest', bold=True)
        header_1 = typer.style("Query: ", bold=True)
        query = typer.style(f"{self.query}")
        typer.echo(header_1 + query)
        # Function per se
        Entrez.email = self.email
        with Entrez.esearch(db='pubmed',
                            term=self.query,
                            idtype='acc',
                            retmax=1000) as f:
            record = Entrez.read(f)
            pmids = record.get('IdList')
            header_2 = typer.style("PMIDs #: ", bold=True)
            pmids_text = typer.style(f"{len(pmids)}",
                                     blink=True,
                                     fg=typer.colors.GREEN,
                                     bold=True)
            # Conclusion
            typer.echo(header_2 + pmids_text)
            return pmids

    def get_articles(self, pmid_list: List[str]) -> List[Generator]:
        """Synopsis: Process each  S2ORC archive and extract aricles of
        interest based on PMIDs fetched from Pubmed
        Input: List of PMIDs
        Output: Get articles from metadata S2ORC archives"""
        interests = [
            self._open_s2rc(str(archive), pmid_list)
            for archive in self.archive_paths
        ]
        return interests

    def _get_art_list(self, article_generator: Generator) -> None:
        """Dependency: Helper for parallel_process method
        Synopsis: Append articles metadata to a new jsonl file"""
        final_list = list(article_generator)
        with jsonlines.open(str(self.extracted_output), 'a') as f:
            [f.write(article) for article in final_list]

    def parallel_process(self, interests_articles: List[Generator]):
        """Synopsis: Extract articles of inteteres from archives in parallel"""
        typer.secho('Working with archives (it could take a while): ',
                    bold=True)
        with click_spinner.spinner():
            parallel(self._get_art_list,
                     interests_articles,
                     threadpool=True,
                     n_workers=4)

    def _open_s2rc(self, archive, pmid_list: List[str]) -> Generator:
        """Dependency: Helper for get method
        Synopsis: Open individual S2ORC archive metadata
        """
        try:
            with gzip.open(archive) as f:
                articles = (json.loads(article) for article in f)
                for article in articles:
                    if jmespath.search('pubmed_id', article) in pmid_list:
                        yield article
        except EOFError:
            header = typer.style("Invalid archive: ", bold=True)
            invalid_archive = typer.style(f"{archive}",
                                          fg=typer.colors.RED,
                                          bold=True)
            typer.echo(header + invalid_archive)
