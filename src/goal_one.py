#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ==============================================================================
# Goal 1. Read data stored in JSON files
# Read pharmacy, claims and reverts from the provided files in your entry point.
# Some events may not comply with the provided schema. You can use the library
# of your choice to perform the JSON parsing.
# We are only interested in events from Pharmacy dataset.
# ==============================================================================
# Created by: laercio.serra@gmail.com
# Created at: 03/11/2025
# ==============================================================================

# Defining libraries
import glob
import os

import duckdb
import pandas as pd


class CreateAndPopulateTable:
    def __init__(self, app_path, tablename):
        self.app_path = app_path
        self.claims_path = os.path.join(self.app_path, "input/claims/*.json")
        self.pharmacies_path = os.path.join(self.app_path, "input/pharmacies/*.csv")
        self.reverts_path = os.path.join(self.app_path, "input/reverts/*.json")
        self.db_path = os.path.join(self.app_path, "database/hippo.db")
        self.tablename = tablename

    def from_csv(self):
        try:
            path = self.get_path()

            # Read CSV files into a Pandas DataFrame
            files = glob.glob(path)
            if not files:
                raise FileNotFoundError(
                    f"No CSV files found in the directory: {path}")
            df_list = [pd.read_csv(file) for file in files]
            df = pd.concat(df_list, ignore_index=True)

            self.run(df)
        except FileNotFoundError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def from_json(self):
        try:
            path = self.get_path()

            # Read JSON files into a Pandas DataFrame
            files = glob.glob(path)
            if not files:
                raise FileNotFoundError(
                    f"No JSON files found in the directory: {path}")
            df_list = [pd.read_json(file) for file in files]
            df = pd.concat(df_list, ignore_index=True)

            self.run(df)
        except FileNotFoundError as e:
            print(f"Error: {e}")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    @staticmethod
    def get_df_claims(df):
        # Define column names and data types
        df.columns = ['id', 'npi', 'ndc', 'price', 'quantity', 'timestamp']
        df['id'] = df['id'].astype(str)
        df['npi'] = df['npi'].astype(str)
        df['ndc'] = df['ndc'].astype(str)
        df['price'] = df['price'].astype(float)
        df['quantity'] = df['quantity'].astype(int)
        # Convert 'timestamp' column to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        return df

    @staticmethod
    def get_df_pharmacies(df):
        # Define column names and data types
        df.columns = ['id', 'chain']
        df['id'] = df['id'].astype(str)
        df['chain'] = df['chain'].astype(str)

        return df

    @staticmethod
    def get_df_reverts(df):
        # Define column names and data types
        df.columns = ['id', 'claim_id', 'timestamp']
        df['id'] = df['id'].astype(str)
        df['claim_id'] = df['claim_id'].astype(str)
        # Convert 'timestamp' column to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        return df

    def get_path(self):
        path = dict(
            claims=self.claims_path,
            pharmacies=self.pharmacies_path,
            reverts=self.reverts_path
        )[self.tablename]

        return path

    def run(self, df):
        if self.tablename == "claims":
            df = self.get_df_claims(df)
        if self.tablename == "pharmacies":
            df = self.get_df_pharmacies(df)
        if self.tablename == "revrets":
            df = self.get_df_reverts(df)

        # Create a DuckDB database connection
        con = duckdb.connect(database=self.db_path, read_only=False)

        # Load DataFrame into DuckDB
        con.execute(f"DROP TABLE IF EXISTS {self.tablename}")
        con.execute(f"CREATE TABLE {self.tablename} AS SELECT * FROM df")

        print(f"=====> {self.tablename} table created successfully")
