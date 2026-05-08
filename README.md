# Slow_Wave_Sleep_Enhancement_System_Lab_Notebook_Aidan_Stahl

# Aidan Stahl's Notebook

# Week 2 (1/26/2026 - 1/30/2026):

* Discussed design ideas for early project approval.
* Reviewed project proposals presented in class.
* Reached out to Maggie Li regarding the sleep tracking project presented during lecture.
* Reviewed overall project details sent by Maggie.
* Met with Maggie via zoom to discuss project details further and get clarification on project requirements.
* Discussed implementation methods for early project approval. We are planning on using EEG leads that connect to a MCU to amplify and digitize EEG   waves and transmit them to a computer for processing to detect slow-wave sleep. We are planning on using YASA, an open-source algorithm for SWS detection.
* We want to play pink noise after detecting SWS with little delay, correctly classify SWS, and ensure the device is comfortable.
* Submitted RFA for early approval.

# Week 3 (2/2/2026 - 2/6/2026):

* Project approved
* Discussed implementation details further

# Week 4 (2/9/2026 - 2/13/2026):

* Worked on project proposal.
* Brainstormed ideas for how to implement the project. Weighed the differences with  using an inexpensive ADC and our own amplifiers vs using ADS1298 ADC with built in amplification.
* Basic sketch and full block diagram for our design:
<img width="1186" height="486" alt="image" src="https://github.com/user-attachments/assets/7ed11e3d-b61c-4228-8603-fd7fc9000532" />

* Considered using ADS131E08IPAGR and ADS1299, but settled on ADS1298 because sampling rate for the 131 was unsatisfactory for EEG applications and 1298 is less expensive than 1299, while still appropriate for our project.
* Additionally, I researched how the ADS function. I found that the 24-bit value is outputted from the ADC and must be converted in our software back to volts. In order to do this, an equation is used:
<img width="806" height="122" alt="image" src="https://github.com/user-attachments/assets/7ed1c6c0-111a-4d30-91eb-4d3836335da7" />

* Incomplete circuit schematic:
<img width="632" height="642" alt="image" src="https://github.com/user-attachments/assets/66450bea-2244-416f-8a11-5f6634c969ca" />

# Week 5 (2/16/2026 - 2/20/2026):

* Continued work on schematic.
* Began PCB design.
* Used Cyton board schematic as a reference.
* Researched components to use for power and considered components for microcontroller and ADC.  We found a 2.5V regulator and -2.5V regulator to use as a reference for the ADC,  a 3.3V regulator to power the microcontroller and ADC, and an inverter that we are planning on using for the - 2.5 V inverter. All components were found on Digikey. We are considering using the ADS1299IPAGR ADC instead of the ADS1298 because ADS1299 is specifically designed for EEG applications and will be able to measure signals more accurately, with lower noise, and higher amplification. The chip is around $80, so we’re hoping that we’ll have enough funds, but are considering asking our sponsor for additional funding if necessary. Additionally, we decided to use the STM32WB5MMGH6TR microcontroller because of its high processing speed and low power consumption for long battery life. Also, Vikram has familiarity with this MCU from ECE 395.
* Additionally, we looked at different battery options, including rechargeable batteries and 6 volt batteries to support at least 10 hours of battery life as part of our high level requirements.
* Scheduled a meeting with Jonathan Ashbrook to get his thoughts on our design plans and more clarification on the design process.
* We had our first meeting with our TA, Hossein. We showed him our current incomplete design and discussed our plans for the project and future design.

# Week 6 (2/23/2026 - 2/27/2026):

