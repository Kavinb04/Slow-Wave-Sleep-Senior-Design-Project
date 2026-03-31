# detection/sws_detector.py
import numpy as np
import yasa

SW_FREQ_BAND = (0.5, 2.0)
SW_DUR_NEG   = (0.3, 1.5)
SW_DUR_POS   = (0.1, 1.0)
SW_AMP_NEG   = (100, 200)   
SW_AMP_POS   = (30, 150)    
SW_AMP_P2P   = (175, 500)

class SWSDetector:
    def __init__(self, sample_rate: int = 250):
        self.fs = sample_rate

    def detect(self, eeg_data: np.ndarray) -> dict:
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

            print(f"  sw type: {type(sw)}")
            print(f"  sw value: {sw}")
            # sw is None if nothing detected
            if sw is None:
                return {'slow_waves': None, 'is_sws': False, 'sw_count': 0}

            # sw is a SwesResults object — call .summary() to get the DataFrame
            summary = sw.summary()
            sw_count = len(summary)
            is_sws = sw_count >= 2

            return {
                'slow_waves': summary,
                'is_sws': is_sws,
                'sw_count': sw_count,
            }

        except Exception as e:
            import traceback
            print(f"[SWSDetector] Detection error: {e}")
            traceback.print_exc()  # shows exact line number of the crash
            return {'slow_waves': None, 'is_sws': False, 'sw_count': 0}