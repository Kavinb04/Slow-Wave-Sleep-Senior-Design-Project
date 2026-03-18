# ECE 445 Notebook Entry 2 (2/16/2026 to 2/20/2026)

Our main objective this week was to make enough progress in our PCB design to go to the PCB review session. This included completing our schematic, assigning proper footprints to each component, and arranging components on the board.

## Changes since Week 1 Proposal

### Switching from ADS1298 to ADS1299 chip
- Realized that using the ADS1298 chip required additional components to make protection circuits for transferring EEG readings to the Analog to Digital Converter (ADC)
- Do not have enough space to fit all the components and wire them properly if using ADS1298
- 

![old_protection_circuit](images/old_protection_circuit.PNG) <br>
*Attempt at designing extra protection for sending EEG signals to ADS1298 chip* <br> <br>

### Built the Power Subsystem
- Used the Cyton Biosensing board as inspiration on how to power our PCB board components
- Had to take into consideration 

[Link to Cyton Board Schematic](https://docs.openbci.com/Cyton/CytonSpecs/)
