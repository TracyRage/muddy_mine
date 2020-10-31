from fastcore.utils import store_attr, parallel  # type: ignore
from typing import Generator, List, Dict
import itertools
from tqdm import tqdm  # type: ignore
from pathlib import Path
from Bio import Entrez  # type: ignore
import jmespath  # type: ignore
import jsonlines  # type: ignore
import gzip
import typer
import json


class GettingPMID:
    """Class dedicated to the collection of the PMIDs, related
    to the papers which are mainly focused on mud volcanoes"""
    def __init__(self,
                 email: str,
                 query: str = 'mud[TIAB] AND volcano[TIAB]') -> None:
        store_attr('email, query')

    @property
    def get_pmid(self):
        """Fetch PMIDs of mud volcano articles"""
        # Header comment
        typer.secho('Getting PMIDs of iterest', bold=True)
        header_1 = typer.style("Query: ", bold=True)
        query = typer.style(f"{self.query}")
        typer.echo(header_1 + query)
        # Function per se
        Entrez.email: str = self.email
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


class Opens2orcMetadata:
    """Class dedicated to S2ORC  metadata database
    basic manupulations (open, filter, etc.)"""
    def __init__(self, archive_paths: str,
                 extracted_articles_file: str) -> None:
        self.archive_paths = Path(archive_paths).glob('**/*.gz')
        self.extracted_articles_file = Path(extracted_articles_file)

    def get_articles(self, pmid_list: List[str]) -> List[Generator]:
        """Process each archive and extract aricles of
        interest based on PMIDs fetched from Pubmed"""
        interests = [
            self._open_s2rc(str(archive), pmid_list)
            for archive in self.archive_paths
        ]
        return interests

    def get_list(self, articles_interest: List[Generator]) -> List[Dict]:
        """Extract articles of interest, and make a list of them"""
        typer.secho('Processing archives: ', bold=True)
        final_list = [list(articles) for articles in tqdm(articles_interest)]
        flat_list = list(itertools.chain(*final_list))
        text_1 = typer.style('Articles found in S2ORC: ', bold=True)
        text_2 = typer.style(f"{len(flat_list)}",
                             blink=True,
                             fg=typer.colors.GREEN,
                             bold=True)
        typer.echo(text_1 + text_2)
        return flat_list

    def write_to_file(self, extracted_articles: List[Dict]) -> None:
        """Write S2ORC extracted articles to a jsonl file"""
        text_1 = typer.style('Writting to a file: ', bold=True)
        text_2 = typer.style(f'{str(self.extracted_articles_file)}',
                             fg=typer.colors.GREEN,
                             bold=True)
        typer.echo(text_1 + text_2)

        with jsonlines.open(str(self.extracted_articles_file), 'a') as f:
            [f.write(article) for article in extracted_articles]
            typer.secho('Done', bold=True, fg=typer.colors.GREEN, blink=True)

    def _open_s2rc(self, archive, pmid_list: List[str]) -> Generator:
        """Open individual S2ORC archive (metadata)"""
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


if __name__ == "__main__":
    email = 'alexei@remizovschi.com'
    archive = '../20200705v1/full/metadata/'
    output_file = '../analysis/mv_metadata.jsonl'
    entrez = GettingPMID(email)
    pmids = entrez.get_pmid
    record = Opens2orcMetadata(archive, output_file)
    interest = record.get_articles(pmids)
    final_result = record.get_list(interest)
    record.write_to_file(final_result)
