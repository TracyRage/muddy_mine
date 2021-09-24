from typing import List, Dict, Generator, Any
from functools import reduce
from collections import Counter
from .get_dict_terms import SynTaxaDict  # tope: ignore
from fastcore.utils import store_attr  # type: ignore
from numpy import nan as NA  # type: ignore
import typer  # type: ignore
import pandas as pd  # type: ignore
import spacy  # type: ignore


class ExtractData:
    """Synopsis: ExtractData class is dedicated to taxonomic
    and mud volcano data mining
    Input: merged csv table with all the relevant S2ORC fields of interest
    Output: csv tables with all the MINED BIOLOGICAL, CHEMICAL
    and GEOLOGICAL data"""
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
        """Synopsis: Read merged input table with all the relevant fields
        of interest"""
        raw_table: pd.DataFrame = pd.read_csv(self.input_table)
        return raw_table

    def get_data(self, raw_table: pd.DataFrame, query: str):
        """Synopsis: Read text (abstract or body text)
        Input: dataframe with all the relevant fields of interest
        Output: Two lists of (1) abstracts / body text 
        and (2) s2orc ids, respectively"""
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
        """Synopsis: Mine taxonomic data from the selected texts
        Output: Generator of dicts 
        '{taxonomic_rank: taxonomy_data (# times mentioned)}"""
        start = typer.style('Extracting taxonomy: ', bold=True)
        taxa_message = typer.style(taxa_rank,
                                   blink=True,
                                   fg=typer.colors.GREEN,
                                   bold=True)
        typer.echo(start + taxa_message)
        for text in self.texts:
            yield self._build_dict(self._extract_taxa(text, taxa_rank, domain),
                                   taxa_rank)

    def get_mv_data(
            self, terminology_list: List[str],
            dict_key: str) -> Generator[Dict[str, List[str]], None, None]:
        """Synopsis: Mine mud volcano data (chemical / geological / other)
        from selected texts
        Output: Generator of dicts
        '{data_category: mud_volcano_data (# times mentioned)}'"""
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
        """Dependency: Helper get_taxonomy method
        Synopsis: Extract TAXON tokens from selected texts"""
        tax_class = SynTaxaDict().taxonomy.get('tax')
        taxonomy = tax_class.get_descendants(domain, taxa_rank)
        nlp = spacy.load(self.core_model)
        doc = nlp(text)
        return [
            token.text for token in doc
            if token.text != 'bacterium' and token.text in taxonomy
        ]

    def _extract_mv_data(self, text: str, data_list: List[str]) -> List[str]:
        """Dependency: Helper get_mv_data method
        Synopsis: Extract relevant tokens from selected texts"""
        nlp = spacy.load(self.core_model)
        doc = nlp(text)
        return [token.text.lower() for token in doc if token.text.lower() in data_list]

    def _build_dict(self, data_list: List[str],
                    taxa_rank: str) -> Dict[str, List[str]]:
        """Dependency: Helper for get_taxonomy and get_mv_data
        Synopsis: Map extracted tokens to dicts"""
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

    def map_s2orc_id(self, mapped_dicts: Dict[str,
                                              List[str]]) -> Dict[str, Any]:
        """Synopsis: Map S2ORC ids to the extracted token dicts
        Input: get_taxonomy and get_mv_data output dicts
        Output: Dict '{s2orc_id: token_dict}'"""
        return {
            s2_id: mapped_dict
            for s2_id, mapped_dict in zip(self.s2orc_ids, mapped_dicts)
        }

    def to_df(
        self, final_dict: Dict[str, Dict[str, List[str]]]
    ) -> Dict[str, Dict[str, List[str]]]:
        """Synopsis: Write mapped dicts to a dataframes"""
        df = pd.DataFrame.from_dict(final_dict, orient='index')
        return df.rename_axis('s2orc_id').reset_index().replace(NA, '-')

    def merge_dfs(self, *args: pd.DataFrame) -> pd.DataFrame:
        """Synopsis: Merge multiple dfs on s2orc_id column"""
        return reduce(
            lambda left, right: pd.merge(
                left, right, on='s2orc_id', how='outer'), [*args]).fillna('-')
