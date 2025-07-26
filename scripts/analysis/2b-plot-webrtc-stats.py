#!/usr/bin/env python3

##########################################################################
########## script for plotting webrtc client and server data #############
##########################################################################
import os
import pandas as pd
import glob
import matplotlib.pyplot as plt
import numpy as np

from utils.context import data_dir, data_processed_dir, plot_dir
from utils.plotting import plotme
from helpers.webrtc import extract_video_plotting_data

## CONFIG
EXPR_FOLDER = os.path.join("july25-campaign", "testing")
DATA_FOLDER = os.path.join(data_dir, EXPR_FOLDER)
CLIENT_FOLDER = os.path.join(DATA_FOLDER, "client")
SERVER_FOLDER = os.path.join(DATA_FOLDER, "server")
PROCESSED_DATA_FOLDER = os.path.join(data_processed_dir, EXPR_FOLDER)
SUMMARY_FILE = os.path.join(DATA_FOLDER, "summary.txt")
# OPS = ["att", "tmb", "vzw"]
OPS = ["test"]

## PLOTTING

# read the summary file
summary_df = pd.read_csv(SUMMARY_FILE, sep=",")

# Process experiments one by one
for idx, row in summary_df.iterrows():
    for op in OPS:
        client_file = glob.glob(os.path.join(CLIENT_FOLDER, f"{op}{row['run']}-*.csv"))
        server_file = glob.glob(os.path.join(SERVER_FOLDER, f"{op}{row['run']}-*.csv"))
        
        if len(client_file) == 1 and len(server_file) == 1:
            client_file = client_file[0]
            server_file = server_file[0]
            
            # Load data
            client_df = pd.read_csv(client_file, low_memory=False)
            server_df = pd.read_csv(server_file, low_memory=False)
            
            # Extract plotting data
            client_plot_data = extract_video_plotting_data(client_df, is_server=False)
            server_plot_data = extract_video_plotting_data(server_df, is_server=True)
            
            # Create figure with 2 subplots for this experiment
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Plot client data (left subplot)
            ax1.set_title(f'Client - {op.upper()} {row["mode"]} Run {row["run"]}', fontsize=12)
            ax1.set_xlabel('Frame Delay (ms)', fontsize=10)
            ax1.set_ylabel('Video Bitrate (Mbps)', fontsize=10)
            ax1.grid(True, alpha=0.3)
            
            # Plot inbound data
            if client_plot_data["inbound"]["bitrates"]:
                ax1.scatter(client_plot_data["inbound"]["frame_delays"], 
                           client_plot_data["inbound"]["bitrates"], 
                           alpha=0.6, s=20, label='Inbound', color='blue')
            
            # Plot outbound data
            if client_plot_data["outbound"]["bitrates"]:
                ax1.scatter(client_plot_data["outbound"]["frame_delays"], 
                           client_plot_data["outbound"]["bitrates"], 
                           alpha=0.6, s=20, label='Outbound', color='red')
            
            ax1.legend()
            
            # Plot server data (right subplot)
            ax2.set_title(f'Server - {op.upper()} {row["mode"]} Run {row["run"]}', fontsize=12)
            ax2.set_xlabel('Frame Delay (ms)', fontsize=10)
            ax2.set_ylabel('Video Bitrate (Mbps)', fontsize=10)
            ax2.grid(True, alpha=0.3)
            
            # Plot inbound data
            if server_plot_data["inbound"]["bitrates"]:
                ax2.scatter(server_plot_data["inbound"]["frame_delays"], 
                           server_plot_data["inbound"]["bitrates"], 
                           alpha=0.6, s=20, label='Inbound', color='blue')
            
            # Plot outbound data
            if server_plot_data["outbound"]["bitrates"]:
                ax2.scatter(server_plot_data["outbound"]["frame_delays"], 
                           server_plot_data["outbound"]["bitrates"], 
                           alpha=0.6, s=20, label='Outbound', color='red')
            
            ax2.legend()
            
            # Adjust layout
            plt.tight_layout()
            
            # Save the plot for this experiment
            plot_path = os.path.join(plot_dir, EXPR_FOLDER)
            os.makedirs(plot_path, exist_ok=True)
            plotme(plt, f"2b-{op}{row['run']}", "video_bitrate_vs_frame_delay", plot_path=plot_path, show_flag=False, ignore_pdf=True)
            
            plt.close()  # Close the figure to free memory

print("Plotting complete!") 