from pypdf import PdfReader
import balance_csv
import expenses_csv
import argparse
from lang import LANGUAGES
import logging

logging.basicConfig(level=logging.INFO)


def main():
    try:
        # get arguments
        parser = argparse.ArgumentParser(description="PDF to change to CSV")
        parser.add_argument(
            "filename", type=str, help="The output file name (with extension)."
        )

        parser.add_argument(
            "-l",
            "--language",
            type=str,
            default="EN",
            help="Language code (default: EN)",
        )

        args = parser.parse_args()
        # selected language
        language = LANGUAGES.get(args.language, LANGUAGES["EN"])

        # generate CSV of balances
        balance_csv.write_csv(args.filename, language)

        # Generate CSV of expenses
        expenses_csv.write_csv(args.filename, language)

        logging.info(f'Conversion of "{args.filename}" finished succesfully.')
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
