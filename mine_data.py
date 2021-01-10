from module.mine_data_pipeline import MineData
import argparse

if __name__ == "__main__":
    # Design parser
    parser = argparse.ArgumentParser(
        description='Mine data from S2ORC archives')
    parser.add_argument('-it',
                        '--input_table',
                        metavar='',
                        required=True,
                        help='Provide table with texts to mine')
    parser.add_argument('-mv',
                        '--output_mv',
                        metavar='',
                        required=True,
                        help='Provide output for mud volcano specific data')
    parser.add_argument('-taxa',
                        '--output_taxa',
                        metavar='',
                        required=True,
                        help='Provide output for taxonomic specific data')
    args = parser.parse_args()

    # Init MineData class (dedicated to data mining)
    record = MineData(args.input_table, args.output_mv, args.output_taxa)

    # Init terminology dataclasses
    record.load_mining

    # Mine abstract chemical data
    record.mine_chemical_data('abstract')

    # Mine abstract Bacterial and Archaea data
    record.mine_taxonomic_data('abstract', 'Bacteria', 'abs_bacteria')
    record.mine_taxonomic_data('abstract', 'Archaea', 'abs_archaea')

    # Mine article chemical data
    # record.mine_chemical_data('text')

    # Mine article Bacterial and Archaea data
    # record.mine_taxonomic_data('text', 'Bacteria', 'art_bacteria')
    # record.mine_taxonomic_data('text', 'Archaea', 'art_archaea')
