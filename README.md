# Slow_Wave_Sleep_Enhancement_System_Lab_Notebook

# Week 2 (1/26/2026 - 2/1/2026):
- Formation week during which the ideas were solidified
- Attended lectures and heard the project proposals
- Met up with the group for the first time, and interest was shown in the slow wave sleep project
- Decided that we will be working on the slow wave sleep project
- As far as early design decisions are concerned, we are planning on having an amplifying circuit with an analog to digital converter which will send the EEG signals to a microcontroller which can be used to analyze them on a computer
- We reviewed the documents sent by Maggie after reaching out to her (she is the sponsor from Carle Health). It seems that an open source YASA software is being used for slow wave sleep detection, we plan on using that
- We are thinking of using STM32 and are planning on working on submitting the early RFA approval soon
- Submitted the early RFA approval

# Week 3 (2/2/2026 - 2/8/2026):
- Our early RFA approval was approved
- Met again to discuss what we can do further to implement the project

# Week 4 (2/9/2026 - 2/15/2026):
- We met up to start work on the proposals and came up with our high level requirements 
- The high level requirement were solidified after meeting with our sponsor
- I set up meetings with Maggie and we asked her all our questions
- Our high level requirements are: play pink noise within 300 ms of detecting slow wave sleep, average comfort rating of the headset should be a ⅘, design should be able to support 10 hours of consecutive sleep 
- We had our first meeting with our TA Hossein. It was a fruitful discussion and he thinks that this project should be fairly complicated and we should work consistently to get it done

<img width="610" height="154" alt="image" src="https://github.com/user-attachments/assets/b8bbffb9-2d3b-4987-9b82-e00b2bf296fa" />

- We are starting work on our Proposal
- We have begun choosing PCB components
-W e are leaning towards using ADS1298 chip as our ADC because it is cheaper than cADS1299 chip ($45.80 vs $73.295)
- We are also planning on using STM32WB5MMG for Microcontroller because of its built-in 2.4 GHz radio for BLE communication
- I have experience using and programming STM Microcontrollers and it has low power consumption for longer bettery life

<img width="614" height="454" alt="image" src="https://github.com/user-attachments/assets/92c3c146-17d7-47da-9c56-02b9a8631c5a" />

<img width="532" height="553" alt="image" src="https://github.com/user-attachments/assets/ff08328f-fe3d-49fa-824c-8a733a0bc0d9" />

# Week 5 (2/16/2026 - 2/22/2026):
- We have the PCB review at the end of this week. We want to get the schematic done and get the PCB reviewed so that we are on track
- There are some changes to be made to the original proposal. We are planning on switching to the ADS1299 chip instead of ADS1298 chip. 
- We realized that using the ADS1298 chip required additional components to make protection circuits for transferring EEG readings to the Analog to Digital Converter (ADC). Our PCB would therefore become too complicated and crowded and the EEG signals could also potentially get saturated
- We were struggling to create a correct protection circuit due to lack of EEG related information on the ADS1298 datasheet
- We also realized that the ADS1299 chip's datasheet has a section that goes more in depth about EEG applications

<img width="525" height="373" alt="image" src="https://github.com/user-attachments/assets/018b41d3-6dd6-4523-b03a-b859e92d3ccc" />
*ADS1299 schematic from datasheet*

<img width="532" height="553" alt="image" src="https://github.com/user-attachments/assets/9f7090de-fe23-4f63-ad51-58b79910eda9" />
*Tried designing protection circuit for ADS1298 which would have been too complicated for our future board in terms of size and soldering*

- Met with Hossein and talked about the design choices we made
- I made the decision that we could potentially ask our sponsors for an additional chip if required if we exceed our 445 budget of $150 
- The ADS1299 chip is $80, almost double of the ADS1298, but we are going ahead with it because for bio applications I think that we need to use the correct components or we may not see the signal as EEG is very low voltage in micro volts. 
- We started with the power subsystem design 
- We need to make sure that we can support 10 hours of battery life 
- We are going to use the Cyton Biosnensing board as an inspiration for our board. Link: https://docs.openbci.com/Cyton/CytonSpecs/
- Needed to use multiple voltage regulators to keep each component's voltage needs met (ADS1299 requires a ±2.5V supply, STM32WB5MMG requires a 3.3 V supply)
- We finalized Components for power subsystem: battery in the 3-6V range, 3.3V regulator, 2.5V regulator, inverter, -2.5V regulator
- We also finalized the Team Contract and signed it this week

