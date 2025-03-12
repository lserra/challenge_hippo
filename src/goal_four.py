#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ==============================================================================
# Goal 4. Understand Most common quantity prescribed for a given Drug
# The business team wants to know what is the Drug most common quantity
# prescribed to negotiate prices discounts.
# Please, write the output to a JSON file.
# ==============================================================================
# Created by: laercio.serra@gmail.com
# Created at: 03/12/2025
# ==============================================================================

# Defining libraries
import json
import os
from collections import Counter

import duckdb
import pandas as pd


# TASK1: querying the data
# TASK2: calculating the most common quantities prescribed for each drug
# TASK3: writing the results to a JSON file
class MostCommonQuantities:
    def __init__(self, app_path):
        self.app_path = app_path
        self.db_path = os.path.join(self.app_path, "database/hippo.db")
        self.json_file_path = os.path.join(self.app_path, "output/most_common_quantities.json")

    def run(self):
        query = """
        SELECT
            bc.claim_npi as ndc,
            bc.claim_qty as quantity
        FROM hippo.main.bt_claims bc;
        """

        try:
            # Create a DuckDB database connection
            con = duckdb.connect(database=self.db_path, read_only=False)

            # Retrieve rows
            df = pd.read_sql(query, con)

            if len(df) > 0:
                # Group by ndc and calculate the most common quantities
                result = []
                for ndc, group in df.groupby('ndc'):
                    quantities = group['quantity'].tolist()
                    most_common = [item for item, count in
                                   Counter(quantities).most_common()]

                    result.append({
                        'ndc': ndc,
                        'most_prescribed_quantity': most_common
                    })

                # Write to JSON file
                with open(self.json_file_path, 'w') as f:
                    json.dump(result, f, indent=4)

                print(f"=====> Most common quantities written to {self.json_file_path}")

            else:
                print(f"=====> No data found for most common quantities")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
