import main





def select_rows(page, start_label, end_label, language):
    text_rows = page.extract_text().split("\n")
    start = language[start_label]
    end = language[end_label]
    if end:
        return text_rows[text_rows.index(start) + 1 : text_rows.index(end)]
    return text_rows[text_rows.index(start) + 1 :]


def balances_to_float(balances):
    if isinstance(balances, list):
        balance_to_float = lambda balance: float(
            balance.replace(".", "").replace(",", ".")
        )
        float_balances = list(map(balance_to_float, balances))
        return float_balances
    else:
        return float(balances.replace(".", "").replace(",", "."))
