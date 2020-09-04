# This file downloads from the API to a database
# Slightly messy due to transfer from a Jupyter Notebook
# Copy fragments of this to a notebook to see the data contained in each step
# Not included in requirements.txt since this file is not expected to run with the bot

import requests
import json
import pandas as pd
import sqlite3


# Creates a dataframe for the list of courses given a subject string, s
# Requires 1 call to the API, should any courses be returned
def make_df(s: str):
    req = requests.get(url="https://api.uwaterloo.ca/v2/courses/" + s + ".json?key=YOUR_API_KEY_HERE")
    return pd.DataFrame.from_dict(json.loads(req.text)["data"])


# Import a list of all course code prefixes
req = requests.get("https://api.uwaterloo.ca/v2/codes/subjects.json?key=YOUR_API_KEY_HERE")
subject_codes = json.loads(req.text)
# The data is under the 'data' key by default
subject_codes = subject_codes["data"]

subject_df = pd.DataFrame.from_dict(subject_codes)
subject_list = subject_df["subject"].tolist()

# Create a master list of dataframes for each subject, and remove all empty ones
dfs = [make_df(subject) for subject in subject_list]
dfs = [df for df in dfs if len(df) > 0]

# Join the dataframes all together and create a new column for searching
df = pd.concat(dfs)
df["searchby"] = df["subject"] + df["catalog_number"]

# Create database from the finished dataframe
conn = sqlite3.connect("courses.db")
df.to_sql(name="courses", con=conn)