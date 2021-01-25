from module.query_metadata import GettingPMID
import argparse

if __name__ == "__main__":
    # Design parser
    parser = argparse.ArgumentParser(
        description="""Get PMIDs from Entrez and check
        them for S2ORC availability. Extract relevant
        articles from the S2ORC meta archives""")
    parser.add_argument('-e',
                        '--email',
                        metavar='',
                        required=True,
                        help='Provide your email address (for Entrez)')
    parser.add_argument('-a',
                        '--archives_path',
                        metavar='',
                        required=True,
                        help='Provide PATH to meta S2ORC archives')
    parser.add_argument('-o',
                        '--output_file',
                        metavar='',
                        required=True,
                        help='Provide jsonl output FILE PATH')
    parser.add_argument('-q',
                        '--entrez_query',
                        metavar='',
                        required=False,
                        help='Provide Entrez search query')
    args = parser.parse_args()

    # Pipeline per se
    # Init GettingPMID class
    entrez = GettingPMID(args.email, args.archives_path, args.output_file,
                         args.entrez_query)
    # Get PMIDs from Pubmed
    pmids = entrez.get_pmid
    # Search for articles of interest in S2ORC meta archives
    interest = entrez.get_articles(pmids)
    final_result = entrez.parallel_process(interest)
