"""
Drug Mentions Pipeline: Extracting and Structuring Drug Mentions from PubMed and Clinical Trials Datasets.

Output: A JSON file named `drug_mentions_graph.json`, containing the processed data in a structured format.
"""

import argparse
import pandas as pd
import json

from utils import date_formater, find_drug_mentions, create_drug_mentions_graph

def main(drugs_file_path, pubmed_csv_file_path, pubmed_json_file_path, clinical_trials_file_path):
    """
    Main function to load, clean and process the dataset and generate the drug mentions JSON.

    Args:
        drugs_file_path (string): Path to the drugs dataset.
        pubmed_file_path (string): Path to the PubMed dataset.
        clinical_trials_file_path (string): Path to the Clinical Trials dataset.
    """
    # Load datasets
    # Read the files with proper encoding, utf-8 is most common for special characters
    drugs_df = pd.read_csv(drugs_file_path, dtype=str, encoding='utf-8')
    pubmed_csv_df = pd.read_csv(pubmed_csv_file_path, dtype=str, encoding='utf-8')
    pubmed_json_df = pd.read_json(pubmed_json_file_path, dtype=str, convert_dates=False, encoding='utf-8')
    clinical_trials_df = pd.read_csv(clinical_trials_file_path, dtype=str, encoding='utf-8')

    # Merge PubMed datasets
    pubmed_df = pd.concat([pubmed_csv_df, pubmed_json_df])

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

    # Extract drug mentions
    pubmed_drug_mentions = find_drug_mentions(drugs_df["drug"], pubmed_df["title"])
    pubmed_drug_mentions_df = pd.DataFrame(pubmed_drug_mentions, columns=["drug", "title"])
    pubmed_drug_mentions_df["source"] = "PubMed"

    clinical_trials_drug_mentions = find_drug_mentions(drugs_df["drug"], clinical_trials_df["title"])
    clinical_trials_drug_mentions_df = pd.DataFrame(clinical_trials_drug_mentions, columns=["drug", "title"])
    clinical_trials_drug_mentions_df["source"] = "Clinical Trial"

    drug_mentions_df = pd.concat([pubmed_drug_mentions_df, clinical_trials_drug_mentions_df])

    # Create the drug mentions graph
    drug_mentions_graph = create_drug_mentions_graph(drug_mentions_df, pubmed_df, clinical_trials_df)

    # Write the graph to a JSON file
    with open("drug_mentions_graph.json", "w") as f:
        # ensure_ascii=False: to preserve special characters (like ™,ô,è...) in their original form
        json.dump(drug_mentions_graph, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--drugs", required=True, help="Path to the drugs dataset (CSV)")
    parser.add_argument("--pubmed_csv", required=True, help="Path to the PubMed dataset (CSV)")
    parser.add_argument("--pubmed_json", required=True, help="Path to the PubMed dataset (JSON)")
    parser.add_argument("--clinical_trials", required=True, help="Path to the Clinical Trials dataset (CSV)")

    args = parser.parse_args()
    main(args.drugs, args.pubmed_csv, args.pubmed_json, args.clinical_trials)