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
- Our high level requirements are: play pink noise within 300 ms of detecting slow wave sleep, average comfort rating of the headset should be a ⅘, design should be able to support 10 hours of consecutive sleep, 
- We had our first meeting with our TA Hossein. It was a fruitful discussion and he thinks that this project should be fairly complicated and we should work consistently to get it done

<img width="610" height="154" alt="image" src="https://github.com/user-attachments/assets/b8bbffb9-2d3b-4987-9b82-e00b2bf296fa" />

- We are starting work on our Proposal
- We have begun choosing PCB components
-W e are leaning towards using ADS1298 chip as our ADC because it is cheaper than cADS1299 chip ($45.80 vs $73.295)
- We are also planning on using STM32WB5MMG for Microcontroller because of its built-in 2.4 GHz radio for BLE communication
- I have experience using and programming STM Microcontrollers and it has low power consumption for longer bettery life
