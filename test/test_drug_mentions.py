import unittest
import pandas as pd
from datetime import datetime
from src.utils import date_formater, find_drug_mentions, create_drug_mentions_graph

class TestUtils(unittest.TestCase):
    def test_date_formater(self):
        """Test date_formater with multiple formats"""
        self.assertEqual(
            date_formater("01/01/2020"), datetime(2020, 1, 1)
        )  # Format: %d/%m/%Y
        self.assertEqual(
            date_formater("2020-01-01"), datetime(2020, 1, 1)
        )  # Format: %Y-%m-%d
        self.assertEqual(
            date_formater("1 January 2020"), datetime(2020, 1, 1)
        )  # Format: %d %B %Y
        self.assertIsNone(
            date_formater("1 Jan 2020")
        )  # Should return None for invalid dates

    def test_find_drug_mentions(self):
        """Test find_drug_mentions function"""
        mentions = find_drug_mentions(
            pd.Series(['aspirin', 'ibuprofen', 'paracetamol']), pd.Series(['aspirin for headache', 'ibuprofen benefits'])
        )
        expected_mentions = [
            ("aspirin", "aspirin for headache"),
            ("ibuprofen", "ibuprofen benefits"),
        ]
        self.assertEqual(mentions, expected_mentions)

    def test_create_drug_mentions_graph(self):
        """Test create_drug_mentions_graph function"""
        drug_mentions_df = pd.DataFrame(
            [
                {"drug": "aspirin", "title": "aspirin for headache", "source": "PubMed"},
                {"drug": "ibuprofen", "title": "ibuprofen benefits", "source": "PubMed"},
                {"drug": "paracetamol", "title": "paracetamol in flu treatment", "source": "Clinical Trial"}
            ]
        )

        pubmed_df = pd.DataFrame(
            [
                {"id": "1", "title": "aspirin for headache", "journal": "Journal A", "date": datetime(2020, 1, 1)},
                {"id": "2", "title": "ibuprofen benefits", "journal": "Journal B", "date": datetime(2020, 1, 2)}
            ]
        )

        clinical_trials_df = pd.DataFrame(
            [
                {"id": "1", "title": "paracetamol in flu treatment", "journal": "Journal C", "date": datetime(2020, 1, 3)}
            ]
        )

        graph = create_drug_mentions_graph(drug_mentions_df, pubmed_df, clinical_trials_df)

        expected_graph = {
            "aspirin": {
                "journals": {
                    "Journal A": [
                        {
                            "date": "2020-01-01",
                            "title": "aspirin for headache",
                            "source": "PubMed",
                        }
                    ]
                }
            },
            "ibuprofen": {
                "journals": {
                    "Journal B": [
                        {
                            "date": "2020-01-02",
                            "title": "ibuprofen benefits",
                            "source": "PubMed",
                        }
                    ]
                }
            },
            "paracetamol": {
                "journals": {
                    "Journal C": [
                        {
                            "date": "2020-01-03",
                            "title": "paracetamol in flu treatment",
                            "source": "Clinical Trial",
                        }
                    ]
                }
            },
        }
        self.assertEqual(graph, expected_graph)

if __name__ == "__main__":
    unittest.main()
