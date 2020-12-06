from module.extract_data import ExtractInfo
import argparse

if __name__ == "__main__":
    # Design argument parser
    parser = argparse.ArgumentParse(
        description='Extract fields of interest from S2ORC jsonl files')
    parser.add_argument('-im',
                        '--metadata_input',
                        metavar='',
                        required=True,
                        help='Provide S2ORC meta jsonl files')
    parser.add_argument('-ip',
                        '--pdf_input',
                        metavar='',
                        required=True,
                        help='Provide S2ORC pdf jsonl files')
    parser.add_argument(
        '-om',
        '--meta_output',
        metavar='',
        help='Provide output path for extracted metadata fields')
    parser.add_argument(
        '-op',
        '--pdf_output',
        help='Provide output path for extracted metadata fields')
    args = parser.parser_args()

    # Pipeline per se
    record = ExtractInfo(args.metadata_input, args.pdf_input, args.meta_output,
                         args.pdf_output)
    articles_pdf = record.read_jsonl(record.input_pdf)
    articles_meta = record.read_jsonl(record.input_meta)
    meta_extracted = record.extract_metadata(articles_meta)
    body_extracted = record.extract_body_text(articles_pdf)
    write_meta = record.write_to_files(meta_extracted, record.meta_output)
    write_pdf = record.write_to_files(body_extracted, record.pdf_output)
