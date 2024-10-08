from pypdf import PdfReader, PageObject
from typing import List, Dict, Tuple
import csv
from . import extraction_utils
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)

balance_file = Path("./output/balance.csv")


# Make heading for CSV
def get_heading() -> List[str]:
    return [
        "Participant",
        "Balance",
        "Expenses+",
        "Expenses-",
        "Income+",
        "Income-",
        "Payment+",
        "Payment-",
    ]


# Make rows for CSV
def get_rows(page: PageObject, language: Dict[str, str]) -> List[List[str]]:
    # Select rows needed from page
    selected_rows = extraction_utils.select_rows(
        page, start_label="bal start", end_label="bal end", language=language
    )
    # process each participant row
    rows = [
        process_participant_row(participant, language) for participant in selected_rows
    ]
    return rows


# Process a participant row
def process_participant_row(participant: str, language: Dict[str, str]) -> List[str]:
    # parse row

    name, raw_balances = balance_parser(participant, language)
    # convert balance strings to floats.
    balances = [
        extraction_utils.amount_to_float(balance, language) for balance in raw_balances
    ]
    return name + balances


def balance_parser(
    participant: str, language: Dict[str, str]
) -> Tuple[List[str], List[str]]:
    split_participant = participant.split("€")
    name = split_participant[0].strip()
    balances = split_participant[1:]
    if language["currency notation"] == "€-":
        return ([name], balances)
    if name.endswith("-"):
        balances[0] = "-" + balances[0]
    return ([name[:-1].strip()], balances)


# write final balance csv
def write_csv(input_pdf_path: str, language: Dict[str, str]) -> None:
    try:
        reader = PdfReader(input_pdf_path)
        # get the balance page
        balance_page = reader.pages[1]
    except FileNotFoundError:
        logging.error(f"The file {input_pdf_path} was not found.")

    except Exception as e:
        logging.error(f"Error reading the PDF: {e}")

    # generate list of strigns to put in CSV
    output_list = [get_heading()] + get_rows(balance_page, language)
    # write csv
    try:
        with open(balance_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(output_list)
        logging.info("Balance CSV file created successfully. See output/balance.csv.")
    except IOError as e:
        logging.error(f"Error writing to Balance CSV: {e}")
