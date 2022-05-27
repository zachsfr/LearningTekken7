# Learning Tekken 7

This repository hosts the code I used to build a reinforcement learning agent for the game Tekken 7. A massive thank you to this community project https://github.com/WAZAAAAA0/TekkenBot. I built everything on top of their code. They laid the baseline for extracting and reading game values from Tekken. The pieces that I designed myself are gymTekken, event_handeler, and model_building. The gymTekken code is a representation of the environment of Tekken. All actions are sent to that class, which it will then act on and send a corresponding observation of what occurred. The event_handelr is a supporting class of methods that handles all actions that need to be taken care of. Since not all the memory address values are working currently, it also collects and stores data on what is occurring in the game as well. The model_building class is where model testing can occur. Currently, random actions are  sent to the learning agent to test and verify the other parts of the code. Due to having to make many workarounds, not everything is  working fully, but it is almost all the way ready to add a reinforcement learning model.   
