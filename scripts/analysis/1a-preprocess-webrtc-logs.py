#!/usr/bin/env python3

##########################################################################
########## script for processing webrtc client and server logs ###########
##########################################################################
import os
import pandas as pd
import glob

from utils.context import data_dir, data_processed_dir

## CONFIG
EXPR_FOLDER = os.path.join("may25-campaign", "testing")
DATA_FOLDER = os.path.join(data_dir, EXPR_FOLDER)
CLIENT_FOLDER = os.path.join(DATA_FOLDER, "client")
SERVER_FOLDER = os.path.join(DATA_FOLDER, "server")
PROCESSED_DATA_FOLDER = os.path.join(data_processed_dir, EXPR_FOLDER)
os.makedirs(PROCESSED_DATA_FOLDER, exist_ok=True)
SUMMARY_FILE = os.path.join(DATA_FOLDER, "summary.txt")
OPS = ["att", "tmb", "vzw"]

## PROCESSING

# read the summary file
summary_df = pd.read_csv(SUMMARY_FILE, sep=",")

# process experiments one by one
for idx, row in summary_df.iterrows():
    print(f"processing experiment {idx+1}/{len(summary_df)}")
    for op in OPS:
        client_file = glob.glob(os.path.join(CLIENT_FOLDER, f"{op}{row['run']}-*.csv"))
        server_file = glob.glob(os.path.join(SERVER_FOLDER, f"{op}{row['run']}-*.csv"))
        assert len(client_file) == 1 and len(server_file) == 1, f"Error: {client_file} {server_file}"
        client_file = client_file[0]
        server_file = server_file[0]
        print(f"  processing {client_file} and {server_file}")
