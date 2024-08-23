# importing required classes
from pypdf import PdfReader
import balance_csv
import expenses_csv
import sys


import argparse


def main():
    parser = argparse.ArgumentParser(description="Process some CSV files.")
    parser.add_argument(
        "filename", type=str, help="The output file name (with extension)."
    )
    args = parser.parse_args()

    balance_csv.write_csv(args.filename)
    expenses_csv.write_csv(args.filename)


if __name__ == "__main__":
    main()
