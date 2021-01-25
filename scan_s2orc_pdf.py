from module.query_pdf import GettingPDFs
import argparse

if __name__ == "__main__":
    # Design arguments parser
    parser = argparse.ArgumentParser(description="""Get pdf entries of interest
        from the S2ORC pdf_parse archives""")
    parser.add_argument('-i',
                        '--metadata_input',
                        metavar='',
                        required=True,
                        help='Provide metadata jsonl FILE')
    parser.add_argument('-a',
                        '--pdf_archives',
                        metavar='',
                        required=True,
                        help='Provide PATH to S2ORC pdf_parse archives')
    parser.add_argument('-o',
                        '--output_file',
                        required=True,
                        help="""Provide PATH for jsonl file with
        the extracted S2ORC pdf_parse entries""")
    args = parser.parse_args()

    # Pipeline per se
    # Init GettingPDFs class
    record = GettingPDFs(args.metadata_input, args.pdf_archives,
                         args.output_file)
    # Get paper_ids from metadata jsonl file
    ids = record.open_input
    # Extract pdf_parse entries
    articles_interest = record.get_articles(ids)
    record.parallel_process(articles_interest)
