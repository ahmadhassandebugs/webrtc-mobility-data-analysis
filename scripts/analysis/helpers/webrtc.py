import pandas as pd


def get_client_video_stats(df, mode="vca"):
    # df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    # total_time_secs = (df["timestamp"].max() - df["timestamp"].min()).total_seconds()
    # total_bytes_sent = df["bytes_sent"].max()
    # total_bytes_received = df["bytes_received"].max()
    # rtt_ms = df["round_trip_time"].mean() * 1000
    # jitter_ms = df["jitter_buffer_delay"].mean()
    # fps = df["fps"].mean()
    # frame_delay_ms = df["frame_delay_ms"].mean()
    # packets_lost_total = df["packets_lost_total"].sum()
    # packets_received = df["packets_received"].max()
    # packets_sent = df["packets_sent"].max()
    # stats = {
    #     "time_secs": total_time_secs,
    #     "send_bitrate_mbps": (total_bytes_sent * 8) / (total_time_secs * 1e6),
    #     "receive_bitrate_mbps": (total_bytes_received * 8) / (total_time_secs * 1e6),
    #     "rtt_ms": rtt_ms,
    #     "jitter_ms": jitter_ms,
    #     "fps": fps,
    #     "frame_delay_ms": frame_delay_ms,
    #     "packets_lost_total": packets_lost_total
    # }
    return parse_csv(df)


def get_server_video_stats(df, mode="vca"):
    # df["vout_timestamp"] = pd.to_datetime(df["vout_timestamp"], unit="ms")
    # df["vin_timestamp"] = pd.to_datetime(df["vin_timestamp"], unit="ms")
    # total_time_vout_secs = (df["vout_timestamp"].max() - df["vout_timestamp"].min()).total_seconds()
    # total_time_vin_secs = (df["vin_timestamp"].max() - df["vin_timestamp"].min()).total_seconds()
    # total_bytes_sent = df["vout_bytesSent"].max()
    # total_packets_sent = df["vout_packetsSent"].max()
    # total_packets_received = df["vin_packetsReceived"].max()
    # total_receive_packets_lost = df["vin_packetsLost"].max()
    # receive_jitter = df["vin_jitter"].mean()
    # receive_rtt = df["vin_roundTripTime"].mean() * 1000
    # stats = {
    #     "send_time_secs": total_time_vout_secs,
    #     "send_bitrate_mbps": (total_bytes_sent * 8) / (total_time_vout_secs * 1e6),
    #     "receive_time_secs": total_time_vin_secs,
    #     "receive_jitter_ms": receive_jitter,
    #     "receive_rtt_ms": receive_rtt,
    # }
    return parse_csv(df)


def parse_csv(df):
    """
    Reconstruct original values from vertically stacked CSV format.
    Calculates statistics separately for audio and video streams.
    
    Args:
        df: DataFrame with columns:
            - timestamp
            - api_timestamp
            - stream_type
            - direction
            - bytes
            - packets
            - fps
            - rtt_ms
            - jitter_ms
            - packets_lost
            - frame_delay_ms
            - fraction_lost
    
    Returns:
        Dictionary with reconstructed values, separated by audio/video
    """
    # Convert timestamps
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["api_timestamp"] = pd.to_datetime(df["api_timestamp"].astype(int), unit="ms")
    
    # Calculate total time
    total_time_secs = (df["timestamp"].max() - df["timestamp"].min()).total_seconds()
    
    # Separate audio and video metrics
    audio_df = df[df["stream_type"] == "audio"]
    video_df = df[df["stream_type"] == "video"]
    
    # Handle transport rows (not separated by audio/video)
    transport_df = df[df["stream_type"] == "transport"]
    transport_inbound = transport_df[transport_df["direction"] == "inbound"]
    transport_outbound = transport_df[transport_df["direction"] == "outbound"]
    
    # Combine transport rows
    transport_combined = pd.DataFrame({
        'timestamp': transport_outbound['timestamp'],
        'api_timestamp': transport_outbound['api_timestamp'],
        'bytes_sent': transport_outbound['bytes'],
        'bytes_received': transport_inbound['bytes'],
        'packets_sent': transport_outbound['packets'],
        'packets_received': transport_inbound['packets']
    })
    
    def calculate_stream_stats(stream_df):
        # Separate different types
        inbound = stream_df[stream_df["direction"] == "inbound"]
        outbound = stream_df[stream_df["direction"] == "outbound"]
        remote_inbound = stream_df[stream_df["direction"] == "inbound_remote"]
        remote_outbound = stream_df[stream_df["direction"] == "outbound_remote"]
        
        return {
            # Outbound metrics
            "outbound_bytes": outbound["bytes"].max(),
            "outbound_packets": outbound["packets"].max(),
            "outbound_fps": outbound["fps"].mean(),
            
            # Inbound metrics
            "inbound_bytes": inbound["bytes"].max(),
            "inbound_packets": inbound["packets"].max(),
            "inbound_packets_lost": inbound["packets_lost"].sum(),
            "inbound_jitter": inbound["jitter_ms"].mean(),
            "inbound_fps": inbound["fps"].mean(),
            "inbound_frame_delay": inbound["frame_delay_ms"].mean(),
            
            # Remote inbound metrics
            "remote_inbound_packets": remote_inbound["packets"].max(),
            "remote_inbound_packets_lost": remote_inbound["packets_lost"].sum(),
            "remote_inbound_jitter": remote_inbound["jitter_ms"].mean(),
            "remote_inbound_rtt": remote_inbound["rtt_ms"].mean(),
            "remote_inbound_fraction_lost": remote_inbound["fraction_lost"].mean(),
            
            # Remote outbound metrics
            "remote_outbound_bytes": remote_outbound["bytes"].max(),
            "remote_outbound_packets": remote_outbound["packets"].max(),
            
            # Derived metrics
            "send_bitrate_mbps": (outbound["bytes"].max() * 8) / (total_time_secs * 1e6),
            "receive_bitrate_mbps": (inbound["bytes"].max() * 8) / (total_time_secs * 1e6),
        }
    
    # Calculate stats for both audio and video
    audio_stats = calculate_stream_stats(audio_df)
    video_stats = calculate_stream_stats(video_df)
    
    # Combine all stats with prefixes
    stats = {
        "time_secs": total_time_secs,
        
        # Transport metrics (not separated by audio/video)
        "transport_bytes_sent": transport_combined["bytes_sent"].max(),
        "transport_bytes_received": transport_combined["bytes_received"].max(),
        "transport_packets_sent": transport_combined["packets_sent"].max(),
        "transport_packets_received": transport_combined["packets_received"].max(),
        # Derived metrics
        "combined_send_bitrate_mbps": (transport_combined["bytes_sent"].max() * 8) / (total_time_secs * 1e6),
        "combined_recv_bitrate_mbps": (transport_combined["bytes_received"].max() * 8) / (total_time_secs * 1e6),
    }
    
    # Add audio stats with prefix
    for key, value in audio_stats.items():
        stats[f"audio_{key}"] = value
    
    # Add video stats with prefix
    for key, value in video_stats.items():
        stats[f"video_{key}"] = value
    
    return stats
