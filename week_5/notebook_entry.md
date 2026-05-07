# ECE 445 Notebook Entry 5 (3/9/2026 to 3/13/2026)

This week was mainly focused on our Breadboard Demo. Acquiring the dev boards for the ADS1299 Chip and an STM32WB5MMG were too expensive, so we created an alternative circuit on our breadboard. We instead used breadboard friendly amplifiers and an STM Dev board capable of wired communication as replacement parts.

## Breadboard Demo Objective
Our main objective was to show the amplification and digitization of signals in the 10 - 100 $\mu v$ range. Our end goal was to be able to plot these signals in real-time on the computer. 

Amplification of Sine Wave:
- The Signal Generator can generate a sine wave with a minimum peak to peak Voltage of 1 mV (Amplitude of 500 $\mu V$)
- Used Voltage divider to bring voltage down to 50 $\mu V$ (Acceptable EEG output range is 0 to 100 $\mu V$)
- 

STM Microcontroller Dev Board:
- Does not have bluetooth capability so sent data through UART

Python Plotting:
- Using a UART to USB connector
- Python script reads values from COM Port
