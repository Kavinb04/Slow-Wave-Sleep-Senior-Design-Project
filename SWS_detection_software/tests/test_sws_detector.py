# tests/test_sws_detector.py
import sys
import warnings
import numpy as np
import mne

sys.path.append(".")
from detection.sws_detector import SWSDetector

SAMPLE_RATE = 100

def load_real_eeg(edf_path):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        raw = mne.io.read_raw_edf(edf_path, preload=True, verbose=False)

    eeg = raw.get_data()[0] * 1e6  # V → µV
    print(f"  EEG amplitude range: {eeg.min():.1f} to {eeg.max():.1f} µV")
    print(f"  EEG std: {eeg.std():.2f} µV")
    return eeg

def test_too_short():
    detector = SWSDetector(sample_rate=SAMPLE_RATE)
    result = detector.detect(np.random.randn(100))
    assert result['is_sws'] == False
    print("PASS - too short signal")

def test_flat_signal():
    detector = SWSDetector(sample_rate=SAMPLE_RATE)
    result = detector.detect(np.zeros(30 * SAMPLE_RATE))
    assert result['is_sws'] == False
    print("PASS - flat signal")

def test_real_eeg(edf_path):
    detector = SWSDetector(sample_rate=SAMPLE_RATE)
    eeg = load_real_eeg(edf_path)

    # Known SWS segment
    start_min = 733
    end_min   = 742

    start = start_min * 60 * SAMPLE_RATE
    end   = end_min   * 60 * SAMPLE_RATE
    chunk = eeg[start:end]

    print(f"  Chunk duration: {len(chunk)/SAMPLE_RATE:.0f}s")
    result = detector.detect(chunk)
    print(f"  Slow waves found: {result['sw_count']}")

    if result['slow_waves'] is not None and result['sw_count'] > 0:
        df = result['slow_waves']
        print(f"\n  {'#':<5} {'Start (s)':<12} {'End (s)':<12} {'Duration (s)':<14} {'Abs time'}")
        print(f"  {'-'*55}")
        for i, row in df.iterrows():
            start_s   = row['Start']
            end_s     = row['End']
            duration  = end_s - start_s
            # Absolute time from start of full recording
            abs_start = (start_min * 60) + start_s
            abs_min   = int(abs_start // 60)
            abs_sec   = abs_start % 60
            print(f"  {i:<5} {start_s:<12.2f} {end_s:<12.2f} {duration:<14.2f} {abs_min}m {abs_sec:.1f}s")
    else:
        print("  No slow waves detected")

    print("\nPASS - real EEG")


def test_sliding_window(edf_path):
    detector = SWSDetector(sample_rate=SAMPLE_RATE)
    eeg = load_real_eeg(edf_path)
    window = 30 * SAMPLE_RATE
    step   =  5 * SAMPLE_RATE
    sws_windows = []

    for start in range(0, len(eeg) - window, step):
        chunk = eeg[start : start + window]
        result = detector.detect(chunk)
        if result['is_sws']:
            sws_windows.append(start / SAMPLE_RATE)

    print(f"  SWS detected in {len(sws_windows)} windows")
    if sws_windows:
        print(f"  First detection at t={sws_windows[0]:.0f}s")
    assert len(sws_windows) > 0, "No SWS detected — check thresholds"
    print("PASS - sliding window")

if __name__ == "__main__":
    EDF_PATH = "tests/sample_data/SC4001E0-PSG.edf"

    print("Running SWS detector tests...\n")
    test_too_short()
    test_flat_signal()
    test_real_eeg(EDF_PATH)
    # test_sliding_window(EDF_PATH)
    print("\nAll tests passed!") 