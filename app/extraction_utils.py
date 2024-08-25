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

        # Find the start index based on 'starts with'
        start_index = (
            next(i for i, row in enumerate(text_rows) if row.startswith(start)) + 1
        )

        # Find the end index based on 'starts with', if end is provided
        end_index = (
            next((i for i, row in enumerate(text_rows) if row.startswith(end)))
            if end
            else None
        )

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
def amount_to_float(balance: str, language: Dict[str, str]) -> float:
    try:
        seperator = language["seperator"]
        if seperator == ".":
            return float(balance.replace(",", ""))
        else:
            return float(balance.replace(".", "").replace(",", "."))
    except ValueError as e:
        logging.error(f"Could not convert balance to float: {e}")
        return None
