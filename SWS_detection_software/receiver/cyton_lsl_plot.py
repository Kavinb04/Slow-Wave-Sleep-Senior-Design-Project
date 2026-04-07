import os
import time
import threading
import numpy as np
import matplotlib.pyplot as plt
import traceback

# Improve LSL reliability on Windows
os.environ["LSLAPICFG"] = '{"allow_ipv6": false}'

from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
from pylsl import StreamInfo, StreamOutlet, StreamInlet, resolve_byprop

# -----------------------------
# CONFIG
# -----------------------------
COM_PORT = "COM3"

# From your terminal, channels 1 and 3 (0-indexed) have real signals.
# Channels showing ~187500 uV are disconnected/floating — avoid those.
CHANNEL_INDEX = 1

BUFFER_SECONDS = 10
DEBUG_PRINT_EVERY = 250

# 187500 uV is the exact Cyton ADC rail value (disconnected pin).
# Filter those out but keep real (possibly large) EEG/EMG signals.
RAIL_VALUE = 187500.0
RAIL_TOLERANCE = 100.0  # treat anything within +/-100 uV of rail as disconnected


# -----------------------------
# PRODUCER: Cyton -> LSL  (runs in background thread)
# -----------------------------
def start_cyton_lsl_stream(stop_event):
    board = None
    try:
        params = BrainFlowInputParams()
        params.serial_port = COM_PORT

        board_id = BoardIds.CYTON_BOARD.value
        board = BoardShim(board_id, params)

        sf = BoardShim.get_sampling_rate(board_id)
        eeg_channels = BoardShim.get_eeg_channels(board_id)

        print(f"[Producer] EEG channels: {eeg_channels}")
        print(f"[Producer] Sample rate: {sf} Hz")
        print(f"[Producer] Opening port: {COM_PORT}")

        info = StreamInfo(
            name="Cyton_EEG",
            type="EEG",
            channel_count=len(eeg_channels),
            nominal_srate=sf,
            channel_format="float32",
            source_id="cyton_stream"
        )

        chns = info.desc().append_child("channels")
        for ch in eeg_channels:
            chn = chns.append_child("channel")
            chn.append_child_value("label", f"EEG{ch}")

        outlet = StreamOutlet(info)
        print("[Producer] LSL outlet created")

        board.prepare_session()
        time.sleep(1)
        board.start_stream()
        print("[Producer] Streaming started")

        sample_counter = 0

        while not stop_event.is_set():
            data = board.get_board_data()
            if data is None or data.shape[1] == 0:
                time.sleep(0.01)
                continue

            eeg = data[eeg_channels, :].astype(np.float32)
            sample_counter += eeg.shape[1]

            if sample_counter % DEBUG_PRINT_EVERY < eeg.shape[1]:
                print(f"[Producer] Frame: {eeg.shape}, first sample (uV): {eeg[:, 0]}")

            for i in range(eeg.shape[1]):
                outlet.push_sample(eeg[:, i].tolist())

            time.sleep(0.005)

    except Exception:
        print("[Producer] Exception:")
        traceback.print_exc()
    finally:
        if board is not None:
            try:
                board.stop_stream()
                board.release_session()
                print("[Producer] Clean shutdown")
            except Exception:
                pass


# -----------------------------
# CONSUMER: LSL -> Plot  (runs on MAIN thread)
# -----------------------------
def start_plot(stop_event):
    print("[Consumer] Looking for LSL stream...")

    streams = []
    while not streams and not stop_event.is_set():
        streams = resolve_byprop('name', 'Cyton_EEG', timeout=2)
        if not streams:
            print("[Consumer] Still waiting for stream...")
            time.sleep(1)

    if stop_event.is_set():
        return

    print("[Consumer] Stream found!")

    inlet = StreamInlet(streams[0])
    info = inlet.info()

    sf = int(info.nominal_srate())
    n_channels = info.channel_count()
    ch_idx = CHANNEL_INDEX if CHANNEL_INDEX < n_channels else 0

    print(f"[Consumer] Connected: {info.name()}, channels={n_channels}, sf={sf}")
    print(f"[Consumer] Plotting channel index {ch_idx}")

    buffer_len = int(BUFFER_SECONDS * sf)
    buf = np.full(buffer_len, np.nan, dtype=np.float32)
    buf_filled = 0

    # --- Plot setup (safe: called on main thread) ---
    plt.ion()
    fig, ax = plt.subplots(figsize=(12, 4))
    x = np.linspace(-BUFFER_SECONDS, 0, buffer_len)
    line, = ax.plot(x, np.zeros(buffer_len), lw=1, color='steelblue')
    ax.set_xlim(-BUFFER_SECONDS, 0)
    ax.set_ylim(-200, 200)
    ax.set_title(f"Live EEG - channel index {ch_idx}  (change CHANNEL_INDEX in config)")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("EEG (uV)")
    fig.tight_layout()

    last_update = time.time()

    try:
        while not stop_event.is_set():
            # Drain the entire inlet buffer each iteration
            samples, _ = inlet.pull_chunk(timeout=0.05, max_samples=512)

            if samples is None or len(samples) == 0:
                continue

            samples = np.array(samples)  # (n_samples, n_channels)

            if samples.shape[1] <= ch_idx:
                continue

            vals = samples[:, ch_idx]

            # Filter out: NaN, inf, and railed (disconnected) values
            mask = (
                np.isfinite(vals) &
                (np.abs(vals - RAIL_VALUE) > RAIL_TOLERANCE) &
                (np.abs(vals + RAIL_VALUE) > RAIL_TOLERANCE)
            )
            vals = vals[mask]

            if len(vals) == 0:
                continue

            buf_filled = min(buf_filled + len(vals), buffer_len)
            buf = np.roll(buf, -len(vals))
            buf[-len(vals):] = vals

            # Redraw at ~20 fps
            if time.time() - last_update > 0.05:
                valid = buf[~np.isnan(buf)]
                line.set_ydata(np.nan_to_num(buf))

                if buf_filled > sf and len(valid) > 0:
                    ymin, ymax = np.min(valid), np.max(valid)
                    margin = max((ymax - ymin) * 0.2, 10)
                    ax.set_ylim(ymin - margin, ymax + margin)

                fig.canvas.draw()
                fig.canvas.flush_events()
                last_update = time.time()

    except KeyboardInterrupt:
        print("[Consumer] Stopping")
    finally:
        plt.ioff()
        plt.close(fig)
        print("[Consumer] Exit")


# -----------------------------
# MAIN
# -----------------------------
if __name__ == "__main__":
    stop_event = threading.Event()

    # Producer runs in background thread
    producer_thread = threading.Thread(
        target=start_cyton_lsl_stream,
        args=(stop_event,),
        daemon=True
    )
    producer_thread.start()

    # Give the board and LSL outlet time to initialize
    print("[Main] Waiting for producer to initialize...")
    time.sleep(4)

    # Consumer (plot) runs on main thread -- required by matplotlib/Tkinter
    try:
        start_plot(stop_event)
    except KeyboardInterrupt:
        pass
    finally:
        print("[Main] Shutting down...")
        stop_event.set()
        producer_thread.join(timeout=5)
        print("[Main] Done")