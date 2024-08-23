# importing required classes 
from pypdf import PdfReader 
  
# creating a pdf reader object 
reader = PdfReader('example.pdf') 
  
# printing number of pages in pdf file 
n_pages = len(reader.pages)
  
for i in range(n_pages):
    page = reader.pages[i] 

    print(page.extract_text()) 
    
# balance_csv
