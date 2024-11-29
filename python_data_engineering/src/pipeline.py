import unicodedata
import pandas as pd
import json
import re
from collections import Counter

from common import date_formater

############################ ############################ ############################ 
    ############################ Step 1: Load Data ############################
############################ ############################ ############################
# Path to datasets
drugs_file_path = "../data/drugs.csv"
pubmed_file_path = "../data/pubmed.csv"
clinical_trials_file_path = "../data/clinical_trials.csv"

# Load datasets
# Read the files with proper encoding, utf-8 is most common for special characters
drugs_df = pd.read_csv(drugs_file_path, dtype=str, encoding='utf-8')
pubmed_df = pd.read_csv(pubmed_file_path, dtype=str, encoding='utf-8')
clinical_trials_df = pd.read_csv(clinical_trials_file_path, dtype=str, encoding='utf-8')

############################ ############################ ############################ 
    ########################### Step 2: Clean the Data ###########################
############################ ############################ ############################
# Clean the drugs dataset (standardize drug names to lowercase)
drugs_df["drug"] = drugs_df["drug"].str.strip().str.lower()

# Clean the PubMed dataset (standardize title, journal, and date)
pubmed_df["title"] = pubmed_df["title"].str.strip().str.lower()
pubmed_df["journal"] = pubmed_df["journal"].str.strip()
pubmed_df["date"] = pubmed_df["date"].apply(date_formater) # Convert all dates

# Clean the Clinical Trials dataset (standardize title, journal, and date)
clinical_trials_df = clinical_trials_df.rename(columns={"scientific_title": "title"})
clinical_trials_df["title"] = clinical_trials_df["title"].str.strip().str.lower()
clinical_trials_df["journal"] = clinical_trials_df["journal"].str.strip()
clinical_trials_df["date"] = clinical_trials_df["date"].apply(date_formater) # Convert all dates

############################ ############################ ############################ 
    ################## Step 3: Find Drug Mentions in datasets ##################
############################ ############################ ############################
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

# Merge mentions of drugs in PubMed and Clinical Trials
drug_mentions_df = pd.concat([pubmed_drug_mentions_df[["drug", "title", "source"]],
                              clinical_trials_drug_mentions_df[["drug", "title", "source"]]])

# Step 4: Create the Drug Mentions Graph
def create_drug_mentions_graph(drug_mentions_df, pubmed_df, clinical_trials_df):
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

# Generate the JSON graph for drug mentions
drug_mentions_graph = create_drug_mentions_graph(drug_mentions_df, pubmed_df, clinical_trials_df)

# print(drug_mentions_graph)

# Output the result as a JSON string
# json_output = json.dumps(drug_mentions_graph, indent=2, ensure_ascii=False)

# Write the output to a JSON file
with open("drug_mentions_graph.json", "w") as f:
    # ensure_ascii=False: to preserve special characters in their original form
    json.dump(drug_mentions_graph, f, indent=2, ensure_ascii=False)

