from module.tabulate_data import TabulateData
import argparse
import typer

if __name__ == "__main__":
    # Design argument parser
    parser = argparse.ArgumentParser(
        description='Transform jsonl files into csv tables')
    parser.add_argument(
        '-im',
        '--meta_input',
        metavar='',
        required=True,
        help='Provide metadata jsonl files with extracted fields of interests')
    parser.add_argument(
        '-ip',
        '--pdf_input',
        metavar='',
        required=True,
        help='Provide jsonl pdf files with extracted fields of interests')
    parser.add_argument('-o',
                        '--merged_output',
                        metavar='',
                        required=True,
                        help='Provide output path for merged table')
    args = parser.parse_args()

    # Pipeline per so
    typer.secho('Reading jsonl files with extracted fields of interests',
                bold=True)
    record = TabulateData(args.meta_input, args.pdf_input, args.merged_output)
    pdf_data = record.read_jsonl(record.extract_pdf)
    tbl_meta = record.read_jsonl(record.extract_meta)
    merged_tb = record.merge_df(tbl_meta, pdf_data)
    record.write_table(merged_tb)
    typer.secho('Merged table has been merged', bold=True)
