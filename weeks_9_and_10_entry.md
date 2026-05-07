# ECE 445 Notebook Entry (4/6/2026 to 4/17/2026) 

While waiting on our PCB, we decided to shift our focus to the slow wave detection component of our Computer Subsystem. Understanding the accuracy of slow wave detection required us to first analyze publicly available EEG data

## What we learned when working with YASA:
- YASA Python library detects slow waves using ".sw_detect" function
- .sw_detect requires at least 30 seconds of sleep data (not adjusted for live EEG data)
- Used sliding window approach to analyze 30 seconds of sleep data
- Learned that EEG data is accompanied by an associated hypnogram (timestamps for what stages of sleep the associated data is classified as

## Testing with Cyton Board
- Testing slow wave detection on live feed from Cyton Board because we are waiting on PCB
- Live feed was very noisy and did not look like EEG waves
- Most likely a plotting issue (debugging it).


<img width="1920" height="1021" alt="image" src="https://github.com/user-attachments/assets/7b5c1976-8b4c-4e83-b52e-1d883348a1a3" />
EDF File with hypnogram timestamps


