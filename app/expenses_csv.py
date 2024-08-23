# importing required classes
from pypdf import PdfReader
import extraction_utils
from icecream import ic
import csv
import lang
import balance_csv

balance_file = "../output/balance.csv"


def get_heading():
    return ["Payer", "Description", "Amount", "Date"] + get_participant_list(
        balance_file
    )


def get_participant_list(file_name):
    participants = []
    with open(file_name, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            participants.append(row["Participant"])
    return participants


def settlement_parser(settlements):
    split_settlements = settlements.split(")")
    settlement_dict = {}
    for settlement in split_settlements[:-1]:
        data = settlement.replace("(", "").split("€")
        settlement_dict[data[0].replace(",", "").strip()] = (
            extraction_utils.balances_to_float(data[1])
        )

    x = []
    for participant in get_participant_list(balance_file):
        clean_participant = participant.replace(" ", "")
        y = settlement_dict.get(clean_participant, 0)
        x.append(y)

    return x


def transaction_parser(transaction):
    remainder = transaction
    for participant in get_participant_list(balance_file):
        if transaction.startswith(participant):
            paid_by = participant
            remainder = transaction[len(participant) :]
    description = remainder.split("€")[0].strip()
    remainder = "€".join(remainder.split("€")[1:]).replace(" ", "")
    comma_index = remainder.find(",")
    amount = extraction_utils.balances_to_float(remainder[: comma_index + 3])
    date = remainder[comma_index + 3 : comma_index + 13]
    settlements = remainder[comma_index + 13 :]
    parsed_settlements = settlement_parser(settlements)
    return [paid_by, description, amount, date] + parsed_settlements


def get_transaction_rows(expense_pages, language):
    transaction_rows = []
    sb = ""
    for page in expense_pages[:-1]:
        transactions = extraction_utils.select_rows(
            page, start_label="exp start", end_label="exp end", language=language
        )
        for transaction in transactions:
            if transaction.endswith(")"):
                sb += transaction
                transaction_rows.append(transaction_parser(sb))
                sb = ""
            else:
                sb += transaction

    transactions = extraction_utils.select_rows(
        expense_pages[-1], start_label="exp start", end_label="exp last end", language=language
    )

    for transaction in transactions:
        if transaction.endswith(")"):
            sb += transaction
            transaction_rows.append(transaction_parser(sb))
            sb = ""
        else:
            sb += transaction

    return transaction_rows


def write_csv(inp, language):
    reader = PdfReader(inp)
    expense_pages = reader.pages[2:]
    output_list = [get_heading()] + get_transaction_rows(expense_pages, language)
    with open("../output/expenses.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(output_list)


