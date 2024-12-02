import pandas as pd

def date_formater(_date: str):
    """
    Converts a date string into a standardized datetime format '%Y-%m-%d'.

    This function attempts to parse a given date string using a predefined list of possible formats.

    Args: _date (str): The date string to be converted.

    Returns: datetime or None: 
        - A `datetime` object if the date string matches one of the predefined formats.
        - `None` if the date string does not match any of the formats.
    """
    possible_formats = ["%d/%m/%Y", "%Y-%m-%d", "%d %B %Y"]
    for _format in possible_formats:
        try:
            return pd.to_datetime(_date, format=_format)#, errors="coerce")
        except ValueError:
            continue
