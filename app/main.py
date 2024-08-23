# importing required classes
from pypdf import PdfReader
import balance_csv
import expenses_csv


from lang import LANGUAGES 
import argparse

def main():
    global language_string
    parser = argparse.ArgumentParser(description="PDF to change to CSV")
    parser.add_argument(
        "filename", type=str, help="The output file name (with extension)."
    )
    
    parser.add_argument('-l', '--language', type=str, default='EN', help='Language code (default: EN)')

    args = parser.parse_args()
    language = LANGUAGES.get(args.language, LANGUAGES['EN'])

    balance_csv.write_csv(args.filename, language)
    expenses_csv.write_csv(args.filename, language)


if __name__ == "__main__":
    main()
