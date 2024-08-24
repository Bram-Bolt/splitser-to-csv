# importing required classes
from pypdf import PdfReader, PageObject
from typing import List, Dict
import csv
import extraction_utils


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
    print(type(page))
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
    balances = extraction_utils.balances_to_float(split_participant[1:])
    return name + balances


# write final balance csv
def write_csv(input_pdf_path: str, language: Dict[str, str]) -> None:
    reader = PdfReader(input_pdf_path)
    # get the blaance page
    balance_page = reader.pages[1]
    # generate list of strigns to put in CSV
    output_list = [get_heading()] + get_rows(balance_page, language)
    # write csv
    with open("../output/balance.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(output_list)
