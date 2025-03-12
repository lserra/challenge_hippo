#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ==============================================================================
# Goal 2. Calculate metrics for some dimensions
# We want to check how some metrics perform depending on a few dimensions.
# Metrics: Count of claims, Count of reverts, Average unit price, Total price
# Dimensions: npi, ndc
# ==============================================================================
# Created by: laercio.serra@gmail.com
# Created at: 03/11/2025
# ==============================================================================

# Defining libraries
import os

import duckdb
import pandas as pd


# TASK1: create claims bigtable
# TASK2: calculate metrics
# TASK3: export results to JSON file
class CalculateMetrics:
    def __init__(self, app_path):
        self.app_path = app_path
        self.db_path = os.path.join(self.app_path, "database/hippo.db")
        self.json_file_path = os.path.join(self.app_path, "output/metrics.json")

    def create_bt(self):
        query = """
        SELECT 
            p.id as pharmacy, 
            r.id as reverted_claim, 
            r.timestamp as reverted_claim_timestamp, 
            c.id as claim,
            c.timestamp as claim_timestamp,
            c.npi as claim_npi,
            c.ndc as claim_ndc,
            c.price as claim_price,
            c.quantity as claim_qty
        FROM hippo.main.claims c
        INNER JOIN hippo.main.pharmacies p 
        ON c.ndc = p.chain
        INNER JOIN hippo.main.reverts r 
        ON c.id = r.claim_id;
        """

        # Create a DuckDB database connection
        con = duckdb.connect(database=self.db_path, read_only=False)

        # Retrieve rows
        df = pd.read_sql(query, con)

        # Create bigtable
        con.execute(f"DROP TABLE IF EXISTS bt_claims")
        con.execute(f"CREATE TABLE bt_claims AS SELECT * FROM df")

        print(f"=====> bt_claims table created successfully")

    def calc_metrics(self):
        query = """
        SELECT
            bc.claim_npi as npi,
            bc.claim_ndc as ndc,
            COUNT(bc.claim) as fills,
            COUNT(bc.reverted_claim) as reverted,
            AVG(bc.claim_price) as avg_price,
            SUM(bc.claim_price) as total_price
        FROM hippo.main.bt_claims bc
        GROUP BY
            bc.claim_npi,
            bc.claim_ndc;
        """

        try:
            # Create a DuckDB database connection
            con = duckdb.connect(database=self.db_path, read_only=False)

            # Retrieve rows
            df = pd.read_sql(query, con)

            if len(df) > 0:
                print(f"=====> Metrics calculated successfully")
                return df
            else:
                print(f"=====> No data found for metrics calculation")
                return None

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    def generate_json_file(self, df):
        try:
            df.to_json(self.json_file_path, orient='records', indent=4)
            print(f"=====> JSON file created successfully at {self.json_file_path}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
