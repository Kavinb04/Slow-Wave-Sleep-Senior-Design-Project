# ECE 445 Notebook Entry (4/20/2026 to 4/27/2026)

## Plotting EEG Waves
- Plotted using UART connection
- Signals were noisy and impossible to use for identifying slow waves
- Adjusted Gain settings and estimated dc_offset to reduce noise
- Programmed Gain = 4; DC_Offset changes constantly when new data is read
- Calibration time of 500 samples of data
- Tested for responsiveness of signal by blinking eyes while wearing headset (Causes spikes in data)
- Correct amplitude was verified using a formula to convert RAW ADC values to $\mu V$

<img width="650" height="566" alt="image" src="https://github.com/user-attachments/assets/e574b18e-2890-4110-8233-6ab3ef756935" />
Screenshot of EEG reading

<img width="408" height="329" alt="image" src="https://github.com/user-attachments/assets/be0c82ba-0865-49e1-a309-8fa75244610c" />
Blink Test

## STM32 Replacement
- STM32 programming capability stopped working
- Tried many avenues for debugging (Using different computers, previous versions of code, checking power subsystem, 
- Finally had to solder a new STM32
- Started working (STM was most likely bricked after we messed with firmware updates for Bluetooth Functionality)
- firmware updates were needed for bluetooth. (accidentally messed with memory that should not be accessed)

<img width="1170" height="235" alt="image" src="https://github.com/user-attachments/assets/b9fa9477-b5aa-427e-bb9b-423627f2ccdc" />
<img width="1548" height="784" alt="image" src="https://github.com/user-attachments/assets/feba7871-6173-4f71-9f73-a9ad8e695f62" />
STM Programming Error Messages

## Bluetooth Capability Issues
- Tried implementing bluetooth client and server code for STM and computer
- Was not working at all
- Xiadong and another TA told us that the STM was placed in the incorrect location of our PCB
- We should not have any Copper Grounding or wires under the Antenna (Right side of the chip)

<img width="433" height="313" alt="image" src="https://github.com/user-attachments/assets/f34180d3-1cf5-4041-8407-d19026e3a289" />



## Messed up signal 
- When trying to incorporate 8 channels into our process, our EEG output was suddenly experiencing lots of noise
- Could not figure out the source of this noise

<img width="1177" height="732" alt="IMG_0327" src="https://github.com/user-attachments/assets/b4e16b74-3bf1-4ef4-83f3-5b2791acbf02" />
How plotting looks like now


## Overall Outcome
Our board was not salvagable for end to end testing with our software component. We documented Video and picture evidence of 

## Software Design
- Used software component from previous weeks as a skeleton
- I worked on the UI and slow wave detection of software
- Aidan and Vikram worked on the function to find the upstate of the detected slow wave and playing pink noise

### Deciding when to run the detector
- If the user was known to be awake or in light sleep, we did not run the slow wave detector
- Pink noise should be played when the user is confirmed to be experiencing Slow Wave Sleep
- Used YASA sleep staging to estimate what sleep stage the EEG data might belong to
- Also needed a minimum of 2.5 minutes of data to predict the specific sleep stage (Used a sliding window for estimating sleep stage)

### Plot # 1: Cyton Board
- Our goal was to show live readings from the cyton board in our detector
- After 2 minutes of calibration, the program correctly identified that the user was not experiencing Slow wave sleep, so noise was not played
<img width="1083" height="566" alt="image" src="https://github.com/user-attachments/assets/6c8e7f59-ff70-4675-9e29-c28796dbda6b" />

### Plot #2: Available EEG data
- Ran the detector on a KNOWN timestamp when the user is in slow wave sleep
- Correctly identified slow waves and played pink noise
<img width="1274" height="717" alt="image" src="https://github.com/user-attachments/assets/0547d75e-6e6f-4331-93fd-1219c9e21b8f" />



