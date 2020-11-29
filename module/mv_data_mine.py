from typing import List, Dict, Generator
from functools import reduce
from collections import Counter
from .get_dict_terms import SynTaxaDict
from fastcore.utils import store_attr  # type: ignore
from numpy import nan as NA  # type: ignore
import typer  # type: ignore
import pandas as pd  # type: ignore
import spacy  # type: ignore


class ExtractData:
    """Class dedicated to taxonomic and mud volcano data mining"""
    def __init__(
        self,
        input_table: str,
        mv_output: str,
        taxa_output: str,
        core_model: str = "en_core_sci_sm",
    ) -> None:
        store_attr("input_table, mv_output, taxa_output, core_model")

    @property
    def read_table(self) -> pd.DataFrame:
        """Read input table"""
        raw_table: pd.DataFrame = pd.read_csv(self.input_table)
        return raw_table

    def get_data(self, raw_table, query: str):
        """Read article text (abstract or body text)"""
        message_start = typer.style('Query level: ', bold=True)
        query_level = typer.style(query,
                                  blink=True,
                                  fg=typer.colors.GREEN,
                                  bold=True)
        typer.echo(message_start + query_level)
        data_to_analyze = raw_table[[query, "s2orc_id"]].dropna()
        self.texts, self.s2orc_ids = (
            list(data_to_analyze[query]),
            list(data_to_analyze["s2orc_id"]),
        )
        return self.texts, self.s2orc_ids

    def get_taxonomy(
            self, taxa_rank: str,
            domain: str) -> Generator[Dict[str, List[str]], None, None]:
        """Mine taxonomic data from selected texts"""
        start = typer.style('Extracting taxonomy: ', bold=True)
        taxa_message = typer.style(taxa_rank,
                                   blink=True,
                                   fg=typer.colors.GREEN,
                                   bold=True)
        typer.echo(start + taxa_message)
        for text in self.texts[:60]:
            yield self._build_dict(self._extract_taxa(text, taxa_rank, domain),
                                   taxa_rank)

    def get_mv_data(
            self, terminology_list: List[str],
            dict_key: str) -> Generator[Dict[str, List[str]], None, None]:
        """Mine mud volcano data from selected texts"""
        start = typer.style('Extracting mud volcano data: ', bold=True)
        data_message = typer.style(dict_key,
                                   fg=typer.colors.GREEN,
                                   bold=True,
                                   blink=True)
        typer.echo(start + data_message)
        for text in self.texts:
            yield self._build_dict(
                self._extract_mv_data(text, terminology_list), dict_key)

    def _extract_taxa(self, text: str, taxa_rank: str,
                      domain: str) -> List[str]:
        """Extract TAXON tokens from selected texts"""
        tax_class = SynTaxaDict().taxonomy.get('tax')
        taxonomy = tax_class.get_descendants(domain, taxa_rank)
        nlp = spacy.load(self.core_model)
        doc = nlp(text)
        return [
            token.text for token in doc
            if token.text != 'bacterium' and token.text in taxonomy
        ]

    def _extract_mv_data(self, text: str, data_list: List[str]) -> List[str]:
        """Extract tokens from selected texts"""
        nlp = spacy.load(self.core_model)
        doc = nlp(text)
        return [token.text for token in doc if token.text.lower() in data_list]

    def _build_dict(self, data_list: List[str],
                    taxa_rank: str) -> Dict[str, List[str]]:
        """Map extracted tokens to dicts"""
        new_dict = dict()
        if data_list != []:
            taxa_count = Counter(data_list)
            new_dict[taxa_rank] = [
                f"{key} ({values})" for key, values in taxa_count.items()
            ]
            return new_dict
        else:
            new_dict[taxa_rank] = None
            return new_dict

    def map_s2orc_id(
            self,
            mapped_dicts: Dict[str,
                               List[str]]) -> Dict[str, Dict[str, List[str]]]:
        """Map S2ORC id to mapped_dict"""
        return {
            s2_id: mapped_dict
            for s2_id, mapped_dict in zip(self.s2orc_ids, mapped_dicts)
        }

    def to_df(
        self, final_dict: Dict[str, Dict[str, List[str]]]
    ) -> Dict[str, Dict[str, List[str]]]:
        """Write mapped dict to a dataframe"""
        df = pd.DataFrame.from_dict(final_dict, orient='index')
        return df.rename_axis('s2orc_id').reset_index().replace(NA, '-')

    def merge_dfs(self, *args: pd.DataFrame) -> pd.DataFrame:
        """Merge multiple dfs on s2orc_id column"""
        return reduce(
            lambda left, right: pd.merge(
                left, right, on='s2orc_id', how='outer'), [*args]).fillna('-')
