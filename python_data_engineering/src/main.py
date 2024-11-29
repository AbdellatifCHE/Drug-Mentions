import unicodedata
import pandas as pd
import json
import re
from collections import Counter

################## ################## ################## ################## ################## ##################
def date_formater(_date: str):# -> pd.Timestamp:
    """
    This function parses a date string by trying to match one of the date formats

    :param _date: str: Date string
    :return: str: Parsed date string
    :raises: ValueError: If the date string does not match any of the date formats
    """
    
    possible_formats = ["%d/%m/%Y", "%Y-%m-%d", "%d %B %Y"]
    for _format in possible_formats:
        try:
            return pd.to_datetime(_date, format=_format)#, errors="coerce")
        except ValueError:
            continue
    # If none of the formats match, raise an error
    #raise ValueError(f"Date format for {_date} not recognized")
################## ################## ################## ################## ################## ##################

# Step 1: Load Data
drugs_file_path = "../data/drugs.csv"
pubmed_file_path = "../data/pubmed.csv"
clinical_trials_file_path = "../data/clinical_trials.csv"

# Load datasets
# Read the files with proper encoding, utf-8 is most common for special characters
drugs_df = pd.read_csv(drugs_file_path, dtype=str, encoding='utf-8')
pubmed_df = pd.read_csv(pubmed_file_path, dtype=str, encoding='utf-8')
clinical_trials_df = pd.read_csv(clinical_trials_file_path, dtype=str, encoding='utf-8')

# Step 2: Clean the Data
# Clean the drugs dataset (standardize drug names to lowercase)
drugs_df["drug"] = drugs_df["drug"].str.strip().str.lower()

# Clean the PubMed dataset (standardize title, journal, and date)
pubmed_df["title"] = pubmed_df["title"].str.strip().str.lower().apply(lambda x: unicodedata.normalize('NFC', x))
pubmed_df["journal"] = pubmed_df["journal"].str.strip().apply(lambda x: unicodedata.normalize('NFC', x))
pubmed_df["date"] = pubmed_df["date"].apply(date_formater)  # to_datetime(pubmed_df["date"], errors="coerce")  # Convert date

print("################################### Before conversion ###################################")
print(clinical_trials_df["journal"])

# Clean the Clinical Trials dataset (standardize title, journal, and date)
clinical_trials_df = clinical_trials_df.rename(columns={"scientific_title": "title"})
clinical_trials_df["title"] = clinical_trials_df["title"].str.strip().str.lower().apply(lambda x: unicodedata.normalize('NFC', x))
clinical_trials_df["journal"] = clinical_trials_df["journal"].str.strip().apply(lambda x: unicodedata.normalize('NFC', str(x)))
clinical_trials_df["date"] = pd.to_datetime(clinical_trials_df["date"], errors="coerce")  # Convert date

print("################################### After conversion ###################################")
print(clinical_trials_df["journal"])

# Step 3: Find Drug Mentions in PubMed Titles
def find_drug_mentions(drug_list, titles):
    mentions = []
    for drug in drug_list:
        matches = titles[titles.str.contains(rf"\b{drug}\b", regex=True)]
        for _, title in matches.items():
            mentions.append((drug, title))
    return mentions

# Extract mentions of drugs in PubMed titles
pubmed_drug_mentions = find_drug_mentions(drugs_df["drug"], pubmed_df["title"])
pubmed_drug_mentions_df = pd.DataFrame(pubmed_drug_mentions, columns=["drug", "title"])
pubmed_drug_mentions_df["source"] = "PubMed"

# Extract mentions of drugs in clinical_trials titles
clinical_trials_drug_mentions = find_drug_mentions(drugs_df["drug"], clinical_trials_df["title"])
clinical_trials_drug_mentions_df = pd.DataFrame(clinical_trials_drug_mentions, columns=["drug", "title"])
clinical_trials_drug_mentions_df["source"] = "Clinical Trial"

# Combine mentions of drugs in PubMed and Clinical Trials
drug_mentions_df = pd.concat([pubmed_drug_mentions_df[["drug", "title", "source"]],
                              clinical_trials_drug_mentions_df[["drug", "title", "source"]]])

# Step 4: Create the Drug Mentions Graph
def create_drug_mentions_graph(drug_mentions_df, pubmed_df, clinical_trials_df):
    # Initialize a dictionary to store the graph
    drug_graph = {}
    
    # Combine PubMed and Clinical Trials mentions
    all_mentions_df = pd.concat([pubmed_df[["id", "title", "journal", "date"]],
                                 clinical_trials_df[["id", "title", "journal", "date"]]])
    
    # Iterate through drug mentions
    for _, row in drug_mentions_df.iterrows():
        drug = row["drug"]
        title = row["title"]
        source = row["source"]
        
        # Initialize structure for the drug if not already present
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

# Generate the JSON graph for drug mentions
drug_mentions_graph = create_drug_mentions_graph(drug_mentions_df, pubmed_df, clinical_trials_df)

print(drug_mentions_graph)

# Output the result as a JSON string
json_output = json.dumps(drug_mentions_graph, indent=2, ensure_ascii=False)

# Optionally, write the output to a JSON file
with open("drug_mentions_graph.json", "w") as f:
    # ensure_ascii=False: to preserve special characters in their original form
    json.dump(drug_mentions_graph, f, indent=2, ensure_ascii=False)

# Print a preview of the JSON output
#print(json_output)  # Show the first 500 characters for preview

