import mne
import yasa

# ── File path ─────────────────────────────────────────
PSG_PATH = "SC4001E0-PSG.edf"

# Match your detector window (IMPORTANT)
START_TIME = 8 * 3600
END_TIME = 9 * 3600

print("Loading EDF...")
raw = mne.io.read_raw_edf(PSG_PATH, preload=True, verbose=False)

eeg_name = "EEG Fpz-Cz"
raw.pick([eeg_name])

sf = raw.info["sfreq"]
data = raw.get_data(units="uV")[0]

# Apply SAME time window as your detector
start_idx = int(START_TIME * sf)
end_idx = int(END_TIME * sf)
data = data[start_idx:end_idx]

print(f"Using channel: {eeg_name}") 
print(f"Sampling rate: {sf} Hz")
print(f"Window length: {len(data)/sf:.2f} sec\n")

print("Running YASA slow wave detection...\n")

sw = yasa.sw_detect(data, sf=sf)

sw_summary = sw.summary()

print("YASA RESULTS")
print(f"Slow waves detected: {len(sw_summary)}")