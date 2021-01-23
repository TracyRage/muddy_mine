from module.query_pdf import GettingPDFs
import argparse

if __name__ == "__main__":
    # Design arguments parser
    parser = argparse.ArgumentParser(
        description="Get pdf entries from S2ORC pdf archives")
    parser.add_argument('-i',
                        '--metadata_input',
                        metavar='',
                        required=True,
                        help='Provide path of extracted metadata jsonl file')
    parser.add_argument('-a',
                        '--pdf_archives',
                        metavar='',
                        required=True,
                        help='Provide path to jsonl S2ORC pdf archives')
    parser.add_argument(
        '-o',
        '--output_file',
        required=True,
        help='Provide path for jsonl file with  extracted S2ORC pdf entries')
    args = parser.parse_args()

    # Pipeline per se
    record = GettingPDFs(args.metadata_input, args.pdf_archives,
                         args.output_file)
    ids = record.open_input
    articles_interest = record.get_articles(ids)
    record.parallel_process(articles_interest)
