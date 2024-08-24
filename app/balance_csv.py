# importing required classes
from pypdf import PdfReader, PageObject
from typing import List, Dict
import csv
import extraction_utils
import logging

logging.basicConfig(level=logging.INFO)


# Make heading for CSV
def get_heading() -> str:
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
    rows = [process_participant_row(participant) for participant in selected_rows]
    return rows


# Process a participant row
def process_participant_row(participant: str) -> List[str]:
    # parse row
    split_participant = participant.split("€")
    name = [split_participant[0][:-1]]
    # convert balance strings to floats.
    balances = [
        extraction_utils.amount_to_float(balance) for balance in split_participant[1:]
    ]
    return name + balances


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
        with open("../output/balance.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(output_list)
        logging.info("Balance CSV file created successfully.")
    except IOError as e:
        logging.error(f"Error writing to Balance CSV: {e}")
