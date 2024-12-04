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
            return pd.to_datetime(_date, format=_format)
        except ValueError:
            continue

def find_drug_mentions(drug_list, titles):
    """
    Finds mentions of drugs in a list of titles.

    Args:
        drug_list (pd.Series): A pandas Series containing drug names.
        titles (pd.Series): A pandas Series containing publication titles.

    Returns:
        list of tuple: A list of tuples containing:
            - Drug name
            - Title in which the drug is mentioned
    """
    mentions = []
    for drug in drug_list:
        matches = titles[titles.str.contains(rf"\b{drug}\b", regex=True)]
        for _, title in matches.items():
            mentions.append((drug, title))
    return mentions

def create_drug_mentions_graph(drug_mentions_df, pubmed_df, clinical_trials_df):
    """
    Creates a JSON graph representing drug mentions in journals and clinical trials.

    Args:
        drug_mentions_df (pd.DataFrame): DataFrame containing drug mentions.
        pubmed_df (pd.DataFrame): DataFrame containing PubMed data.
        clinical_trials_df (pd.DataFrame): DataFrame containing Clinical Trials data.

    Returns:
        dict: A dictionary.
    """
    # Initialize a dictionary to store the graph
    drug_graph = {}
    
    # Merge PubMed and Clinical Trials mentions
    all_mentions_df = pd.concat([pubmed_df[["id", "title", "journal", "date"]],
                                 clinical_trials_df[["id", "title", "journal", "date"]]])
    
    # Iterate through drug mentions
    for _, row in drug_mentions_df.iterrows():
        drug = row["drug"]
        title = row["title"]
        source = row["source"]
        
        # Initialize structure for the drug if not present
        if drug not in drug_graph:
            drug_graph[drug] = {"journals": {}}
        
        # Find journal and date from the original publications
        matching_row = all_mentions_df[all_mentions_df['title'] == title].iloc[0]
        journal = matching_row['journal']
        date = matching_row['date'].strftime("%Y-%m-%d")
        
        # Add the title, journal, date and source to the drug's journal mention list
        if journal not in drug_graph[drug]["journals"]:
            drug_graph[drug]["journals"][journal] = []
        
        drug_graph[drug]["journals"][journal].append({"date": date, "title": title, "source": source})
    
    return drug_graph