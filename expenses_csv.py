# importing required classes
from pypdf import PdfReader
import extraction_utils
from icecream import ic
import csv
import lang
import balance_csv

language = lang.NL

# creating a pdf reader object
fn = "example2.pdf"
reader = PdfReader(fn)
expense_pages = reader.pages[2:]

balance_csv.write_csv(fn)


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
    settlement_dict[data[0].replace(",", "").strip().replace(" ", "")] = (
        extraction_utils.balances_to_float(data[1])
    )

    x = []
    for participant in participant_list:
        clean_participant = participant.replace(" ", "")

        y = settlement_dict.get(clean_participant, 0)
        x.append(y)

    return x


# def transaction_parser(transaction):
#     remainder = transaction
#     for participant in participant_list:
#         if transaction.startswith(participant):
#             paid_by = participant
#             remainder = transaction[len(participant) :]
#     description = remainder.split("€")[0].strip()
#     remainder = "€".join(remainder.split("€")[1:])
#     amount = extraction_utils.balances_to_float(remainder.split(" ")[1])
#     date = remainder.split(" ")[2]
#     settlements = " ".join(remainder.split(" ")[3:])
#     parsed_settlements = settlement_parser(settlements)
#     return [paid_by, description, amount, date] + parsed_settlements


def transaction_parser(transaction):
    remainder = transaction
    for participant in participant_list:
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


ex_expense_pages = expense_pages[0]
participant_list = get_participant_list("out.csv")

skip = False
sb = ""
for j, page in enumerate(expense_pages[:-1]):
    transactions = extraction_utils.select_rows(
        page, start_label="exp start", end_label="exp end"
    )
    for i, transaction in enumerate(transactions):

        if transaction.endswith(")"):
            sb += transaction
            try:
                print(transaction_parser(sb))
            except:
                print(sb)
            sb = ""
        else:
            sb += transaction

        # print(f"{j}-{i} {transaction[-1]}")
