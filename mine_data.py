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
                        help='Provide csv table with texts to mine')
    parser.add_argument(
        '-mv',
        '--output_mv',
        metavar='',
        required=True,
        help='Provide output  PATH for mud volcano specific data table')
    parser.add_argument(
        '-taxa',
        '--output_taxa',
        metavar='',
        required=True,
        help='Provide output PATH for taxonomic specific data table')
    args = parser.parse_args()

    # Init MineData class (dedicated to data mining)
    record = MineData(args.input_table, args.output_mv, args.output_taxa)

    # Init terminology dataclasses
    record.load_mining

    # Mine article chemical data
    record.mine_chemical_data('text')

    # Mine article Bacterial and Archaea data
    record.mine_taxonomic_data('text', 'Bacteria', 'art_bacteria')
    record.mine_taxonomic_data('text', 'Archaea', 'art_archaea')

    # UNCOMMENT THE LINES BELOW IF YOU WANT TO EXTRACT INFO FROM THE ABSTRACTS

    # Mine abstract chemical data
    # record.mine_chemical_data('abstract')

    # Mine abstract Bacterial and Archaea data
    # record.mine_taxonomic_data('abstract', 'Bacteria', 'abs_bacteria')
    # record.mine_taxonomic_data('abstract', 'Archaea', 'abs_archaea')
