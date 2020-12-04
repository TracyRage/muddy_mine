from .mv_data_mine import ExtractData  # type: ignore
from .get_dict_terms import SynChemDict, SynGeoDict  # type: ignore
from .get_dict_terms import SynMudDict, SynMethodDict  # type: ignore
from fastcore.utils import compose, store_attr  # type: ignore
from typing import Dict, List
import pathlib  # type: ignore
import pandas as pd  # type: ignore


class MineData:
    """Synopsis: MineData class is dedicated to data mining
    Input: input table with all the relevant texts (abstracts/body texts)
    Output: csv tables with all the mined data"""
    def __init__(self, input_table: str, mv_out: str, taxa_out: str) -> None:
        store_attr('input_table, mv_out, taxa_out')

    @property
    def load_mining(self) -> None:
        """Synopsis: Init ExtractData class to prepare mining methods"""
        self.record = ExtractData(self.input_table, self.mv_out, self.taxa_out)
        # Init dataclasses w/ terminology to search for
        self.chemistry = SynChemDict().chemistry
        self.geology = SynGeoDict().geology
        self.mud_volcano = SynMudDict().mud
        self.methods = SynMethodDict().methods

    def mine_data(self, level: str, terminology: Dict[str,
                                                      List]) -> pd.DataFrame:
        """Dependency: Helper for mining_pipeline method
        Synopsis: Mine non-taxonomic data"""
        # Read table with text
        table = self.record.read_table
        # Get abstract or whole article to analyze
        self.record.get_data(table, level)
        # Extract mud volcano specific data
        items = [
            self.record.get_mv_data(value, key)
            for key, value in terminology.items()
        ]
        # Map found dict to s2orc ids
        s2orc_items = [self.record.map_s2orc_id(item) for item in items]
        # Transform dicts to dataframes and merge them all
        s2orc_dfs = [
            self.record.to_df(s2orc_item) for s2orc_item in s2orc_items
        ]
        return self.record.merge_dfs(*s2orc_dfs)

    def mine_taxonomy(self, taxa_rank: str, level: str,
                      domain: str) -> pd.DataFrame:
        """Dependency: Helper for mine_taxonomic_data methods
        Synopsis: Mine taxonomic data"""
        # Read table with text
        table = self.record.read_table
        # Get abstract or whole article to analyze
        self.record.get_data(table, level)
        # Mine taxonomy
        taxa_dict = self.record.get_taxonomy(taxa_rank, domain)
        # Map to s2orc ids and convert to dataframes
        chain_function = compose(self.record.map_s2orc_id, self.record.to_df)
        return chain_function(taxa_dict)

    # Write to a file
    def write_data(self, df: pd.DataFrame, prefix: str, output_file: str):
        """Dependency: Helper for mining_pipeline and mine_taxonomic_data methods
        Synopsis: Export mined dataframes to csv table"""
        df.to_csv(pathlib.Path(output_file).with_name(prefix + ".csv"))

    # Combine mine_data & write_data functions
    def mining_pipeline(self, level: str, terminology: Dict[str, List],
                        file_name: str, output_file: str):
        """Dependency: Helper for mine_chemical_data method"""
        self.write_data(self.mine_data(level, terminology), file_name,
                        output_file)

    def mine_chemical_data(self, text_type: str):
        """Synopsis: Mine chemical & mud volcano relevant data"""
        self.mining_pipeline(text_type, self.chemistry, 'chemistry_abstract',
                             self.mv_out)
        self.mining_pipeline(text_type, self.geology, 'geology_abstract',
                             self.mv_out)
        self.mining_pipeline(text_type, self.mud_volcano, 'mv_abstract',
                             self.mv_out)
        self.mining_pipeline(text_type, self.methods, 'methods_abstract',
                             self.mv_out)

    def mine_taxonomic_data(self, text_type: str, org_domain: str,
                            type_prefix: str):
        """Synopsis: Mine taxonomic data; domain Archaea or Bacteria and
        write to csv tables"""
        # Mine taxonomic data and convert to list of dataframes
        taxa_result = [
            self.mine_taxonomy(taxa_rank='phylum',
                               domain=org_domain,
                               level=text_type),
            self.mine_taxonomy(taxa_rank='class',
                               domain=org_domain,
                               level=text_type),
            self.mine_taxonomy(taxa_rank='order',
                               domain=org_domain,
                               level=text_type),
            self.mine_taxonomy(taxa_rank='family',
                               domain=org_domain,
                               level=text_type),
            self.mine_taxonomy(taxa_rank='genus',
                               domain=org_domain,
                               level=text_type),
            self.mine_taxonomy(taxa_rank='species',
                               domain=org_domain,
                               level=text_type)
        ]
        # Write dataframes to file
        self.write_data(self.record.merge_dfs(*taxa_result), type_prefix,
                        self.taxa_out)
