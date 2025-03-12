#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ==============================================================================
# EDA - Exploratory Data Analysis
# ==============================================================================
# Created by: laercio.serra@gmail.com
# Created at: 03/11/2025
# ==============================================================================

# Defining libraries
import os

import duckdb
import pandas as pd
from ydata_profiling.profile_report import ProfileReport

APP_PATH = os.path.dirname(os.path.abspath(__file__))


def data_profiling():
    """Claims Data profile"""

    # Create a DuckDB database connection
    db_path = os.path.join(APP_PATH, "database/hippo.db")
    con = duckdb.connect(database=db_path, read_only=False)

    # Execute the query and read it into a Pandas DataFrame
    query = f"SELECT * FROM claims"
    df = pd.read_sql(query, con)

    if len(df) > 0:
        print(f"-----> Generating Profile Report")
        profile = ProfileReport(df, explorative=True, title="Hippo Claims Data Profile")

        # Save report as an HTML file
        print(f"-----> Exporting Profile Report")
        profile.to_file("claims_table_report.html")

        print("✅ Report generated successfully: claims_table_report.html")


if __name__ == "__main__":
    data_profiling()
