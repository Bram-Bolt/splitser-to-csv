# importing required classes
from pypdf import PdfReader

import extraction_utils

# creating a pdf reader object
reader = PdfReader("example.pdf")
balance_page = reader.pages[1]


def get_heading() -> str:
    return "Participant,Balance,Expenses+,Expenses-,Income+,Income-,Payment+,Payment-"


# extract text
def get_rows(page):
    selected_rows = extraction_utils.select_rows(
        page, start_label="bal start", end_label="bal end"
    )
    rows = []
    for participant in selected_rows:
        split_participant = participant.split("€")
        name = [split_participant[0][:-1]]
        balances = extraction_utils.balances_to_float(split_participant[1:])
        rows.append(name + balances)

    return rows


output_list = [[get_heading()]]
output_list + get_rows(balance_page)

print(output_list + get_rows(balance_page))
