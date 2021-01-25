from module.extract_data import ExtractInfo
import argparse

if __name__ == "__main__":
    # Design argument parser
    parser = argparse.ArgumentParser(
        description='Extract fields of interest from the S2ORC jsonl files')
    parser.add_argument('-im',
                        '--metadata_input',
                        metavar='',
                        required=True,
                        help='Provide S2ORC meta jsonl FILE')
    parser.add_argument('-ip',
                        '--pdf_input',
                        metavar='',
                        required=True,
                        help='Provide S2ORC pdf jsonl FILE')
    parser.add_argument(
        '-om',
        '--meta_output',
        metavar='',
        help='Provide output FILE PATH for the extracted metadata fields')
    parser.add_argument(
        '-op',
        '--pdf_output',
        help='Provide output FILE PATH for the extracted metadata fields')
    args = parser.parse_args()

    # Pipeline per se
    # Init ExtractInfo class
    record = ExtractInfo(args.metadata_input, args.pdf_input, args.meta_output,
                         args.pdf_output)
    # Read metadata jsonl file
    articles_pdf = record.read_jsonl(record.input_pdf)
    # Read pdf_parse jsonl file
    articles_meta = record.read_jsonl(record.input_meta)
    # Extract fields of interest from metadata jsonl
    meta_extracted = record.extract_metadata(articles_meta)
    # Extract fields of interest from pdf_parse
    body_extracted = record.extract_body_text(articles_pdf)
    # Write to files
    write_meta = record.write_to_files(meta_extracted, record.output_meta)
    write_pdf = record.write_to_files(body_extracted, record.output_pdf)