* We completed our first circuit schematic and further developed our PCB layout.
* We met with Jonathan Ashbrook and inquired about frequency filtering and input protection and showed him our circuit schematic and incomplete PCB layout so he could review. He said reverse input protection for the user should be of minimal concern since the product is powered by a battery with low voltage and current output that wouldn’t be harmful to the user. He suggested frequency filtering in the range of Bluetooth’s 2.4 GHz carrier frequency because, due to the STMs built-in Bluetooth that we are planning on using, that is likely our largest source of interference. He also said everything else looks good.
* We looked into the best component values for the most optimal frequency filtering and settled on 1000 Ohm resistors and 2.2 nF capacitors as low-pass filters for all 8 EEG input nodes.
* We used this equation to find the most optimal component values based on a desired cutoff frequency:
<img width="736" height="118" alt="image" src="https://github.com/user-attachments/assets/bc7a04c8-da53-40b1-bd18-5adbda6107d4" />

* Additionally, I calculated the transfer function to find suppression with our current component values at the frequency of Bluetooth:
<img width="1164" height="212" alt="image" src="https://github.com/user-attachments/assets/b03b7f65-7ab7-44c6-9adb-612806c59b28" />

* We wrote requirements and verifications for our design review. We want to make sure that our ADC and microcontroller receive the correct power, that SPI communication functions properly, that our plots are retained when using a waveform generator to verify, and that Bluetooth communication works correctly. We also want to make sure that slow-wave sleep is detected properly and pink noise plays after detection.
* We are going to set the ADC sampling frequency to 250 Hz to ensure no aliasing.
* We met with Hossein and updated him on our current progress with component choices and design choices. Also, we updated him regarding the meeting with Jonathan Ashbrook.
* Visual aid placed in our design review that shows an overview of our project:
<img width="1048" height="270" alt="image" src="https://github.com/user-attachments/assets/f9a3bf2f-3411-4437-88dc-db01bd3ae8c1" />

* More detailed block diagram showing high-level product design:
<img width="680" height="462" alt="image" src="https://github.com/user-attachments/assets/534e8679-34e9-4b86-9e16-f793aa2294b7" />

* Mostly complete circuit design (not finalized):
<img width="686" height="480" alt="image" src="https://github.com/user-attachments/assets/e25a6a4c-db92-4ceb-b52b-4efc889659a4" />

* Completed and submitted the design review document.
* Met with Hossein and discussed our potential ideas for the breadboard demo and updated him on current progress.

# Week 7 (3/2/2026 - 3/6/2026):

* We mostly finalized our product’s components
* We also attempted to finish the PCB layout in time for first round PCB orders, but we were not able to make first round PCB orders.
* I made the connections between the ADS1299 ADC and STM microcontroller and completed some additional wiring for power and other components around the board.
* Here is our current PCB layout with DRC errors that still need to be corrected:
<img width="1168" height="458" alt="image" src="https://github.com/user-attachments/assets/91ad5181-6bfa-4cbd-b34f-f47101484ed6" />

* We submitted second round PCB orders anyways, just to see the physical board, but we will definitely need to order a revised PCB in the next order window.

# Week 8 (3/9/2026 - 3/13/2026):

* Worked on breadboard demo. For our breadboard demo, since none of our components work on breadboards, and their equivalent dev board components are too expensive, we decided to emulate the amplification our ADC will do to see how well a low voltage signal in the 100 microvolt range will be maintained.
* We were hoping to fine tune the component values for our low-pass filters as well through this breadboard demo.
* For the breadboard demo, I designed a circuit with amplification stages, similar to what the ADC would be doing. The first amplifier was an instrumentation amplifier for high accuracy with a gain of 100. The next two stages were op-maps both with a gain of 10, so total amplification after all three stages would have a gain of 10,000, which is around the same gain our ADC will have to amplify the EEG signals.
* Breadboard demo circuit design:
<img width="1216" height="388" alt="image" src="https://github.com/user-attachments/assets/b6b97532-25ae-4a45-b695-987834c6911a" />

