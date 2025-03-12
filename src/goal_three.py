#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ==============================================================================
# Goal 3. Make a recommendation for the top 2 Chain to be displayed for each Drug.
# The business team wants to understand Drug unit prices per Chain.
# To measure performance, we will check the chain that, on average, charges less
# per drug unit. Please, write the output to a JSON file.
# ==============================================================================
# Created by: laercio.serra@gmail.com
# Created at: 03/12/2025
# ==============================================================================

# Defining libraries
import json
import os

import duckdb
import pandas as pd


# TASK1: querying the data
# TASK2: calculating average prices per chain for each drug
# TASK3: sorting the results
# TASK4: writing the results to a JSON file
class RecommendTopChains:
    def __init__(self, app_path):
        self.app_path = app_path
        self.db_path = os.path.join(self.app_path, "database/hippo.db")
        self.json_file_path = os.path.join(self.app_path, "output/top_chains.json")

    def run(self):
        query = """
        SELECT
            bc.claim_npi as ndc,
            bc.pharmacy as chain,
            AVG(bc.claim_price) as avg_price
        FROM hippo.main.bt_claims bc
        GROUP BY
            bc.claim_npi,
            bc.pharmacy;
        """

        try:
            # Create a DuckDB database connection
            con = duckdb.connect(database=self.db_path, read_only=False)

            # Retrieve rows
            df = pd.read_sql(query, con)

            if len(df) > 0:
                # Group by ndc and sort chains by avg_price within each group
                df_sorted = df.sort_values(
                    by=['ndc', 'avg_price'], ascending=[True, True]
                )
                top_chains = df_sorted.groupby('ndc').head(2)

                # Create the output format
                result = []
                for ndc, group in top_chains.groupby('ndc'):
                    chains = group[['chain', 'avg_price']].to_dict(orient='records')
                    result.append({
                        'ndc': ndc,
                        'chain': chains
                    })

                # Write to JSON file
                with open(self.json_file_path, 'w') as f:
                    json.dump(result, f, indent=4)

                print(f"=====> Recommendations written to {self.json_file_path}")

            else:
                print(f"=====> No data found for recommendations")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
