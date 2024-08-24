from pypdf import PageObject
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)


# Select rows based on start and end of table
def select_rows(
    page: PageObject, start_label: str, end_label: str, language: Dict[str, str]
):
    try:
        # extract text
        text_rows = page.extract_text().split("\n")

        # get indicators in right language
        start = language[start_label]
        end = language.get(end_label)  # Use get() to avoid KeyError

        # start one after heading of rows
        start_index = text_rows.index(start) + 1

        # if there is an end, select until end.
        end_index = text_rows.index(end) if end else None

        return text_rows[start_index:end_index]

    except ValueError as e:
        logging.error(
            f"Label not found in the text rows, is the language selected correctly?: {e}"
        )
        return []

    except KeyError as e:
        logging.error(f"Label not found in the language dictionary: {e}")
        return []


# Convert an amount to a float
def amount_to_float(balance: str) -> float:
    try:
        return float(balance.replace(".", "").replace(",", "."))
    except ValueError as e:
        logging.error(f"Could not convert balance to float: {e}")
        return None
