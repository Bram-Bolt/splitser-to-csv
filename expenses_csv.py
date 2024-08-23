# importing required classes 
from pypdf import PdfReader 

import lang
language = lang.NL

# creating a pdf reader object 
reader = PdfReader('example.pdf') 
expense_pages = reader.pages[2:] 

ex_expense_pages = expense_pages[0]
transactions = ex_expense_pages.extract_text().split("\n")

for trans in transactions:
    print(trans)