# sws_detector.py
import numpy as np
import yasa

# YASA slow-wave detection parameters (AASM-compliant defaults)
SW_FREQ_BAND = (0.5, 2.0)   # Hz — slow-wave frequency range
SW_DUR_NEG   = (0.3, 1.5)   # seconds — negative half-wave duration
SW_DUR_POS   = (0.1, 1.0)   # seconds — positive half-wave duration
SW_AMP_NEG   = 40            # µV — minimum negative peak amplitude
SW_AMP_POS   = 10            # µV — minimum positive peak amplitude
SW_AMP_P2P   = 75            # µV — minimum peak-to-peak amplitude

class SWSDetector:
    """
    Runs YASA slow-wave detection on a window of EEG data.
    Call detect() periodically (e.g., every 5 seconds) with
    the latest rolling buffer from EEGReceiver.
    """
    def __init__(self, sample_rate: int = 250):
        self.fs = sample_rate

    def detect(self, eeg_data: np.ndarray) -> dict:
        """
        Args:
            eeg_data: 1D numpy array of EEG in µV, at least 5 seconds long.
        Returns:
            dict with keys:
              - 'slow_waves': DataFrame of detected events (or None)
              - 'is_sws': bool, True if slow waves are actively occurring
              - 'sw_count': int
        """
        min_samples = int(5 * self.fs)
        if len(eeg_data) < min_samples:
            return {'slow_waves': None, 'is_sws': False, 'sw_count': 0}

        try:
            sw = yasa.sw_detect(
                eeg_data,
                sf=self.fs,
                freq_sw=SW_FREQ_BAND,
                dur_neg=SW_DUR_NEG,
                dur_pos=SW_DUR_POS,
                amp_neg=SW_AMP_NEG,
                amp_pos=SW_AMP_POS,
                amp_ptp=SW_AMP_P2P,
            )

            if sw is None:
                return {'slow_waves': None, 'is_sws': False, 'sw_count': 0}

            summary = sw.summary()

            # "Active SWS" heuristic: ≥2 slow waves detected in the last 30s window
            sw_count = len(summary)
            is_sws = sw_count >= 2

            return {
                'slow_waves': summary,
                'is_sws': is_sws,
                'sw_count': sw_count,
            }

        except Exception as e:
            print(f"[SWSDetector] Detection error: {e}")
            return {'slow_waves': None, 'is_sws': False, 'sw_count': 0}

    def get_bandpower(self, eeg_data: np.ndarray) -> dict:
        """
        Returns delta (0.5–4 Hz) bandpower as a quick SWS proxy.
        Useful for staging before running full sw_detect.
        """
        bp = yasa.bandpower(eeg_data, sf=self.fs, bands=[(0.5, 4, 'Delta')])
        return {'delta_power': float(bp['Delta'].values[0])}