<img width="664" height="461" alt="image" src="https://github.com/user-attachments/assets/8f7c1422-7002-4540-9344-b1ec4e8ed48c" />
*Finalized schematic*

# Week 6 (2/23/2026 - 3/1/2026):
- This week we have the design document due. We also received an email from Jonathon Ashbrook, who is an ECE alumni of UIUC. We plan to meet him and ask for his expert opinion on our PCB design and overall project. 
- We met up with Jonathon Ashbrook. It was a very  fruitful meeting. We also took some notes during the meeting. Our main concerns were about if we chose the correct components and if we were doing the filtering correctly. Also asked about placement of the components. 
- He told us to show the amplification of one channel of EEG data for the breadboard demo
- He also suggested to use a STM dev board from the lab and wired USB for data transfer
- He said to keep the capacitors as close to ADS chip and ensure the power subsystem is placed away from RF filtering
- Met with Hossein and showed design documentation and discussed the meeting with Jonathon Ashbrook
- After this meeting I decided that it is very important for us to have various debug options. This would be useful for future
- I suggested later that we need to have an LED that shows the board is on. We also need to have debugging pins that will allow us to measure the voltages of the components. Additionally, we should be able to program the STM32 through these pins. I made these suggestions based on my previous experience in working with PCB. Hardware debugging is very difficult and it is important to have options to see what is going on with the board to identify the problems. 

<img width="710" height="473" alt="image" src="https://github.com/user-attachments/assets/83aadd1d-5e02-4a33-84ef-0e6b6f451546" />
*Finalized block diagram*

# Week 7 (3/2/2026 - 3/8/2026):
- Unfortunately, we weren't able to make the first round of PCB orders. 
- My main contribution was in the schematic overall design. I made sure that every single connection was correct by consulting the documentation. Because it is very hard to debug PCB, I decided that it is okay if we miss the first pCB order as long as we are able to create a very accurate PCB in the second order that would save us a lot of time in the future in debugging. 
- We are actively working on meeting the second PCB round order. 
- There seem to be multiple DRC issues that we ran into. I am satisfied with the schematic. I have gone through multiple consultations with the documentation. I think that our board is electrically correct. However, in the PCB there seems to be many DRC issues and also our PCB looks a bit messy with all the connections. I hope that we can meet the deadline. 
- Met with Hossein and showed progress with PCB design
- I implemented my suggestions earlier about debugging pins which we forgot to include. So I had to make some changes to the schematic: used connector pins to expose the SWDIO, SWCLK, Vcc, GND, UART_Tx, and UART_Rx for programming and data, changed protection circuit for the STM to be more similar to the datasheet

<img width="393" height="605" alt="image" src="https://github.com/user-attachments/assets/72d9cd1e-6200-45ec-8a2c-3c06bf78aba3" />
*ADS1299 part of schematic*

<img width="398" height="523" alt="image" src="https://github.com/user-attachments/assets/f2c93912-96be-43a1-be33-a52004804735" />
*STM32 part of schematic*

- We submitted the PCB second order because we wanted a PCB, but I am very sure that this will not work. This is due to the multiple DRC errors we ran into and the grounding is not good
- The front and back grounding layers (B.Cu and F.Cu) were not connected in certain areas
- Various copper islands arose from this
- Many pad spacing errors on the ADS1299 chip

<img width="665" height="403" alt="image" src="https://github.com/user-attachments/assets/3debd39f-d639-4aff-8900-1b2186b4a3c4" />
*Multiple grounding errors*

