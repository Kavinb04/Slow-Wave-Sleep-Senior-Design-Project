import numpy as np
import collections
import mne
import yasa
from scipy.signal import butter, sosfilt, sosfilt_zi
import warnings
import sys
import os

# ── Parameters ─────────────────────────────────────────
FILTER_LOW          = 0.25
FILTER_HIGH         = 4.0
MIN_NEG_DURATION_S  = 0.15
MAX_NEG_DURATION_S  = 2.0
MIN_PEAK_UV         = -60.0
PEAK_CONFIRM        = 3
POST_WAVE_PAUSE_S   = 1.5

WINDOW_SEC          = 30     # ← BACK TO 30s
YASA_CHECK_EVERY_S  = 1.0    # ← BACK TO 1s
YASA_MIN_WAVES      = 5

START_TIME          = 8 * 3600
END_TIME            = 9 * 3600


# ── Bandpass Filter ────────────────────────────────────
class BandpassFilter:
    def __init__(self, sf):
        nyq      = sf / 2.0
        sos      = butter(4, [FILTER_LOW / nyq, FILTER_HIGH / nyq],
                          btype='band', output='sos')
        self.sos = sos
        self.zi  = sosfilt_zi(sos) * 0.0

    def __call__(self, sample):
        out, self.zi = sosfilt(self.sos, [sample], zi=self.zi)
        return float(out[0])


# ── YASA Gate (ONLY change: silence output) ─────────────
class YasaGate:
    def __init__(self, sf):
        self.sf             = sf
        self.window_samples = int(WINDOW_SEC * sf)
        self.check_every    = int(YASA_CHECK_EVERY_S * sf)
        self.raw_buffer     = collections.deque(maxlen=self.window_samples)
        self.is_open        = False
        self.samples_since_check = 0

    def update(self, raw_uv):
        self.raw_buffer.append(raw_uv)
        self.samples_since_check += 1

        if self.samples_since_check < self.check_every:
            return self.is_open

        self.samples_since_check = 0

        if len(self.raw_buffer) < self.window_samples:
            return self.is_open

        window = np.array(self.raw_buffer)

        # 🔥 SILENCE EVERYTHING FROM YASA
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')

        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                sw = yasa.sw_detect(window, self.sf, verbose='ERROR')
            n_waves = len(sw.summary()) if sw is not None else 0
        except:
            n_waves = 0

        sys.stdout.close()
        sys.stderr.close()
        sys.stdout = old_stdout
        sys.stderr = old_stderr

        # ← YOUR ORIGINAL SIMPLE LOGIC
        self.is_open = n_waves >= YASA_MIN_WAVES

        return self.is_open


# ── Real-Time Detector (UNCHANGED except print) ─────────
class Detector:
    def __init__(self, sf):
        self.sf              = sf
        self.filt            = BandpassFilter(sf)
        self.gate            = YasaGate(sf)

        self.state           = 'WAITING'
        self.track_peak      = 0.0
        self.track_start_idx = 0
        self.rise_count      = 0
        self.prev            = 0.0
        self.pause_until_idx = 0

    def process(self, raw_uv, idx):
        t = idx / self.sf

        gate_open = self.gate.update(raw_uv)
        sample = self.filt(raw_uv)

        if self.state == 'PAUSED':
            if idx >= self.pause_until_idx:
                self.state = 'WAITING'
            self.prev = sample
            return

        if self.state == 'WAITING':
            if self.prev >= -35.0 and sample < -35.0:
                self.state           = 'TRACKING'
                self.track_peak      = sample
                self.track_start_idx = idx
                self.rise_count      = 0

        elif self.state == 'TRACKING':
            if sample < self.track_peak:
                self.track_peak = sample
                self.rise_count = 0
            elif sample > self.prev:
                self.rise_count += 1
                if self.rise_count >= PEAK_CONFIRM:
                    self._evaluate(idx, t, gate_open)

        self.prev = sample

    def _evaluate(self, idx, t, gate_open):
        duration = (idx - self.track_start_idx) / self.sf
        peak     = self.track_peak

        if not (MIN_NEG_DURATION_S <= duration <= MAX_NEG_DURATION_S):
            self.state = 'WAITING'
            return

        if peak > MIN_PEAK_UV:
            self.state = 'WAITING'
            return

        if gate_open:
            print(format_time(t))   # ← ONLY OUTPUT

        self.pause_until_idx = idx + int(POST_WAVE_PAUSE_S * self.sf)
        self.state           = 'PAUSED'


# ── Helpers ────────────────────────────────────────────
def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    return f"{h}:{m:02d}:{s:02d}"


# ── Run ────────────────────────────────────────────────
def run_detection():
    raw = mne.io.read_raw_edf("SC4001E0-PSG.edf", preload=True, verbose=False)

    # ← CORRECT CHANNEL
    raw.pick(["EEG Fpz-Cz"])

    sf     = raw.info['sfreq']
    signal = raw.get_data(units='uV')[0]

    detector  = Detector(sf)
    start_idx = int(START_TIME * sf)
    end_idx   = int(END_TIME * sf)

    for i in range(start_idx, min(end_idx, len(signal))):
        detector.process(signal[i], i)


if __name__ == "__main__":
    run_detection()