* Since the waveform generator was not capable of outputting a value in the 100 microvolt range, I also used a voltage divider to divide the voltage by 1000. We were able to successfully see a sine wave from a 100 microvolt peak to peak output amplified by our three stage amplification breadboard on an oscilloscope with the correct amplitude.
* Sine waves in the 1-10 microvolt peak to peak voltage amplitude range were not maintained, likely due to high noise levels. This shouldn’t be a problem with our ADC because the amplifiers have much higher accuracy and noise reduction.
* I also checked between stages to verify that voltage at each stage was correct.
* Additionally, we used the STM Nucleo development board to develop a plotting platform that uses the in-built ADC. We sent the sine wave through our voltage divider, amplified this signal, and then checked what was being measured from the dev board. We were able to clearly see a sine wave, showing that after 10,000 gain, the wave will be maintained.
* Signal seen from STM dev board after being passed through our amplification breadboard:
<img width="590" height="494" alt="image" src="https://github.com/user-attachments/assets/224d4bb9-dd6e-47f6-9270-24f5eb48143e" />

# Week 9 (3/23/2026 - 3/27/2026):

* Worked on revising our PCB layout and fixing DRC errors. We asked Hossein for his advice and he advised us to reach out to Xiaodong.
* Xiaodong advised us on fixing the remaining DRC errors. He explained to us that the issues are likely from pad spacing on the provided footprints for the ADS and STM chips.
* I was able to fix some of the DRC errors by reducing the solder mask expansion value to fix overlapping pads or pads that were too close together.
* We were unable to resolve all issues. There were still some problems with grounding. We still put in an order for the fourth round of PCB orders.
* We decided that we are going to need to order a PCB on our own because the current PCB is still not correct.

# Week 10 (3/30/2026 - 4/3/2026):

* I was able to solve grounding issues by redrawing the ground plane and adding more ground vias where the ground plane was still missing.
* I was able to fix some of the spacing DRC issues that Xiaodong informed us about by decreasing the solder mask expansion and increasing pad spacing.
* We met with our Nafisa from our sponsored group who informed us that we can order a new PCB with a stencil and another ADS1299 chip and they would reimburse us.
* Photo of our final PCB layout:
<img width="696" height="492" alt="image" src="https://github.com/user-attachments/assets/2c370ec0-5ba5-44a4-8974-734e883c71cc" />

* Worked on the individual progress report.
* Met with Hossein and updated him on the progress we have made and our PCB order. Additionally, we discussed potential options for the progress demo next week.
* We began working on the slow-wave sleep detection software in preparation for the progress demo.
* We found classified EEG data online in the form of EDF files. We found an EDF viewer that allowed us to view the data and classifications simultaneously. We used this data to verify if our SWS detector was working correctly by checking if the classification times for slow-wave sleep matched what our software was saying.
* The current software version we developed is somewhat accurate, but still has flaws and must be refined.
* We also worked on a peak detection algorithm that would play pink noise at specific times along the upstate of slow-waves once slow-wave sleep is detected. This software is still not functioning correctly.
* Worked on live plotting with the Cyton board and will implement this with our actual board once it arrives.
* We used AI to assist us with the implementation of this software/code.

# Week 11 (4/6/2026 - 4/10/2026):

* We had our progress demo.
* We are still waiting for our PCB order so we were not able to show anything for that. We were able to show some of the software that we have for slow-wave sleep detection and slow wave peak detection and the live plotting with the Cyton board.
* Worked on revising our slow-wave detection software and peak detection software.
* EDF plots from online with classifications that we used to verify SWS detection software accuracy:
<img width="1034" height="672" alt="image" src="https://github.com/user-attachments/assets/a2f93603-e286-414c-b55b-485d2a997b5e" />

* Our PCB arrived and we began organizing our components and soldering our PCB.
* We used solder paste, a stencil, and the PCB oven to solder the ADS1299 and STM32 chips. The STM32 has especially small pins, so we had to be very careful to prevent shorts.
* Blank PCB board and fully soldered PCB board:
<img width="1242" height="472" alt="image" src="https://github.com/user-attachments/assets/c31fcc27-562a-4781-82e8-b2beb2b53dc8" />

* Connected power to the board and saw the LED light up.
* I measured power at different points across the PCB with a multimeter and found that one of the pins was receiving a much lower voltage than it should’ve been. Upon further assessment, I realized that one of the pins for our inverter was not grounded properly, so I added more solder on the pin and this fixed the voltage issue.

