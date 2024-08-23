# importing required classes 
from pypdf import PdfReader 
import lang

language = lang.NL

# creating a pdf reader object 
reader = PdfReader('example.pdf') 
balance_page = reader.pages[1] 


def get_heading() -> str:
    return "Participant,Balance,Expenses+,Expenses-,Income+,Income-,Payment+,Payment-"

# extract text
def get_rows(page):
    text_rows = balance_page.extract_text().split("\n")

    participants = text_rows[text_rows.index(language["bal heading"])+1:]
    
    rows = []
    for participant in participants:
        split_participant = participant.split("€")
        name = [split_participant[0][:-1]]
        balances = balances_to_float(split_participant[1:])
        rows.append(name + balances)
        
    return rows 

def balances_to_float(balances):
    balance_to_float = lambda balance: float(balance.replace(".", "").replace(",", "."))
    float_balances = list(map(balance_to_float, balances))
    return float_balances




output_list = [[get_heading()]]
output_list + get_rows(balance_page)

print(output_list + get_rows(balance_page))