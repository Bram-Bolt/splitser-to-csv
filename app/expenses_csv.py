from pypdf import PdfReader, PageObject
from . import extraction_utils
import csv
import logging
from typing import List, Dict, Callable
from pathlib import Path

logging.basicConfig(level=logging.INFO)

balance_file = Path("./output/balance.csv")
expenses_file = Path("./output/expenses.csv")


# Make heading for CSV
def get_heading() -> List[str]:
    return ["Payer", "Description", "Amount", "Date"] + get_participant_list(
        balance_file
    )


# Generate list of participants
def get_participant_list(filename: str) -> list[str]:
    try:
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            participants = [row["Participant"] for row in reader]
        return participants
    except Exception as e:
        logging.error(
            f"Could not read {filename}. Rerunning often resolves this issue. {e}"
        )


# Parse a settlement
def settlement_parser(settlements: str, language: Dict[str, str]) -> List[str]:
    try:
        split_settlements = settlements.split(")")
        # make a dictionary of the settlements {name: amount}
        settlement_dict = {}
        for settlement in split_settlements[:-1]:
            data = settlement.replace("(", "").split("€")
            settlement_dict[data[0].replace(",", "").strip()] = (
                extraction_utils.amount_to_float(data[1], language)
            )

        parsed_settlements = [
            # When participant dit not participate, set it to 0.
            settlement_dict.get(participant.replace(" ", ""), 0)
            for participant in get_participant_list(balance_file)
        ]
        return parsed_settlements
    except Exception as e:
        logging.error(f"Error parsing settlements: {e}")


# parse a transaction
def transaction_parser(transaction: str, language: Dict[str, str]) -> List[str]:
    try:
        # set remainder of string to parse
        remainder = transaction
        # Search for participant who paid
        for participant in get_participant_list(balance_file):
            if transaction.startswith(participant):
                paid_by = participant
                remainder = transaction[len(participant) :]
        # Get description
        description = remainder.split("€")[0].strip()
        remainder = "€".join(remainder.split("€")[1:]).replace(" ", "")
        # Locate comma
        comma_index = remainder.find(language["seperator"])
        # Index amount
        amount = extraction_utils.amount_to_float(
            remainder[: comma_index + 3], language
        )
        # Index Date
        date = remainder[comma_index + 3 : comma_index + 13]
        # Index Settlements
        settlements = remainder[comma_index + 13 :]
        # Parse settlements
        parsed_settlements = settlement_parser(settlements, language)
        return [paid_by, description, amount, date] + parsed_settlements
    except Exception as e:
        logging.error(f"Error parsing transaction: {e}")


# Combine rows of transaction
# Sometimes a transaction has multiple rows, therefore we need to combine them before parsing
def build_transactions(
    transactions: List[str],
    transaction_rows: List[str],
    transaction_builder: str,
    parser: Callable,
    language: Dict[str, str],
) -> str:
    for transaction in transactions:
        if transaction.endswith(")"):
            transaction_builder += transaction
            transaction_rows.append(parser(transaction_builder, language))
            transaction_builder = ""
        else:
            transaction_builder += transaction
    return transaction_builder


# Make rows of csv
def get_transaction_rows(
    expense_pages: List[PageObject], language: Dict[str, str]
) -> List[str]:
    transaction_rows = []
    transaction_builder = ""
    try:
        # Process all pages except the last one
        for page in expense_pages[:-1]:
            transactions = extraction_utils.select_rows(
                page, start_label="exp start", end_label="exp end", language=language
            )
            transaction_builder = build_transactions(
                transactions,
                transaction_rows,
                transaction_builder,
                transaction_parser,
                language,
            )

        # Process the last page
        transactions = extraction_utils.select_rows(
            expense_pages[-1],
            start_label="exp start",
            end_label="exp last end",
            language=language,
        )
        build_transactions(
            transactions,
            transaction_rows,
            transaction_builder,
            transaction_parser,
            language,
        )

        return transaction_rows
    except Exception as e:
        logging.error(f"Error making rows for CSV: {e}")


def write_csv(input_pdf_path: str, language: Dict[str, str]) -> None:
    try:
        reader = PdfReader(input_pdf_path)
        # get expense pages
        expense_pages = reader.pages[2:]
    except FileNotFoundError:
        logging.error(f"The file {input_pdf_path} was not found.")
        return

    except Exception as e:
        logging.error(f"Error reading the PDF: {e}")
        return

    # generate list of strings to put in CSV
    output_list = [get_heading()] + get_transaction_rows(expense_pages, language)

    # write csv
    try:
        with open(expenses_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(output_list)
        logging.info("Expenses CSV file created successfully. See output/expenses.csv.")
    except IOError as e:
        logging.error(f"Error writing to Expenses CSV: {e}")
