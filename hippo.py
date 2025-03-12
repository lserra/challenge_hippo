#!/usr/bin/python3
# -*- coding: utf-8 -*-

# ==============================================================================
# We work to offer the lowest possible prices on generic and branded medications,
# regardless of whether you have insurance or not.
# Patients get prescriptions with drug (ndc) and its (quantity) to be filled by
# a Pharmacy (npi). When the patient arrives at the pharmacy with the
# prescription, the pharmacist informs the (price) and submits a new claim.
# Sometimes, the consumer does not return to the pharmacy to get the drugs,
# this will generate a claim revert which should be registered by the pharmacist
# in order to revert (i.e. invalidate) that claim.
# ==============================================================================
# Created by: laercio.serra@gmail.com
# Created at: 03/11/2025
# ==============================================================================

# Defining libraries
import os

from src.goal_four import MostCommonQuantities as mcq
from src.goal_one import CreateAndPopulateTable as cpt
from src.goal_three import RecommendTopChains as rtc
from src.goal_two import CalculateMetrics as cm

APP_PATH = os.path.dirname(os.path.abspath(__file__))


def load_data(app_path):
    # Creating and loading data to pharmacies table
    cpt(app_path=app_path, tablename="pharmacies").from_csv()
    # Creating and loading data to claims table
    cpt(app_path=app_path, tablename="claims").from_json()
    # Creating and loading data to reverts table
    cpt(app_path=app_path, tablename="reverts").from_json()


def calc_metrics(app_path):
    # Creating bigtable
    cm(app_path=app_path).create_bt()
    # Calculating metrics
    df = cm(app_path=app_path).calc_metrics()
    # Writing to a JSON file
    cm(app_path=app_path).generate_json_file(df=df)


def make_recommendation(app_path):
    # Querying the data
    # Calculating average prices per chain for each drug
    # Sorting the results
    # Writing to a JSON file
    rtc(app_path=app_path).run()


def common_quantities(app_path):
    # Querying the data
    # Calculating the most common quantities prescribed for each drug
    # Writing to a JSON file
    mcq(app_path=app_path).run()


def exec_tasks():
    load_data(app_path=APP_PATH)
    calc_metrics(app_path=APP_PATH)
    make_recommendation(app_path=APP_PATH)
    common_quantities(app_path=APP_PATH)
    print("✅ Hippo process finished successfully!")


if __name__ == '__main__':
    exec_tasks()