# Week 8 (3/9/2026 - 3/15/2026):
- This week is the breadboard demo 
- We do not have any kind of precise chips that can amplify the low voltage EEG signals and convert them accurately into digital
- So I decided that we should have some kind of amplifier circuit with the existing amplifiers available in the ECE supply centre. The ADS1299 break out board is very expensive and impractical to use just for the breadboard demo
- I found some amplifiers from the ECE supply shop. I also rented a STM32 Nucleo breakout board from the ECE 445 lab. 
- My plan is to amplify an input signal (thinking of a sine wave) and then amplifying it by 10,000 times and then it will be within the range of  0 to 3.3V for the STM32 to receive and transmit to the computer. We should be able to plot the sine wave which will prove that our concept of amplification works. 
- However, I am worried that the amplification and multiple chips will cause the signal to saturate. This is something that is actually good because that will prove that for this kind of low voltage amplification circuit, we absolutely need to use the ADS1299 and that proves that our design is correct, thereby also meeting the demands of the breadboard demo. 
- Met with Hossein and shared idea of what we are doing with the breadboard demo
- I designed the original amplifier circuit and helped write the python script that plots the sine wave. We were successful when the input was about 100 micro volts but when we tried a lower voltage, like 10 microvolts the signal was saturated thus proving that we need more sophisticated amplifying via the ADS1299 which will only be possible to test when we get a working PCB, and not on the breadboard since the parts are too expensive and impractical to acquire when we are designing a PCB.

<img width="522" height="614" alt="image" src="https://github.com/user-attachments/assets/5b602d6b-47a7-4be5-af94-f34bcec92771" />
*Breadboard demo circuit*

<img width="540" height="429" alt="image" src="https://github.com/user-attachments/assets/96d07af6-e6c0-49fa-9f0a-c662bf600bde" />
*Plotting of a low frequency sine wave of 2 mV peak to peak*

# Week 9 (3/16/2026 - 3/22/2026):
- Spring break

# Week 9 (3/23/2026 - 3/29/2026):
- Due to the breadboard demo we did not have much time to resolve our PCB issues. 
- We missed the third round order, but we are determined to make the 4th round order this week.
- The first thing that we need to revolve are the PCB grounding issues 
- We set up a meeting with TA Xiadong. 
- Xiadong pointed out that we had pad spacing errors and recommended to increase the pad spacing and look at the documentation to find the recommended pad spacing for each component
- Met with Hossein and talked about our PCB issues and our steps taken to solve it
- We did the same and increased the pad spacing. This did resolve some of our issues. However, we were still having issues with grounding. We will try to solve them this week. One technique that we are trying is adding multiple vias to connect the grounding
- We made a submission for the 4th round PCB order, but we weren't able to solve the grounding issues.

<img width="540" height="514" alt="image" src="https://github.com/user-attachments/assets/a3fc1b29-0f4e-4aed-9e2a-a509973e2da1" />
*Pad spacing recommendation from documentation*

<img width="527" height="514" alt="image" src="https://github.com/user-attachments/assets/e3fb73c2-25ae-47b7-ae0b-844dc01d7efb" />
*DRC errors*

# Week 10 (3/30/2026 - 4/5/2026):
- Since we weren’t able to make a working PCB for the 4th round (we are quite certain it won’t work because of grounding issues), I have reached out to our sponsors and asked if they would be willing to sponsor a PCB order
- They have agreed to sponsor the PCB. This is good news. Now we will just have to solve the grounding issues. 
- We consulted with Xiadong again, and we were able to solve all of our issues. The main problems that we had at the end were only 2 errors. There was no proper grounding connection for the STM chip and that was resolved by moving the wire traces and adding vias. We also adjusted the pad spacing to match the documentation and were able to resolve all of our PCB issues
- Met with Hossein and showed our progress with the PCB errors
- And talked about what we were doing for the progress demo
- We made the order for the PCB and set it for expedited delivery because we have the progress demo next week and we want to be able to show our final PCB. 
- I have decided to start looking at how we can program the STM once we get the PCB.

<img width="662" height="370" alt="image" src="https://github.com/user-attachments/assets/be674f3b-5166-4582-ad42-77b0d5000f91" />
*Finalized PCB without any DRC errors*

