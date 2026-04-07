import numpy as np
import collections
import mne
import yasa
from scipy.signal import butter, sosfilt, sosfilt_zi
import warnings
import sys
import os

# ── Parameters ─────────────────────────────────────────
FILTER_LOW             = 0.5     # raised from 0.25 — reduces baseline drift
FILTER_HIGH            = 4.0

ENTRY_THRESHOLD_UV     = -25.0   # lowered from -35 — catch more trough candidates
MIN_NEG_DURATION_S     = 0.15
MAX_NEG_DURATION_S     = 2.0
MIN_PEAK_UV            = -50.0   # loosened from -60 — catch shallower valid peaks
TROUGH_DEADBAND_UV     = 5.0     # signal must rise this far above trough to count as rise
PEAK_CONFIRM           = 5       # raised from 3 — more robust uptick confirmation

POST_WAVE_PAUSE_S      = 0.8     # lowered from 1.5 — avoid missing rapid waves

WINDOW_SEC             = 30      # rolling YASA window (s)
YASA_MIN_WAVES         = 2       # lowered from 5 — less likely to drop SWS mid-bout

CHECK_INTERVAL_NO_SWS  = 1.0     # YASA check interval when NOT in SWS (s)
CHECK_INTERVAL_SWS     = 5.0     # YASA check interval when IN SWS (s)

START_TIME             = 13 * 3600
END_TIME               = 15 * 3600


# ── Bandpass Filter ────────────────────────────────────
class BandpassFilter:
    """
    Stateful causal Butterworth bandpass filter (0.5–4 Hz).
    Processes one sample at a time, maintaining filter state between calls
    so it works correctly in a streaming / real-time context.
    """
    def __init__(self, sf):
        nyq      = sf / 2.0
        sos      = butter(4, [FILTER_LOW / nyq, FILTER_HIGH / nyq],
                          btype='band', output='sos')
        self.sos = sos
        self.zi  = sosfilt_zi(sos) * 0.0

    def __call__(self, sample):
        out, self.zi = sosfilt(self.sos, [sample], zi=self.zi)
        return float(out[0])


# ── YASA Gate ──────────────────────────────────────────
class YasaGate:
    """
    Runs YASA slow-wave detection on a rolling 30-second buffer.

    Check frequency adapts to current SWS state:
      - Not in SWS → check every 1 second  (fast response to SWS onset)
      - In SWS     → check every 5 seconds (reduce CPU load, stay confirmed)

    Bug fix: samples_since_check is only reset when YASA actually runs,
    not on the early return when the buffer is not yet full. This prevents
    the gate from flickering open/closed every few seconds.

    is_open = True  → SWS confirmed, uptick detector is active
    is_open = False → waiting for SWS onset
    """
    def __init__(self, sf):
        self.sf                  = sf
        self.window_samples      = int(WINDOW_SEC * sf)
        self.raw_buffer          = collections.deque(maxlen=self.window_samples)
        self.is_open             = False
        self.samples_since_check = 0

    def update(self, raw_uv):
        self.raw_buffer.append(raw_uv)
        self.samples_since_check += 1

        # dynamic interval: fast when hunting for SWS, slower when confirmed
        check_every = int((CHECK_INTERVAL_SWS if self.is_open
                           else CHECK_INTERVAL_NO_SWS) * self.sf)

        if self.samples_since_check < check_every:
            return self.is_open

        # buffer not full yet — reset counter but don't run YASA
        if len(self.raw_buffer) < self.window_samples:
            self.samples_since_check = 0
            return self.is_open

        # ready to run YASA — reset counter
        self.samples_since_check = 0

        window = np.array(self.raw_buffer)

        # silence all YASA / MNE stdout and stderr output
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                sw = yasa.sw_detect(window, self.sf, verbose='ERROR')
            n_waves = len(sw.summary()) if sw is not None else 0
        except Exception:
            n_waves = 0
        finally:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        prev_state   = self.is_open
        self.is_open = n_waves >= YASA_MIN_WAVES

        # log state transitions only
        if self.is_open and not prev_state:
            print(f"[YASA] SWS confirmed ({n_waves} waves in window) "
                  f"— uptick detector ACTIVE")
        elif not self.is_open and prev_state:
            print(f"[YASA] SWS ended ({n_waves} waves in window) "
                  f"— uptick detector INACTIVE")

        return self.is_open


