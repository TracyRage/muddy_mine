from module.query_metadata import GettingPMID
import argparse

if __name__ == "__main__":
    # Design parser
    parser = argparse.ArgumentParser(
        description="""Get PMIDs from Entrez and check
        them for S2ORC availability. Extract relevant 
        articles from S2ORC meta""")
    parser.add_argument('-e',
                        '--email',
                        metavar='',
                        required=True,
                        help='Provide your email address')
    parser.add_argument('-a',
                        '--archives_path',
                        metavar='',
                        required=True,
                        help='Provide archives paths')
    parser.add_argument('-o',
                        '--output_file',
                        metavar='',
                        required=True,
                        help='Provide jsonl output file')
    parser.add_argument('-q',
                        '--entrez_query',
                        metavar='',
                        required=False,
                        help='Provide entrez search query')
    args = parser.parse_args()

    # Pipeline per se
    entrez = GettingPMID(args.email, args.archives_path, args.output_file,
                         args.entrez_query)
    pmids = entrez.get_pmid
    interest = entrez.get_articles(pmids)
    final_result = entrez.parallel_process(interest)
