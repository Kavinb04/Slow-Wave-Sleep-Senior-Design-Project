# detection/sws_detector.py
import numpy as np
import yasa
import mne

SW_FREQ_BAND = (0.5, 2.0)
SW_DUR_NEG   = (0.3, 1.5)
SW_DUR_POS   = (0.1, 1.0)
SW_AMP_NEG   = (40, 200)
SW_AMP_POS   = (10, 150)
SW_AMP_P2P   = (50, 500)

class SWSDetector:
    def __init__(self, sample_rate: int = 250):
        self.fs         = sample_rate
        self.last_stage = 'Unknown'

    def get_sleep_stage(self, eeg_5min: np.ndarray) -> str:
        try:
            info = mne.create_info(
                ch_names=['EEG'],
                sfreq=self.fs,
                ch_types=['eeg']
            )
            raw = mne.io.RawArray(
                eeg_5min[np.newaxis, :] / 1e6,
                info,
                verbose=False
            )

            sls   = yasa.SleepStaging(raw, eeg_name='EEG')
            hypno = sls.predict()

            print(f"  [Staging] Raw predictions: {list(hypno)}")

            # Count how many epochs in the last 5 min were predicted N3
            n3_count  = list(hypno).count('N3')
            total     = len(hypno)
            n3_ratio  = n3_count / total if total > 0 else 0

            print(f"  [Staging] N3 epochs: {n3_count}/{total} ({n3_ratio:.0%})")

            # If more than 30% of epochs are N3 → call it N3
            if n3_ratio >= 0.4:
                return 'N3'
            else:
                return 'Other'

        except Exception as e:
            print(f"  [Staging] Error: {e}")
            return self.last_stage

    def detect(self, eeg_30s: np.ndarray, eeg_5min: np.ndarray, run_staging: bool) -> dict:
        min_samples = int(5 * self.fs)
        if len(eeg_30s) < min_samples:
            return {'slow_waves': None, 'is_sws': False, 'sw_count': 0, 'stage': 'Unknown'}

        # Step 1 — update sleep stage every 30s once 5min buffer is full
        if run_staging:
            self.last_stage = self.get_sleep_stage(eeg_5min)

        stage = self.last_stage

        # Step 2 — only run sw_detect if likely N3
        if stage != 'N3':
            return {
                'slow_waves' : None,
                'is_sws'     : False,
                'sw_count'   : 0,
                'stage'      : stage,
            }

        # Step 3 — run slow wave detection
        try:
            sw = yasa.sw_detect(
                eeg_30s,
                sf=self.fs,
                freq_sw=SW_FREQ_BAND,
                dur_neg=SW_DUR_NEG,
                dur_pos=SW_DUR_POS,
                amp_neg=SW_AMP_NEG,
                amp_pos=SW_AMP_POS,
                amp_ptp=SW_AMP_P2P,
            )

            if sw is None:
                return {'slow_waves': None, 'is_sws': False, 'sw_count': 0, 'stage': stage}

            summary  = sw.summary()
            sw_count = len(summary)
            is_sws   = sw_count >= 2

            return {
                'slow_waves' : summary,
                'is_sws'     : is_sws,
                'sw_count'   : sw_count,
                'stage'      : stage,
            }

        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'slow_waves': None, 'is_sws': False, 'sw_count': 0, 'stage': stage}