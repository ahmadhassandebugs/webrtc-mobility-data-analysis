#!/usr/bin/env python3

##########################################################################
########## script for processing webrtc client and server logs ###########
##########################################################################
import os
import pandas as pd
import glob

from utils.context import data_dir, data_processed_dir
from helpers.webrtc import get_client_video_stats, get_server_video_stats

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
data = []
for idx, row in summary_df.iterrows():
    for op in OPS:
        client_file = glob.glob(os.path.join(CLIENT_FOLDER, f"{op}{row['run']}-*.csv"))
        server_file = glob.glob(os.path.join(SERVER_FOLDER, f"{op}{row['run']}-*.csv"))
        assert len(client_file) == 1 and len(server_file) == 1, f"Error: {client_file} {server_file}"
        client_file = client_file[0]
        server_file = server_file[0]
        client_df = pd.read_csv(client_file, low_memory=False)
        server_df = pd.read_csv(server_file, low_memory=False)
        client_stats = get_client_video_stats(client_df)
        server_stats = get_server_video_stats(server_df)
        client_stats["op"] = op
        client_stats["run"] = row["run"]
        client_stats["mode"] = row["mode"]
        client_stats["side"] = "client"
        server_stats["op"] = op
        server_stats["run"] = row["run"]
        server_stats["mode"] = row["mode"]
        server_stats["side"] = "server"
        data.append(client_stats)
        data.append(server_stats)

# save the data to a csv file
df = pd.DataFrame(data)
cols = ["run", "mode", "op", "side"] + [col for col in df.columns if col not in ["run", "mode", "op", "side"]]
df = df[cols]
df = df.sort_values(by=["run", "mode", "op", "side"])
df.to_csv(os.path.join(PROCESSED_DATA_FOLDER, "webrtc_stats.csv"), index=False)

print("Complete../")
