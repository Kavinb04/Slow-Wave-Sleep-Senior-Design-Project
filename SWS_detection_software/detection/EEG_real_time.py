import numpy as np
import collections
import mne
from scipy.signal import butter, sosfilt, sosfilt_zi

# ── Parameters ─────────────────────────────────────────
FILTER_LOW = 0.25
FILTER_HIGH = 4.0

DEFAULT_THRESHOLD = -80.0
MIN_NEG_DURATION_S = 0.15
MAX_NEG_DURATION_S = 2.0
MIN_PEAK_UV = -50.0

PEAK_CONFIRM = 3

# Time window
START_TIME = 8 * 3600
END_TIME = 9 * 3600


# ── Bandpass Filter ────────────────────────────────────
class BandpassFilter:
    def __init__(self, sf):
        nyq = sf / 2.0
        sos = butter(4, [FILTER_LOW / nyq, FILTER_HIGH / nyq],
                     btype='band', output='sos')
        self.sos = sos
        self.zi = sosfilt_zi(sos) * 0.0

    def __call__(self, sample):
        out, self.zi = sosfilt(self.sos, [sample], zi=self.zi)
        return float(out[0])


# ── Detector ───────────────────────────────────────────
class Detector:
    def __init__(self, sf):
        self.sf = sf
        self.filt = BandpassFilter(sf)

        self.buffer = collections.deque(maxlen=int(10 * sf))

        self.threshold = DEFAULT_THRESHOLD
        self.last_thresh_idx = 0

        self.state = 'WAITING'
        self.track_peak = 0.0
        self.track_start_idx = 0
        self.rise_count = 0
        self.prev = 0.0

        self.n_slow_waves = 0
        self.n_artifacts = 0

    def process(self, raw_uv, idx):
        sample = self.filt(raw_uv)
        self.buffer.append(sample)

        # adaptive threshold
        self.threshold = DEFAULT_THRESHOLD

        if self.state == 'WAITING':
            if (self.prev > sample) and (sample < -35):
                self.state = 'TRACKING'
                self.track_peak = sample
                self.track_start_idx = idx
                self.rise_count = 0

        elif self.state == 'TRACKING':
            if sample < self.track_peak:
                self.track_peak = sample
                self.rise_count = 0
            elif sample > self.prev:
                self.rise_count += 1
                if self.rise_count >= PEAK_CONFIRM:
                    self._evaluate(idx)

        self.prev = sample

    def _evaluate(self, idx):
        duration = (idx - self.track_start_idx) / self.sf
        peak = self.track_peak

        # slow wave criteria
        if duration < MIN_NEG_DURATION_S or duration > MAX_NEG_DURATION_S:
            self.n_artifacts += 1
            self.state = 'WAITING'
            return

        if peak > MIN_PEAK_UV:
            self.n_artifacts += 1
            self.state = 'WAITING'
            return

        self.n_slow_waves += 1
        self.state = 'WAITING'


# ── Run Detection ──────────────────────────────────────
def run_detection():
    edf_path = "SC4001E0-PSG.edf"
    channel = "EEG Fpz-Cz"

    raw = mne.io.read_raw_edf(edf_path, preload=True, verbose=False)
    raw.pick([channel])

    sf = raw.info['sfreq']
    signal = raw.get_data(units='uV')[0]

    detector = Detector(sf)

    start_idx = int(START_TIME * sf)
    end_idx = int(END_TIME * sf)

    print(f"Running from {START_TIME}s to {END_TIME}s\n")

    for i in range(start_idx, min(end_idx, len(signal))):
        detector.process(signal[i], i)

    print("\nRESULTS")
    print(f"Slow waves detected: {detector.n_slow_waves}")
    print(f"Rejected (artifacts): {detector.n_artifacts}")


# ── Main ───────────────────────────────────────────────
if __name__ == "__main__":
    run_detection()