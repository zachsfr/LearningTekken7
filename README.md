Check out these experimental forks for new TekkenBotPrime features (and sometimes faster updates):\
https://github.com/dcep93/TekkenBot \
https://github.com/Alchemy-Meister/TekkenBot \
https://github.com/compsyguy/TekkenBot

# TekkenBot
AI and tools for playing and understanding Tekken 7.

Created by roguelike2d. Maintained by the community.

# Frequently asked questions
**Q:** What is this thing?\
**A:** It's a program for Tekken 7 that shows frame data information of your moves in real-time on PC.

**Q:** How do I use it?\
**A:** Go to the releases page, download the latest `TekkenBotPrime_vXXX.zip`, extract the files somewhere, open `TekkenBotPrime.exe`, and finally hop into practice mode.\
If you'd rather run from source instead, install Python 3 and run `GUI_TekkenBotPrime.py`

**Q:** The bot stopped working after a game patch!\
**A:** Wait for a good soul to update the `memory_address.ini` file, or fix it yourself by following the guide on the Wiki.

**Q:** The frame advantage of this move seems wrong!\
**A:** Double check using the alternative "manual" method to find frame advantage with the help of `tiny_live_frame_data_numbers`:
1. start a mirror match (because not all characters have the same jumps)
2. set the dummy to neutral jump as second action
3. do your attack, neutral jump, and don't do anything else\
...the little numbers near the big frame advantage ones should now hopefully display the correct advantage.

**Q:** I'm getting the `PID not found` error even though the game is running!\
**A:** Start the bot as admin (or alternatively start the game as non-admin).

**Q:** The bot doesn't show!\
**A:** Play borderless or windowed, full screen doesn't work.

**Q:** But I really really want to play full screen otherwise my game will lag!\
**A:** If you have a multi-monitor setup, enable `overlay_as_draggable_window` and move the overlay to a different monitor.
## Tools
### FrameDataOverlay
A window that can go over the game to display real time move information read from memory. Requires the game to be in windowed or borderless to work or can be run as a standalone window on a second screen.
![Robot feet and bear paws 1](Screenshots/frame_data.png?raw=true)
### CommandInputOverlay
Display command inputs, similar to the one already in Tekken 7 except it gives frame by frame information and includes cancelable frames.
![Robot feet and bear paws 2](Screenshots/command_input.png?raw=true)
## Bots
Currently in progress.
### Details
Tekken Bot bots are programs that plays Tekken 7 on PC by reading the game's memory, making decisions based on the game state, and then inputting keyboarding commands. Ultimately the goal is to create emergent behavior either through specific coding it or, if possible, a generalized learning algorithm.
### Frame Trap Bot
Pushes jab or a user inputted move when getting out of block stun.
### Punisher Bot
Attempts to punish negative attacks with the best available punish. Punishes are listed in the character's file in the /TekkenData folder.
## Project details
### Prerequisites
Tekken Bot is developed on Python 3.5 and tries to use only core libraries to improve portability, download size, and, someday, optimization. It targets the 64-bit version of Tekken 7 available through Steam on Windows 7/8/10.
### Deployment
Tekken Bot distributable is built using pyinstaller with Python 3.5. On Windows, use the included build_project.bat file.
