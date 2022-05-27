"""
BotCommands provides another layer of abstraction between GameInputter and a Tekken Bot, allowing button presses to be
grouped together into larger building blocks like 'backdash' or 'do a combo' or 'block low'. In addition to button
presses, BotCommands accomadtes low level concepts in addition to buttons, like 'hit confirm' (check to see if this
combo isn't hitting) or 'pause until my next move comes out'.

A botcommand 'command' consists of a list of tuples, each one with a command and the amount of time to wait in frames before
performing it. UniversalCommands contains a few general sequences. They are also simple enough to be constructed on the fly
or read from a file.
"""
import time
import random

from click import command
from ButtonCommandEnum import Command
from TekkenGameState import TekkenGameState
from MoveInfoEnums import InputAttackCodes, InputDirectionCodes
import BasicCommands
import GameInputter


class UniversalCommands:
    BACKDASH = list(zip(
        [Command.TapBack,Command.TapBack],
        [0,1]
    ))

    FORWARDDASH_HALF = list(zip(
        [Command.TapForward, Command.TapForward, Command.TapBack],
        [0, 2, 5]
    ))

    SIDESTEP_RIGHT = list(zip(
        [Command.TapRight, Command.TapBack],
        [0, 4]
    ))

    SIDESTEP_LEFT = list(zip(
        [Command.TapLeft, Command.TapBack],
        [0, 4]
    ))

    SIDESTEP_UP = list(zip(
        [Command.TapUp, Command.TapBack],
        [0, 16]
    ))

    BLOCK_LONG = list(zip(
        [Command.HoldBack, Command.ReleaseBack, Command.Wait],
        [0, 10, 1]
    ))

    BLOCK_MID_FULL = list(zip(
        [Command.HoldBack, Command.ReleaseBack, Command.Wait],
        [0, 10, 1]
    ))

    BLOCK_LOW_FULL = list(zip(
        [Command.HoldDownBack, Command.ReleaseDownBack, Command.Wait],
        [0, 10, 1]
    ))

    LOW_PARRY = list(zip(
        [Command.HoldForward, Command.HoldDown, Command.ReleaseForward, Command.ReleaseDown],
        [0, 0, 120, 0]
    ))

    THROW_TECH_1 = list(zip(
        [Command.Tap1, Command.Tap1, Command.Tap1, Command.Tap1, Command.Tap1, Command.Tap1],
        [4, 4, 4, 4, 4, 4]
    ))

    THROW_TECH_12 = list(zip(
        [Command.Tap1, Command.Tap2, Command.Tap1, Command.Tap2, Command.Tap1, Command.Tap2, Command.Tap1, Command.Tap2, Command.Tap1, Command.Tap2, Command.Tap1, Command.Tap2],
        [4, 0, 4, 0, 4, 0, 4, 0, 4, 0, 4, 0]
    ))

    THROW_TECH_2 = list(zip(
        [Command.Tap2, Command.Tap2, Command.Tap2, Command.Tap2, Command.Tap2, Command.Tap2],
        [4, 4, 4, 4, 4, 4]
    ))

    MASH_CONTINUE = list(zip(
        [Command.Accept, Command.Accept],
        [4, 4]
    ))

    Combo_1 = list(zip(
        [Command.Accept, Command.Accept],
        [4, 4]
    ))

