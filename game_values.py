"""
Collects information from TekkenGameState over time in hopes of synthesizing it and presenting it in a more useful way.

"""

from MoveInfoEnums import AttackType
from MoveInfoEnums import ThrowTechs
from MoveInfoEnums import ComplexMoveStates
from TekkenGameState import TekkenGameState

class TekkenEncyclopedia:
    def __init__(self, print_extended_frame_data = False):
        self.FrameDataP1 = {}
        self.FrameDataP2 = {}
        self.p1 = 1
        self.p2 =1
        self.GameEvents = []
        self.current_game_event = None
    
        self.print_extended_frame_data = print_extended_frame_data

        self.active_frame_wait = 1
        self.active_frame_wait2 = 1
        self.was_fight_being_reacquired = True

        
        self.current_frame_data_entry = True
        self.previous_frame_data_entry = None


    
    def GetPlayerString(self, Player):
        if (Player) :
            return "p1 | "
        else:
            return "p2 | "


    
    """"
    #Set the dummy to jump and hold up and this prints the frame difference.
    def CheckJumpFrameDataFallback(self, gameState):
        if not self.isPlayerOne:
            if gameState.IsFulfillJumpFallbackConditions():
                print("p1 jump frame diff: " + str(gameState.GetBotMoveTimer() - gameState.GetOppMoveTimer()))
        """
    def Update(self, gameState: TekkenGameState,Player_info):
        #if(gameState.IsOppAttacking()):
            #print("Getting attacked!")
            
        
       
        x1 = self.DetermineFrameData(gameState,False,Player_info[0])
       
        
        gameState.FlipMirror()
        

       
        x2=  self.DetermineFrameData(gameState,True,Player_info[1])
       

        #, x2 , x3 = None, None,None
       


        gameState.FlipMirror()
        
        return x1,x2
       
       


    def DetermineFrameData(self, gameState,Player,Player_info):
        
        val = None
        #if(gameState.IsBotAttackStarting()):
           # print("WHy")
       # if(gameState.IsOppAttacking()):
            #print('LOL')
            
        currentState = None
        frameDataEntry = None
        if (gameState.IsBotBlocking() or gameState.IsBotGettingHit() or gameState.IsBotBeingThrown() or gameState.IsBotBeingKnockedDown() or gameState.IsBotBeingWallSplatted()): #or gameState.IsBotUsingOppMovelist()): #or  gameState.IsBotStartedBeingJuggled() or gameState.IsBotJustGrounded()):
            
            
            
            #print(gameState.stateLog[-1].bot.move_id)
            #print(gameState.stateLog[-1].bot.move_timer)
            #print(gameState.stateLog[-1].bot.recovery)
            #print(gameState.DidBotIdChangeXMovesAgo(self.active_frame_wait))
            #print(self.FrameData)
            
           
            if gameState.DidBotIdChangeXMovesAgo(self.active_frame_wait) or gameState.DidBotTimerInterruptXMovesAgo(
                    self.active_frame_wait)-1:  # or gameState.DidOppIdChangeXMovesAgo(self.active_frame_wait):
               
                is_recovering_before_long_active_frame_move_completes = (gameState.GetBotRecovery() - gameState.GetBotMoveTimer() == 0)
                gameState.BackToTheFuture(self.active_frame_wait)
              
                #print(gameState.GetOppActiveFrames())
                if (not self.active_frame_wait >= gameState.GetOppActiveFrames() ) and not is_recovering_before_long_active_frame_move_completes:
                    self.active_frame_wait += 1
                   
                    
                else:
                    
                  
                    gameState.ReturnToPresent()

                    currentActiveFrame = gameState.GetLastActiveFrameHitWasOn(self.active_frame_wait)

                    gameState.BackToTheFuture(self.active_frame_wait)


                  
                   
                    if Player:

                        frameDataEntry = FrameDataEntry(self.print_extended_frame_data)
                        self.FrameDataP1[self.p1] = frameDataEntry
                        
                        self.p1 += 1    #print(self.FrameData)
                        
                    else:
                       
                        frameDataEntry = FrameDataEntry(self.print_extended_frame_data)
                        self.FrameDataP2[self.p2] = frameDataEntry
                        #print(self.FrameData)
                        self.p2 +=1
                    
                    
                    frameDataEntry.currentActiveFrame = currentActiveFrame

                    frameDataEntry.currentFrameAdvantage = '??'
                     
                    frameDataEntry.move_id = gameState.GetOppMoveId()
                    # frameDataEntry.damage =
                    frameDataEntry.damage = gameState.GetOppDamage()
                    frameDataEntry.startup = gameState.GetOppStartup()

                    if frameDataEntry.damage == 0 and frameDataEntry.startup == 0:
                        frameDataEntry.startup, frameDataEntry.damage = gameState.GetOppLatestNonZeroStartupAndDamage()

                    frameDataEntry.activeFrames = gameState.GetOppActiveFrames()
                    frameDataEntry.hitType = AttackType(gameState.GetOppAttackType()).name
                    if gameState.IsOppAttackThrow():
                        frameDataEntry.hitType += "_THROW"

                    frameDataEntry.recovery = gameState.GetOppRecovery()

                    #frameDataEntry.input = frameDataEntry.InputTupleToInputString(gameState.GetOppLastMoveInput())

                    frameDataEntry.input = gameState.GetCurrentOppMoveString()

                    frameDataEntry.technical_state_reports = gameState.GetOppTechnicalStates(frameDataEntry.startup - 1)

                    frameDataEntry.tracking = gameState.GetOppTrackingType(frameDataEntry.startup)

                    #print(gameState.GetRangeOfMove())

                    gameState.ReturnToPresent()

                    #frameDataEntry.throwTech = gameState.GetBotThrowTech(frameDataEntry.activeFrames + frameDataEntry.startup)
                    frameDataEntry.throwTech = gameState.GetBotThrowTech(1)

                    time_till_recovery_opp = gameState.GetOppFramesTillNextMove()
                    time_till_recovery_bot = gameState.GetBotFramesTillNextMove()

                    new_frame_advantage_calc = time_till_recovery_bot - time_till_recovery_opp

                    frameDataEntry.currentFrameAdvantage = frameDataEntry.WithPlusIfNeeded(new_frame_advantage_calc)

                    if gameState.IsBotBlocking():
                        frameDataEntry.onBlock = new_frame_advantage_calc
                    else:
                        if gameState.IsBotGettingCounterHit():
                            frameDataEntry.onCounterHit = new_frame_advantage_calc
                        else:
                            frameDataEntry.onNormalHit = new_frame_advantage_calc

                    frameDataEntry.hitRecovery = time_till_recovery_opp
                    frameDataEntry.blockRecovery = time_till_recovery_bot
                    frameDataEntry.move_str = gameState.GetCurrentOppMoveName()
                    frameDataEntry.prefix = self.GetPlayerString(Player)

                    #print(str(frameDataEntry).split('|'))
                    #print("Frame Entry " + str(frameDataEntry))
                    #print(self.FrameDataP1)
                    val = str(frameDataEntry)
                    Player_info["Health"] = max( 0, Player_info["Health"] -gameState.GetBotHealth())
                    
                    self.current_frame_data_entry = frameDataEntry
                    print(Player_info["Health"])
                    
                    gameState.BackToTheFuture(self.active_frame_wait)

                    self.active_frame_wait = 1
                gameState.ReturnToPresent()
        if Player:
            return str(frameDataEntry).split('|')          
        return str(frameDataEntry).split('|')

        """
        if not  Player:
            if gameState.IsBotWhiffingAlt() and not gameState.IsOppBlocking() and not gameState.IsOppGettingHit():
                #print("reached base level plu 1")
                if gameState.DidBotIdChangeXMovesAgo(self.active_frame_wait2) or  gameState.DidBotTimerInterruptXMovesAgo(
                    self.active_frame_wait2):  # or gameState.DidOppIdChangeXMovesAgo(self.active_frame_wait):
                    print("reached base level")
                    is_recovering_before_long_active_frame_move_completes = (gameState.GetBotRecovery() - gameState.GetBotMoveTimer() == 0)
                    gameState.BackToTheFuture(self.active_frame_wait2)

                
                    if (not self.active_frame_wait >= gameState.GetBotRecovery() + 1) and not is_recovering_before_long_active_frame_move_completes:
                        self.active_frame_wait2 += 1
                        print("dssd")
                    else:
                        print("reached deep")
                        gameState.ReturnToPresent()


                        currentActiveFrame = gameState.GetLastActiveFrameHitWasOn(self.active_frame_wait)
                        

                        gameState.BackToTheFuture(self.active_frame_wait2)
                        currentState = []
                        time_till_recovery_opp = gameState.GetOppFramesTillNextMove()
                        time_till_recovery_bot = gameState.GetBotFramesTillNextMove()

                        new_frame_advantage_calc = time_till_recovery_bot - time_till_recovery_opp
                        currentState.extend([
                            

                        
                        gameState.GetOppActiveFrames(),
                        gameState.GetOppActiveFrames(),
                        gameState.IsOppAttacking(),
                        gameState.IsBotAttackStarting(),
                        gameState.GetOppFramesTillNextMove(),
                        gameState.GetBotFramesTillNextMove()
                        ])
                    
                        self.active_frame_wait2 = 1
                    gameState.ReturnToPresent()
            """
       
               


