from module.mv_data_mine import ExtractData
from module.get_dict_terms import (SynChemDict, SynGeoDict, SynMudDict,
                                   SynMethodDict)
from fastcore.utils import compose
from typing import Dict, List
import pathlib
import pandas as pd

if __name__ == "__main__":
    path = 'analysis/merged_tbl.csv'
    mv_output = 'analysis/abstract_data/mv_data/abstract'
    taxa_output = 'analysis/abstract_data/taxonomic_data/abstract'

    # Init ExtractData class (dedicated to data mining)
    record = ExtractData(path, mv_output, taxa_output)

    # Init dataclasses w/ terminology to search for
    chemistry = SynChemDict().chemistry
    geology = SynGeoDict().geology
    mud_volcano = SynMudDict().mud
    methods = SynMethodDict().methods

    # Mine non-taxonomic data from abstract / article body
    def mine_data(level: str, terminology: Dict[str, List]):
        """Mine non-taxonomic data (Helper #1)"""
        table = record.read_table
        record.get_data(table, level)
        items = [
            record.get_mv_data(value, key)
            for key, value in terminology.items()
        ]
        s2orc_items = [record.map_s2orc_id(item) for item in items]
        s2orc_dfs = [record.to_df(s2orc_item) for s2orc_item in s2orc_items]
        return record.merge_dfs(*s2orc_dfs)

    def mine_taxonomy(taxa_rank: str, level: str, domain: str):
        """Mine taxonomic data (Helper #1)"""
        table = record.read_table
        record.get_data(table, level)
        taxa_dict = record.get_taxonomy(taxa_rank, domain)
        chain_function = compose(record.map_s2orc_id, record.to_df)
        return chain_function(taxa_dict)

    # Write to a file
    def write_data(df: pd.DataFrame, prefix: str, output_file: str):
        """Export mined dataframes to csv table (Helper #2)"""
        df.to_csv(pathlib.Path(output_file).with_name(prefix + ".csv"))

    # Combine mine_data & write_data functions
    def mining_pipeline(level: str, terminology: Dict[str, List],
                        file_name: str, output_file: str):
        """Mining function (main one)"""
        write_data(mine_data(level, terminology), file_name, output_file)

    # Extract physical / chemical data (abstract level)
    # mining_pipeline('abstract', chemistry, 'chemistry_abstract', mv_output)
    # mining_pipeline('abstract', geology, 'geology_abstract', mv_output)
    # mining_pipeline('abstract', mud_volcano, 'mv_abstract', mv_output)
    # mining_pipeline('abstract', methods, 'methods_abstract', mv_output)

    # Extract taxonomic data (abstract level)
    taxa_result = [
        # mine_taxonomy(taxa_rank='phylum', domain='Archaea', level='abstract'),
        mine_taxonomy(taxa_rank='class', domain='Archaea', level='abstract'),
        mine_taxonomy(taxa_rank='order', domain='Archaea', level='abstract'),
        mine_taxonomy(taxa_rank='family', domain='Archaea', level='abstract'),
        mine_taxonomy(taxa_rank='genus', domain='Archaea', level='abstract'),
        # mine_taxonomy(taxa_rank='species', domain='Archaea', level='abstract'),
    ]

    write_data(record.merge_dfs(*taxa_result), 'archaea_taxonomy_abstract',
               taxa_output)