class BotCommands:
    def __init__(self, inputController, is_playback_mode = False):
        self.updateFrame = 0
        self.is_playback_mode = is_playback_mode
        self.isBusy = False
        self.inputController = inputController
        self.commandBuffer = {}
        self.commandIndex = 0
        self.inputDelay = 0
        self.inputDelayCode = None

    def Update(self, gameState: TekkenGameState,wait =15):
        #self.UpdateInputDelay(gameState)
        print(self.commandBuffer)
        

        self.UpdateCommandBuffer(gameState,wait)
        self.ClearCommands()
    """""
    def UpdateCommandBuffer(self, gameState: TekkenGameState):
        if not self.IsAvailable():
            if self.updateFrame == self.commandBuffer[self.commandIndex][1]:
                command = self.commandBuffer[self.commandIndex][0]
                self.commandIndex += 1
                self.ProcessCommand(command, gameState)
                self.updateFrame = 0
                self.UpdateCommandBuffer(gameState)
            else:
                self.updateFrame += 1
        self.ClearCommands()
        print(self.updateFrame)

    """""
    def UpdateCommandBuffer(self, gameState: TekkenGameState,wait):
        
        for val in self.commandBuffer.values():
            #print(val)
            i=1
            for command in val:
                
                #print(command[0] )
                
                #print(i)
                i+=1
                time.sleep(command[1]/60)
                self.ProcessCommand(command[0], gameState)
                
                self.updateFrame = 0
                    
            
            time.sleep(wait/60)
            self.inputController.Release()
        
        #print(self.updateFrame)
        
     
    def addNewCommand(self,command):
        
        command_string = []
        buffer = []

        for command in command.split(','):
            if len(command.split('+')) !=1:
                command_string = self.move_value(command,command_string)
            else: 
                command_string = self.basic_value(command,command_string)
        
        if  len(command.split('+')) == 1:
            for i in range(len(command_string)):
                buffer.append(5)
        else:
            for i in range(len(command_string)):
                
                if i < 2:
                    buffer.append(0)
                else:
                    
                    buffer.append(2)
        
        final_command = list(zip(
           command_string ,
           buffer
       
        ))
        self.AddCommand(final_command)
         
    def move_value(self,command,command_string):
        command = command.split('+')

        if command[0] == 'f':
            command_string.append(Command.TapForward)
            command_string.append(Command.TapForward)
            

        if command[0] == 'b':
            command_string.append(Command.TapBack)
            command_string.append(Command.TapBack)
            
        if command[0] == 'd/f':
                command_string.append(Command.TapForward)
                command_string.append(Command.TapDown)
                

        if command[0] == 'd/b':
            command_string.append(Command.TapDown)
            command_string.append(Command.TapBack)
            
            
        
        command_string = self.basic_value(command[1],command_string)
        
        return command_string
        
    def basic_value(self, command,command_string):
        if command == '1':
            command_string.append(Command.Tap1)
            #command_string.append(Command.Release1)
        if command == '2':
            command_string.append(Command.Hold2)
            #command_string.append(Command.Release2)
        if command == '3':
            command_string.append(Command.Tap3)
        if command == '4':
            command_string.append(Command.Tap4)
        return command_string
        

    def IsAvailable(self):
        return self.commandIndex >= len(self.commandBuffer)

    def GetUp(self):
        self.AddCommand([(Command.TapBack, 1)])

    def MashTech(self):
        if random.randint(0, 1) == 0:
            self.AddCommand(UniversalCommands.THROW_TECH_1)
        else:
            self.AddCommand(UniversalCommands.THROW_TECH_2)

    def Backdash(self):
        self.AddCommand(UniversalCommands.BACKDASH)

    def ForwarddashSmall(self):
        self.AddCommand(UniversalCommands.FORWARDDASH_HALF)

    def SidestepRight(self):
        self.AddCommand(UniversalCommands.SIDESTEP_RIGHT)

    def SidestepLeft(self):
        self.AddCommand(UniversalCommands.SIDESTEP_LEFT)

    def SidestepUp(self):
        self.AddCommand(UniversalCommands.SIDESTEP_UP)

    def BlockAndWait(self):
        self.AddCommand(UniversalCommands.BLOCK_LONG)

    def ThrowTech(self):
        self.AddCommand(UniversalCommands.THROW_TECH_1)

    def BlockMidFull(self):
       
        self.AddCommand(UniversalCommands.BLOCK_MID_FULL)
        

    def BlockLowFull(self):
      
        self.AddCommand(UniversalCommands.BLOCK_LOW_FULL)
        

    def LowParry(self, startup):
   
        self.AddCommand(UniversalCommands.LOW_PARRY)
      

    def WalkForward(self, startup):
      
        self.AddCommand([(Command.HoldForward, startup)])

    def MashContinue(self):
        self.AddCommand(UniversalCommands.MASH_CONTINUE)

    def ResetPractice(self):
        self.ClearCommands()
        self.AddCommand([(Command.ReleaseAll, 0), (Command.Wait, 2), (Command.ResetPractice, 0), (Command.Wait, 1)])
    """"
    def AddCommand(self, buffer):
        if self.IsAvailable():
            self.commandBuffer = list(buffer)
            self.updateFrame = 0
            self.commandIndex = 0
            """
    def AddCommand(self, buffer):
      
        #print(type(self.commandBuffer) ) 
        self.commandBuffer["Command " + str(len(self.commandBuffer)+1 )  ] =   list(buffer)
        #self.commandBuffer = list(buffer)
        #print(self.commandBuffer)
        #self.updateFrame = 0
        #self.commandIndex = 0 

    
    
    
    def ProcessCommand(self, command, gameState:TekkenGameState):
        #self.CheckForInputDelay(command)

        if command == Command.TapForward:
            self.inputController.TapForward()
        if command == Command.TapBack:
            self.inputController.TapBack()
        if command == Command.TapUp:
            self.inputController.TapUp()
        if command == Command.TapDown:
            self.inputController.TapDown()
        if command == Command.TapRight:
            self.inputController.TapRight()
        if command == Command.TapLeft:
            self.inputController.TapLeft()
        if command == Command.Tap1:
            self.inputController.Tap1()
        if command == Command.Tap2:
            self.inputController.Tap2()
        if command == Command.Tap3:
            self.inputController.Tap3()
        if command == Command.Tap4:
            self.inputController.Tap4()

        if command == Command.Accept:
            self.inputController.TapAccept()
        if command == Command.ResetPractice:
            self.inputController.TapAccept()
            self.inputController.TapSelect()

        if command == Command.HoldBack:
            self.inputController.HoldBack()
        if command == Command.ReleaseBack:
            self.inputController.TapBack()
        if command == Command.HoldForward:
            self.inputController.HoldForward()
        if command == Command.ReleaseForward:
            self.inputController.ReleaseForward()
        if command == Command.HoldDown:
            self.inputController.HoldDown()
        if command == Command.ReleaseDown:
            self.inputController.ReleaseDown()
        if command == Command.HoldUp:
            self.inputController.HoldUp()
        if command == Command.ReleaseUp:
            self.inputController.ReleaseUp()

        if command == Command.Hold1:
            self.inputController.Hold1()
        if command == Command.Hold2:
            self.inputController.Hold2()
        if command == Command.Hold3:
            self.inputController.Hold3()
        if command == Command.Hold4:
            self.inputController.Hold4()

        if command == Command.Release1:
            self.inputController.Release1()
        if command == Command.Release2:
            self.inputController.Release2()
        if command == Command.Release3:
            self.inputController.Release3()
        if command == Command.Release4:
            self.inputController.Release4()

        if command == Command.HoldRage:
            self.inputController.HoldRage()
        if command == Command.ReleaseRage:
            self.inputController.ReleaseRage()

        if command == Command.HoldDownBack:
            self.inputController.HoldBack()
            self.inputController.HoldDown()
        if command == Command.ReleaseDownBack:
            self.inputController.ReleaseBack()
            self.inputController.ReleaseDown()

        if command == Command.ReleaseAll:
            self.inputController.Release()


        if command == Command.PunishConfirm:
            if gameState.DidBotRecentlyDoMove():
                pass
            else:
                self.commandIndex = 0

        if command == Command.HitConfirm:
            if gameState.DidBotRecentlyDoDamage:
                pass
            else:
                self.ClearCommands()

        if command == Command.Nextmove:
            if gameState.IsBotMoveChanged() or gameState.IsBotAttackStarting():
                #print(gameState.GetBotJustMoveID())
                #print(gameState.stateLog[-1].bot.move_id)
                pass
            else:
                self.commandIndex -= 1
                self.commandBuffer[self.commandIndex] = (Command.Nextmove, 1)

        if command == Command.Startupmove:
            self.commandIndex -= 1
            #print(gameState.GetBotTimeUntilImpact())
            self.commandBuffer[self.commandIndex] = (Command.Wait, gameState.GetBotTimeUntilImpact() * -1)


        if command == Command.Recovery:
            self.commandIndex -= 1
            inputDelay = 0
            self.commandBuffer[self.commandIndex] = (Command.Wait, max(0, gameState.GetBotFramesUntilRecoveryEnds() - 6 - inputDelay))

        if command == Command.FullRecovery:

            if gameState.GetBotRecovery() - gameState.GetBotMoveTimer() < 6:
                pass
            else:
                self.commandIndex -= 1
                self.commandBuffer[self.commandIndex] = (Command.FullRecovery, 1)

    def CheckForInputDelay(self, command):
        if self.inputDelayCode == None:
            self.inputDelay = 0
            if command == Command.Tap1:
                self.inputDelayCode = [InputAttackCodes.x1, InputAttackCodes.x1x2, InputAttackCodes.x1x3, InputAttackCodes.x1x4, InputAttackCodes.x1x2x3, InputAttackCodes.x1x2x4, InputAttackCodes.x1x3x4]
            else:
                self.inputDelayCode = None

    def UpdateInputDelay(self, gameState: TekkenGameState):
        if self.inputDelayCode != None:
            #if any((True for x in self.inputDelayCode if x in botInputState)):
            if gameState.DidBotIdChangeXMovesAgo(1):
                print(self.inputDelay)
                self.inputDelayCode = None
                self.inputDelay = 0
            else:
                self.inputDelay += 1
                if self.inputDelay > 40:
                    self.inputDelayCode = None
                    self.inputDelay = 0

    def ClearCommands(self):
        self.commandBuffer = {}
        #self.inputController.Release()
        self.updateFrame = 0
 

 