# Week 11 (4/6/2026 - 4/12/2026):
- The PCB has gotten stuck in shipment. We have not received the order yet. This is a little worrying since our progress demo is this week. 
- I have decided to shift the focus of our software. We haven’t had too many opportunities till now to work on it because of the PCB and hardware design issues. 
- Essentially, the first step would be to look at the publicly available EDF dataset and try to run a real time algorithm that runs through the data 
- I designed an algorithm that can run the data in real time and look at the classifications that were placed manually. This would help us in seeing if we are seeing the right sleep stages.
- I later realized that the manual classifications are something that was just added and we obviously won’t have access to that when we get real time data. So instead, I am thinking of designing a peak counting algorithms
- We have decided to use an algorithm that is reading EEG data in real time and counting the number of peaks if the wave goes below a certain threshold
- This threshold will mean that we are in the correct amplitude of the slow wave peaks 
- Kavin is simultaneously trying to implement YASA slow wave detector to let my algorithm know when we are in slow wave sleep 
- I am designing an algorithm to count the number of peaks after the EEG goes below a certain threshold and after I know that I am in slow wave sleep. Then if the number of peaks is more than 5 then we are surely in slow wave sleep. I will play the pink noise at this point of time. 
- I figured that it is not possible to know exactly when we are in pink wave sleep as soon as it starts. So we will need to have some kind of rolling buffer
- So in my updated algorithm, I am going to have a rolling buffer of 30 seconds which is updated every second. I am going to look to see if we are in a slow wave based on these 30 seconds. Then start counting peaks if we cross a threshold and play pink noise after 5 peaks are detected.
- We were moderately successful in designing this algorithm and this is what we plan to show in the progress demo since we do not have our PCB yet. It still seems to be stuck in transit 
- Originally we hoped that it would arrive before the progress demo and we could try soldering on the STM32 and the ADS1299 chips to show hardware progress, however it did not arrive. 
- Some of the code has been uploaded on the GitHub branch. We used AI to assist us with coding
- We finished the algorithm and decided to demo using the Cyton board as an input to the algorithm. We showed pink noise being played at certain timestamps which roughly corresponded to the slow wave sleep on the EDF field. 
- After the demo, we decided to start soldering the PCB 

<img width="669" height="359" alt="image" src="https://github.com/user-attachments/assets/c493ee99-c397-46af-8015-5a5705aaa16d" />
*EDF file we were working with*

<img width="659" height="424" alt="image" src="https://github.com/user-attachments/assets/4a3b7ede-c2d2-4b5e-8b53-0ecdd356e963" />
*Plotting EEG using OpenBCI software*

# Week 12 (4/13/2026 - 4/19/2026):
- Our PCB arrived unfortunately the day before the progress demo. So we didn't get the chance to work on it much. Additionally, it did not come with the stencil for soldering so we did not want to solder the board and waste our chips in case we made a mistake since they are very expensive and we only have 2 of each
- We finally got our stencil and we are going to use this to solder the ADS1299 and STM32 chips. We just realized that the pad spacing is extremely small and we cannot see the pads below the STM32 chip. We hope that this won’t cause any problems down the line.

<img width="660" height="487" alt="image" src="https://github.com/user-attachments/assets/a60b90d9-7c88-4678-87ea-28b61bc2c5db" />
*Final received PCB*

- We started soldering the components and applied solder paste through the stencil
- We finally finished soldering and we are going to try and program the STM32
- We were able to successfully program the STM32 via the header pins

<img width="658" height="528" alt="image" src="https://github.com/user-attachments/assets/619da3c1-c4f2-42a3-ac0e-dcb820fba853" />
*Set up used for holding the board in place for soldering*

<img width="660" height="545" alt="image" src="https://github.com/user-attachments/assets/c0041b1a-568c-48fa-a05a-c8614a77ac59" />
*Able to program STM of our custom PCB*

<img width="636" height="444" alt="image" src="https://github.com/user-attachments/assets/21c24618-1015-4a7a-b938-42481fdb7ed8" />
*Final soldered PCB*

- Our next step was to start and visualize imputed signals from the PCB. We tried sending in sine waves and used a python script to visualize the plotting in real time. The first step was to ensure that there was proper SPI communication between the STM32 and the ADS1299 chip
- I mainly worked on the STM32 code and I soldered most of the hand-soldered parts
- I first tested if I am able to read the device ID of the ADS1299
- I then checked if I could write to the registers on the ADS1299 and read from them 
- This was successful so I moved on to seeing if I could plot sine waves from one channel.
- This was successful as well.

<img width="661" height="564" alt="image" src="https://github.com/user-attachments/assets/f7d95a57-b990-4eb1-b482-3c0e9a49d56e" />
*Plotting low amplitude low frequency sine wave after inputting through  voltage divider circuit so that the voltage is in microvolts*