# Week 12 (4/13/2026 - 4/17/2026):

* We programmed the STM32 and set up SPI communication.
* We encountered a connection problem with the STM that we were able to resolve after having Xiaodong take a look. We were missing a diode but solved this by shorting the two pads on the PCB with a small piece of wire. Now the STM connects without issue using the STM programer.
* We programmed the STM and set up SPI communication between the STM and ADC.
* We successfully plotted a sine wave generated by the waveform generator connected to our PCB. The PCB takes the waveform generated wave as an input and after filtering, the voltage is measured by the ADS which then communicates with the STM via SPI and the STM sends over our data to the computer using UART communication. We don’t have Bluetooth implemented at this point, so we are using UART as a supplement.
* Successfully plotted sine wave using a waveform generator and our PCB:
<img width="1094" height="414" alt="image" src="https://github.com/user-attachments/assets/d34d1f64-3d5a-4f08-8d0f-5138c70b6ce9" />

* Updated Hossein on project progress.
* Additionally, we were able to measure EEG waves with our PCB using the OpenBCI headset.

# Week 13 (4/20/2026 - 4/24/2026):
* Attempted Bluetooth implementation.
* We realized that there was supposed to be a dedicated keep out zone for the antenna of the STM32, and that we had added traces under the antenna. * * Unfortunately, as a result, the Bluetooth was unlikely to function.
* We attempted setup several times to no avail.
* After attempting Bluetooth setup one final time, there was an issue that seemed to have bricked the STM. We replaced the STM and got it functioning again and took a video and photos of our PCB measuring EEG waves.
* Photo of headset measuring EEG waves using our PCB:
<img width="998" height="572" alt="image" src="https://github.com/user-attachments/assets/763ae15b-5115-49f9-bd9d-3800bf052edb" />

* The PCB was functioning properly for 2 days but broke again. The plots show a large amount of noise and are minimally reactive to plotting a waveform generated sine wave. We replaced the ADC to see if that was potentially a problem and had the same issue.
* Plots after second PCB issue:
<img width="1032" height="586" alt="image" src="https://github.com/user-attachments/assets/62130aaf-f9e1-47f4-9931-fb3b500f2599" />

* Spent many hours debugging. At this point, it seemed like a hardware issue, and due to the lack of time left in the class, it seemed unlikely that we would be able to get the board fixed in time for the final demo. We likely had to order another STM MCU or another PCB and entirely replace all components.
* Looking back, it would’ve been easier to use an ESP32 because of the ease of soldering and ease of implementation using the arduino IDE.
* With little left to debug, we decided to focus on software in preparation for the final demo.
* Kavin put the finishing touches on the slow-wave sleep detection algorithm, while Vikram and I refined our slow-wave sleep peak detector and pink noise player.
* We implemented an adjustable voltage threshold. Once our EEG wave crosses this threshold, it classifies it as a slow wave and the peak is typically near at this point, so pink noise is played shortly after crossing this threshold. The threshold is based on the last 5 seconds of data by finding the bottom 15th percentile. Once a wave is classified as a slow-wave, a 50 ms timed burst of pink noise is played, which corresponds with the upstate of the slow wave, since our threshold gives an estimate for the negative peak.
* Additionally, we worked on a way to simulate an EDF file as live data so we could jump to a specific time in the EDF file and determine if slow-wave sleep is being classified correctly.
* Example of live data simulator using an EDF file with our software:
<img width="846" height="480" alt="image" src="https://github.com/user-attachments/assets/fb5eaf84-bd1e-4877-8bff-8205dfbc67e8" />

* Example of classifying an EEG wave as a slow wave and subsequently playing pink noise within 300 ms of the beginning of the upstate:
<img width="810" height="444" alt="image" src="https://github.com/user-attachments/assets/79e33ab4-b94c-4adb-adc1-04cf72f52f8c" />
