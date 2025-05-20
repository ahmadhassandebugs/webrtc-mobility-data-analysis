import pandas as pd


def get_client_video_stats(df, mode="vca"):
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    total_time_secs = (df["timestamp"].max() - df["timestamp"].min()).total_seconds()
    total_bytes_sent = df["bytes_sent"].sum()
    total_bytes_received = df["bytes_received"].sum()
    rtt_ms = df["round_trip_time"].mean() * 1000
    jitter_ms = df["jitter_buffer_delay"].mean() * 1000
    fps = df["fps"].mean()
    frame_delay_ms = df["frame_delay_ms"].mean()
    packets_lost_total = df["packets_lost_total"].sum()
    packets_received = df["packets_received"].sum()
    packets_sent = df["packets_sent"].sum()
    stats = {
        "time_secs": total_time_secs,
        "send_bitrate_mbps": (total_bytes_sent * 8) / (total_time_secs * 1e6),
        "receive_bitrate_mbps": (total_bytes_received * 8) / (total_time_secs * 1e6),
        "rtt_ms": rtt_ms,
        "jitter_ms": jitter_ms,
        "fps": fps,
        "frame_delay_ms": frame_delay_ms,
        "packets_lost_total": packets_lost_total
    }
    return stats


def get_server_video_stats(df, mode="vca"):
    df["vout_timestamp"] = pd.to_datetime(df["vout_timestamp"], unit="ms")
    df["vin_timestamp"] = pd.to_datetime(df["vin_timestamp"], unit="ms")
    total_time_vout_secs = (df["vout_timestamp"].max() - df["vout_timestamp"].min()).total_seconds()
    total_time_vin_secs = (df["vin_timestamp"].max() - df["vin_timestamp"].min()).total_seconds()
    total_bytes_sent = df["vout_bytesSent"].sum()
    total_packets_sent = df["vout_packetsSent"].sum()
    total_packets_received = df["vin_packetsReceived"].sum()
    total_receive_packets_lost = df["vin_packetsLost"].sum()
    receive_jitter = df["vin_jitter"].mean() * 1000
    receive_rtt = df["vin_roundTripTime"].mean() * 1000
    stats = {
        "send_time_secs": total_time_vout_secs,
        "send_bitrate_mbps": (total_bytes_sent * 8) / (total_time_vout_secs * 1e6),
        "receive_time_secs": total_time_vin_secs,
        "receive_jitter_ms": receive_jitter,
        "receive_rtt_ms": receive_rtt,
    }
    return stats
