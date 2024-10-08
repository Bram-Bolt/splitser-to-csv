
# splitser-to-csv
## Simple python script to generate CSVs based on Splitser settlement PDFs.
<img src="https://i.imgur.com/RsnM866.png" alt="drawing" width="200"/>

This program uses PyPdf to read out the PDF files generated by Splitser/WieBetaaltWat, and convert them to CSV. 
This project will generate two files:

1. balance.csv, with balances of the participants
2. expenses.csv, with all expenses made in the settlement.

## Quick Set Up
### Installation
To install the package, clone the repository and use  `pip`  to install it locally:

```bash
git clone https://github.com/bram-bolt/splitser-to-csv.git
cd splitser-to-csv
pip install .
```

### Usage
Usage is language dependent, since PDF headings and currency notation differ.
#### 🇬🇧 English (Splitser)
Usage defaults to English
```bash
python -m app.main [file]
```
#### 🇳🇱 Dutch (WieBetaaltWat)
Voor Nederlandse PDFs gebruik de --language flag. 
```bash
python -m app.main [file] -l NL 
```
.. of
```bash
python -m app.main [file] --language NL 
```

## Advanced tutorial
### 1. Download PDF
A PDF of settlements can be downloaded the following way:

 1. Settle your list
 2. Press the `Settlements` button
 3. Tap on the screen saying `You are even 🎉`
 4. Press the `Settlement` button
 5. Press PDF.
 6. Transfer this PDF to the right device.

### 2. Put PDF in splitser-to-csv directory
By putting the PDF in the splitser-to-csv directory, you can just use the filename as [file] argument.
### 3. Run the command
```bash
python -m app.main [file] --language [LANG] 
```
Current language codes:
EN: English (also used in German and Italian version of Splitser)
NL: Dutch (Used in WieBetaaltWat)

### 4. Locate output CSVs
The generated CSVs are located in ./output

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss potential changes or improvements.

Questions? Feel free to reach out to [contact@brambolt.me](mailto:contact@brambolt.me).
