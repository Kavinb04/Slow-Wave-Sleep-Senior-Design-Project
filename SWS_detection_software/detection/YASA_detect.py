import mne
import yasa
import numpy as np

# ── File path ─────────────────────────────────────────
PSG_PATH = "SC4001E0-PSG.edf"
START_TIME = 8 * 3600
END_TIME   = 9 * 3600

WINDOW_SEC = 30   # sliding window size
STEP_SEC   = 1    # step every 1 second

# Stage thresholds (slow waves per 30s window)
STAGE3_MIN = 1    # ≥1 slow wave  → Stage 3
STAGE4_MIN = 4    # ≥4 slow waves → Stage 4

print("Loading EDF...")
raw = mne.io.read_raw_edf(PSG_PATH, preload=True, verbose=False)
eeg_name = "EEG Fpz-Cz"
raw.pick([eeg_name])
sf   = raw.info["sfreq"]
data = raw.get_data(units="uV")[0]

# Crop to time window of interest
start_idx = int(START_TIME * sf)
end_idx   = int(END_TIME   * sf)
data = data[start_idx:end_idx]

print(f"Channel      : {eeg_name}")
print(f"Sampling rate: {sf} Hz")
print(f"Signal length: {len(data)/sf:.2f} s\n")

# ── Sliding window ─────────────────────────────────────
total_samples = len(data)
win_samples   = int(WINDOW_SEC * sf)
step_samples  = int(STEP_SEC   * sf)

sw = yasa.sw_detect(data, sf=sf)
sw_onsets = sw["Start"].values

for win_start_samp in range(0, total_samples - win_samples + 1, step_samples):
    win_start_sec = win_start_samp / sf
    win_end_sec   = win_start_sec + WINDOW_SEC

    # Count slow waves whose onset falls inside this window
    count = int(np.sum((sw_onsets >= win_start_sec) & (sw_onsets < win_end_sec)))

    # Determine sleep stage
    if count >= STAGE4_MIN:
        stage = "Stage 4"
    elif count >= STAGE3_MIN:
        stage = "Stage 3"
    else:
        continue   # not Stage 3 or 4 — skip printing

    # Absolute timestamp in the recording
    abs_sec = START_TIME + win_start_sec + WINDOW_SEC   # label at window end
    h = int(abs_sec // 3600)
    m = int((abs_sec % 3600) // 60)
    s = int(abs_sec % 60)

    print(f"{h:02d}:{m:02d}:{s:02d}                   {count:>8}  {stage}")