
# Drug-Mentions Project
This project processes datasets related to drugs, PubMed articles, and clinical trials to identify mentions of drugs in publication and clinical trials titles.

## **Project Structure**
The project is organized as follows:

```
Drug-Mentions/
├── data/
│   └── (datasets: drugs.csv, pubmed.csv, pubmed.json, clinical_trials.csv)
├── src/
│   ├── pipeline.py       # Main script to process data and generate JSON output
│   └── utils.py         # Utility functions for data cleaning and formatting
├── test/
│   └── (unit tests)
└── sql/
    └── (folder for SQL-related parts)
```

### **Files**
1. **`pipeline.py`**
   - Main script for data processing:
     - Loads and cleans the datasets.
     - Identifies drug mentions in pubmed and clinical trials titles.
     - Generates a JSON graph that maps drug mentions to journals, titles, and publication dates.
   - Outputs the graph to `drug_mentions_graph.json`.

2. **`utils.py`**
   - Contains utility functions:
     - `date_formater`: Converts dates from multiple formats to a standardized format.

3. **Datasets** (stored in `data/`):
   - **`drugs.csv`**: List of drugs.
   - **`pubmed.csv`**: Publications from PubMed (CSV format).
   - **`pubmed.json`**: Publications from PubMed (JSON format).
   - **`clinical_trials.csv`**: Clinical trial publications.

4. **Output**:
   - A JSON file, `drug_mentions_graph.json`, containing a structured representation of drug mentions.

---

## **Installation and Requirements**
To run the project locally, you will need:
1. **Python**: Version 3.7 or higher.
2. **Libraries**:
   - `pandas`

### **Setup Instructions**
1. Clone the repository or download the project folder.
2. Navigate to the `Drug-Mentions` folder.
3. Set up a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # For Linux/MacOS
   venv\Scripts\activate      # For Windows
   ```
4. Install dependencies:
   ```bash
   pip install pandas
   ```

---

## **Execution**
1. Ensure the datasets (`drugs.csv`, `pubmed.csv`, `pubmed.json`, `clinical_trials.csv`) are present in the `data/` folder.
2. Run the `pipeline.py` script:
   ```bash
   python -m src.pipeline
   ```
3. The processed JSON output will be saved as `drug_mentions_graph.json` in the current working directory.

4. To execute the unit tests:
```bash
   python -m unittest discover -s test
```