<img width="639" height="563" alt="image" src="https://github.com/user-attachments/assets/fffe4564-8c80-4f49-b203-42b0e57a4bc7" />
*Plotting sine wave*

# Week 13 (4/20/2026 - 4/26/2026):
- This week I focused my efforts on trying to plot EEG. This proved to be unsuccessful in the first attempt. I realized that it was because there was a lot of noise on the headset since it is a dry electrode and that cause a lot of DC offset which was offsetting the EEG signal

<img width="677" height="579" alt="image" src="https://github.com/user-attachments/assets/a38a3b3d-9ac8-4659-94dc-d8e4ddceb9e7" />
*EEG signal being offset*

- So I tried adjusting the gain settings and applied a software filter to remove further noise. This helped a bit and I was able to see something that looked like EEG but still had a lot of noise

<img width="662" height="565" alt="image" src="https://github.com/user-attachments/assets/c5bdd451-5270-42ca-afba-7e31e9cba2e0" />
*Noisy EEG signal*

- So I adjusted the gain settings even more and kept playing around with it. I then also realized that we were not connecting the bias electrode correctly. It was supposed to originate from the forehead and not earlibe like the reference electrode. Once I fixed that and reduced the gain, the results looked much better

<img width="673" height="546" alt="image" src="https://github.com/user-attachments/assets/36760471-1b00-4ab9-9c95-8b16f5e6ad81" />
*Clean EEG plotting 1*

<img width="674" height="583" alt="image" src="https://github.com/user-attachments/assets/c2794ea7-70ba-4fac-a6f9-febe86cb4463" />
*Clean EEG plotting 2*

<img width="669" height="579" alt="image" src="https://github.com/user-attachments/assets/dd574e65-0c64-4f99-82ae-f75c95443530" />
*Clean EEG plotting 3*

- The best way to see if the EEG is responsive is a blinking test. There should be spikes when a person blinks. I verified that this works as well.

<img width="682" height="586" alt="image" src="https://github.com/user-attachments/assets/42d12e4f-48dc-4d17-bd5e-d1247550b78c" />
*Blinking test*

- We have now run into an issue where the STM32 is not programming. I suspect that it is because we tried uploading a different software for bluetooth that could have messed up the configurations. 
- Removed and resoldered the STM32.
- Able to program again.
- Moving to 8 channels
- Ran into issue with plotting 8 channels. 
- Now STM32 doesn't program again
- Tried resoldering again
- Been resoldering for a couple of days now. The pins are so small that even slight movement in the board is causing the signal to get completely distorted
- Also I have realized that the bluetooth antenna is placed in the wrong place. We will not be able to achieve bluetooth communication because of traces underneath the antenna. 
- The only option is to resolder onto a new board or order a new board, but we do not have time and we still have the software component to work on which is not fully functional yet and that is an important part of the project as well. 
- Able to program it but the signal is distorted and with the final demo coming soon, I think it is best to move on from the board and use the Cyton board instead and work on improving the software
- I suggested an improvement to the pink noise playing algoethm. Tried using Hilber Filter but realized that it would not be useful for our application. Instead, I am going to set an adaptive threshold. The threshold will be updated every 2 seconds based on previous 5 seconds of data. This way we won’t have to count peaks like before because that is not accurate because the EEG data is constantly changing. Additionally, I am going to play pink noise at a set time after threshold crossing since the threshold is nearest to the peak and the time after which the pink noise is played after a set time will correspond to the upstate when the neurons are active making it mor eeffectve. 
- Successfully able to implement the software.

<img width="664" height="374" alt="image" src="https://github.com/user-attachments/assets/2d64dddb-0291-482f-a5f3-deb774055d71" />
*Plotting EEG data on software*

- I am going to add timestamps as to where we played the pink noise to verify against the publicly available EEG file. This works well as well after some iterations in the threshold and changes in code. Final product looks good to go for final demo

<img width="668" height="390" alt="image" src="https://github.com/user-attachments/assets/ba987078-6a2f-4179-afa3-beeff235f702" />
*Correct identification and playing of pink noise*


# Week 14 (4/27/2026 - 5/3/2026):
- Final demo

# Week 15 (5/4/2026 - 5/7/2026):
- Finished final presentation and submitted final report and lab checkout
- Said our goodbyes to our TA Hossein who has been very supportive and helpful throughout the course of the semester


































































