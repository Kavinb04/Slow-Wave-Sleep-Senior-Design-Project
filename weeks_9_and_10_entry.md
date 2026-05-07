# ECE 445 Notebook Entry (4/6/2026 to 4/10/2026) 

While waiting on our PCB, we decided to shift our focus to the slow wave detection component of our Computer Subsystem. Understanding the accuracy of slow wave detection required us to first analyze publicly available EEG data

## What we learned when working with YASA:
- YASA Python library detects slow waves using ".sw_detect" function
- .sw_detect requires at least 30 seconds of sleep data (not adjusted for live EEG data)
- Used sliding window approach to analyze 30 seconds of sleep data
- Learned that EEG data is accompanied by an associated hypnogram (timestamps for what stages of sleep the associated data is classified as awake, light sleep, or deep Slow wave sleep)

## Testing with Cyton Board
- Testing slow wave detection on live feed from Cyton Board because we are waiting on PCB
- Live feed was very noisy and did not look like EEG waves
- Most likely a plotting issue (debugging it).


<img width="1920" height="1021" alt="image" src="https://github.com/user-attachments/assets/7b5c1976-8b4c-4e83-b52e-1d883348a1a3" />
EDF File with hypnogram timestamps

# ECE 445 Notebook Entry (4/13/2026 to 4/17/2026) 

Both our Round 4 and expedited shipping PCB orders have arrived. Received additional ADS1299, capacitor, and resistor parts. 

## Stencil and Oven soldering
- Soldered the ADS1299 and STM32 using a combination of our stencil and PCB oven
- The PCB stencil was needed to apply soldering paste to the ADS1299 and STM32 numerous soldermask pads
- Ran into a few issues with having to reapply solder paste (Accidental bridges or missing spots)
- Once components were placed, we used oven to solidify connection between part and PCB

## Hand Soldering
- Remaining parts were hand soldered
- Identified bridges using the continuity test
- Realized footprint for battery protection diode and button to reset STM were smaller than our parts
- Had to create a separate order for these parts
- Board was getting proper power (Used LED to verify)



<img width="5712" height="4284" alt="IMG_0323" src="https://github.com/user-attachments/assets/d1f5b8cf-3219-4b04-bf46-3ebce498b627" />
Round 4 PCB 

<img width="5712" height="4284" alt="IMG_0321" src="https://github.com/user-attachments/assets/4a15bbce-4129-4ce7-b0e9-2f780efddd4f" />
Finalized PCB

(Insert image of stencil board here)
How we applied stencil solder



