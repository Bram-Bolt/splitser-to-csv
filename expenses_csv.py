# importing required classes
from pypdf import PdfReader
import extraction_utils
from icecream import ic

import lang

language = lang.NL

# creating a pdf reader object
reader = PdfReader("example.pdf")
expense_pages = reader.pages[2:]

ex_expense_pages = expense_pages[0]
transactions = extraction_utils.select_rows(
    ex_expense_pages, start_label="exp start", end_label="exp end"
)

ic(transactions)
