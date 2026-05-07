# ECE 445 Notebook Entry (4/20/2026 to 4/27/2026)

## Plotting EEG Waves
- Plotted using UART connection
- Signals were noisy and impossible to use for identifying slow waves
- Adjusted Gain settings and estimated dc_offset to reduce noise
- Programmed Gain = 4; DC_Offset changes constantly when new data is read
- Calibration time of 500 samples of data
- Tested for responsiveness of signal by blinking eyes while wearing headset (Causes spikes in data)

<img width="650" height="566" alt="image" src="https://github.com/user-attachments/assets/e574b18e-2890-4110-8233-6ab3ef756935" />
Screenshot of EEG reading

<img width="408" height="329" alt="image" src="https://github.com/user-attachments/assets/be0c82ba-0865-49e1-a309-8fa75244610c" />
Blink Test


## PCB Issues
- STM32 programming capability stopped working
- Tried many avenues for debugging (Using different computers, previous versions of code, different power
- Finally had to solder a new STM32
- Started working (STM was most likely bricked after we messed with firmware updates)
- firmware updates were needed for bluetooth

## Bluetooth Capability Issues

## Software Design