class FrameDataEntry:
    def __init__(self, print_extended = False):
        self.print_extended = print_extended
        self.prefix = '??'
        self.move_id = '??'
        self.move_str = '??'
        self.startup = '??'
        self.calculated_startup = -1
        self.hitType = '??'
        self.onBlock = '??'
        self.onCounterHit = '??'
        self.onNormalHit = '??'
        self.recovery = '??'
        self.damage = '??'
        self.blockFrames = '??'
        self.activeFrames = '??'
        self.currentFrameAdvantage = '??'
        self.currentActiveFrame = '??'
        self.health = '??'
        self.input = '??'
        self.technical_state_reports = []
        self.blockRecovery = '??'
        self.hitRecovery = '??'
        self.throwTech = None
        self.tracking = ComplexMoveStates.F_MINUS


    def WithPlusIfNeeded(self, value):
        try:
            if value >= 0:
                return '+' + str(value)
            else:
                return str(value)
        except:
            return str(value)

    def InputTupleToInputString(self, inputTuple):
        s = ""
        for input in inputTuple:
            s += (input[0].name + input[1].name.replace('x', '+')).replace('N', '')
        if input[2]:
            s += "+R"
        return s

    def __repr__(self):

        notes = ''

        if self.throwTech != None and self.throwTech != ThrowTechs.NONE:
            notes += self.throwTech.name + " "

        self.calculated_startup = self.startup
        for report in self.technical_state_reports:
            #if not self.print_extended:
            if 'TC' in report.name and report.is_present():
                notes += str(report)
            elif 'TJ' in report.name and report.is_present():
                notes += str(report)
            elif 'PC' in report.name and report.is_present():
                notes += str(report)
            elif 'SKIP' in report.name and report.is_present():
                #print(report)
                self.calculated_startup -= report.total_present()
            elif 'FROZ' in report.name and report.is_present():
                #print(report)
                self.calculated_startup -= report.total_present()
            elif self.print_extended:
                if report.is_present():
                    notes += str(report)
        nerd_string = ""
        if self.print_extended:
            pass
            #notes += ' stun {}'.format(self.blockRecovery)
            #notes += ' a_recovery {}'.format(self.hitRecovery)
            #notes += "Total:" + str(self.recovery) + "f "

        if self.calculated_startup != self.startup:
            self.calculated_startup = str(self.calculated_startup) + "?"

        non_nerd_string = "{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}".format(
            str(self.input),
            str(self.move_id),
            self.move_str,
            str(self.hitType)[:7],
            str(self.calculated_startup),
        self.WithPlusIfNeeded(self.onBlock),
            self.WithPlusIfNeeded(self.onNormalHit),
            self.WithPlusIfNeeded(self.onCounterHit),
            (str(self.currentActiveFrame) + "/" + str(self.activeFrames)),
            self.tracking.name.replace('_MINUS', '-').replace("_PLUS", '+').replace(ComplexMoveStates.UNKN.name, '?'),
            self.recovery,
            self.hitRecovery,
            self.blockRecovery,
            self.health
        )
    

        notes_string = "{}".format(notes)
        now_string = "|{}".format(str(self.currentFrameAdvantage))
        return self.prefix + non_nerd_string + notes_string + now_string




