import pandas as pd

def date_formater(_date: str):
    possible_formats = ["%d/%m/%Y", "%Y-%m-%d", "%d %B %Y"]
    for _format in possible_formats:
        try:
            return pd.to_datetime(_date, format=_format)#, errors="coerce")
        except ValueError:
            continue