# ── Real-Time Uptick Detector ──────────────────────────
class Detector:
    """
    Sample-by-sample state machine that detects the uptick of each slow wave
    and triggers pink noise playback.

    States
    ──────
    WAITING   Listen for signal crossing below ENTRY_THRESHOLD_UV.
    TRACKING  Follow trough downward. Use a deadband above the trough minimum
              rather than requiring strictly consecutive rises — this tolerates
              the flat plateau commonly seen at real slow wave troughs without
              falsely resetting the rise counter.
    RISING    Uptick confirmed and all trough criteria met. Fire trigger
              immediately and enter PAUSED.
    PAUSED    Refractory period. All incoming samples ignored until elapsed.

    The YASA gate controls whether triggers fire:
      - Gate closed → state machine still runs (avoids cold-start lag) but
                      _on_uptick() suppresses the audio trigger.
      - Gate open   → _on_uptick() fires on every valid uptick.

    Refractory period is enforced regardless of gate state to prevent
    double-triggering on the same wave.
    """
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
        t         = idx / self.sf
        gate_open = self.gate.update(raw_uv)
        sample    = self.filt(raw_uv)

        # ── PAUSED ────────────────────────────────────────
        if self.state == 'PAUSED':
            if idx >= self.pause_until_idx:
                self.state = 'WAITING'
            self.prev = sample
            return

        # ── WAITING ───────────────────────────────────────
        if self.state == 'WAITING':
            # detect downward crossing of entry threshold
            if self.prev >= ENTRY_THRESHOLD_UV and sample < ENTRY_THRESHOLD_UV:
                self.state           = 'TRACKING'
                self.track_peak      = sample
                self.track_start_idx = idx
                self.rise_count      = 0

        # ── TRACKING ──────────────────────────────────────
        elif self.state == 'TRACKING':
            if sample < self.track_peak:
                # still descending — update trough, reset rise counter
                self.track_peak = sample
                self.rise_count = 0

            elif sample > self.track_peak + TROUGH_DEADBAND_UV:
                # signal has risen meaningfully above the trough floor —
                # count as a confirmed rising sample. The deadband prevents
                # plateau noise from stalling the counter at flat troughs.
                self.rise_count += 1

                if self.rise_count >= PEAK_CONFIRM:
                    duration = (idx - self.track_start_idx) / self.sf

                    valid_duration = MIN_NEG_DURATION_S <= duration <= MAX_NEG_DURATION_S
                    valid_peak     = self.track_peak <= MIN_PEAK_UV

                    if valid_duration and valid_peak:
                        # uptick confirmed — transition to RISING and trigger
                        self.state = 'RISING'
                        self._on_uptick(idx, t, gate_open)
                    else:
                        # criteria not met — discard, wait for next wave
                        self.state = 'WAITING'

            # if sample is between track_peak and track_peak + deadband,
            # do nothing — tolerate flat troughs without resetting rise_count

        self.prev = sample

    def _on_uptick(self, idx, t, gate_open):
        """
        Called at the moment of a confirmed wave uptick.

        In the live system, replace the print statement with your pink noise
        audio trigger, e.g.:
            audio_engine.play_pink_noise(duration_ms=50)
        """
        if gate_open:
            print(f"[TRIGGER] Uptick detected at {format_time(t)} "
                  f"— play pink noise")

        # refractory period enforced regardless of gate state
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
    print("Loading EDF...")
    raw = mne.io.read_raw_edf("SC4001E0-PSG.edf", preload=True, verbose=False)
    raw.pick(["EEG Fpz-Cz"])

    sf     = raw.info['sfreq']
    signal = raw.get_data(units='uV')[0]

    print(f"Sampling rate  : {sf} Hz")
    print(f"Window         : {START_TIME // 3600}h – {END_TIME // 3600}h")
    print(f"Filter         : {FILTER_LOW}–{FILTER_HIGH} Hz")
    print(f"Entry threshold: {ENTRY_THRESHOLD_UV} µV")
    print(f"Min peak       : {MIN_PEAK_UV} µV")
    print(f"YASA window    : {WINDOW_SEC}s | "
          f"check: {CHECK_INTERVAL_NO_SWS}s (no SWS) / "
          f"{CHECK_INTERVAL_SWS}s (SWS)\n")

    detector  = Detector(sf)
    start_idx = int(START_TIME * sf)
    end_idx   = int(END_TIME   * sf)

    for i in range(start_idx, min(end_idx, len(signal))):
        detector.process(signal[i], i)

    print("\nDone.")


# ── Entry Point ────────────────────────────────────────
if __name__ == "__main__":
    run_detection()