from re import L
import time
import threading
import random
from turtle import update
import numpy as np
import pandas as pd
import BasicCommands
import GameInputter
import TekkenGameState
from ArtificialKeyboard import ArtificalKeyboard
from multiprocessing.pool import ThreadPool
from game_values import TekkenEncyclopedia




class ActionHandler:
    
    def __init__(self,side=False):
        self.actions = pd.read_csv("TekkenData/simple_moves.csv")
        self.gameController = GameInputter.GameControllerInputter(side)
        self.botCommands = BasicCommands.BotCommands(self.gameController)
       
        self.frameRateCounter = 0
        self.frameRate = 0
        self.cyclopedia = TekkenEncyclopedia( False)
        self.used = 0
        self.info = {}
        self.pan = 0
        self.info = {'Player Wins':0,
                    'Opponent Wins': 0,
                    "Health Remaining Win":[]
                       
        
        }
        self.set()
        self.reset()
        
    
    def set(self):
        self.player1 = {
        "Health":175,
        "M Won Overall":0,
        "M Won Set":0
        
        }

        self.player2 = {
            "Health":175,
            "M Won Overall":0,
            "M Won Set":0
            
        }
    
    def reset(self):
        

        self.state = {
        'Round Timer': np.array([60],dtype='int32'),

            'Health':  (
                np.array([175],dtype='int32'), 
                np.array([175],dtype='int32'),   

            ),

            'Frames':( 
                np.array([0],dtype='int32'), 
                np.array([0],dtype='int32'),   

            ),  
            'Opponet': 3,
            'State': (
                0,
                0,
            ),        
            'whiff': (
                0,
                0
            ) 
        
        }

        self.timer = time.time()
   
   
    def isFightOver(self):
       
        #print(self.state['Timer'])
        return self.state['Round Timer'] < .2    or self.player1['Health'] == 0 or self.player2['Health'] == 0
    
    def update_actions(self):
        actions = self.actions.iloc[:,0].to_numpy()
        self.used += 1

        return actions
    def membs(self):
        all = self.__dict__.items()
        return all
    
    def finished(self,gameState: TekkenGameState):
        
        val = 0
        if self.player1["Health"] > self.player2["Health"]:
            
            
            self.info['Player Wins'] +=1 
            self.info['Health Remaining Win'].append(self.player1['Health'])
            self.match_update(self.player1)
            print(self.player1)
            val =5
        
        elif self.player2["Health"]> self.player1["Health"]:
            
            
            self.info['Opponent Wins'] +=1 
            self.match_update(self.player2)
            print(self.player2)
            val = -1
        
        return val, self.info
    
    def match_update(self,dict):
            dict["M Won Overall"] += 1
            dict["M Won Set"] += 1
            
            self.player1['Health']= 175
            self.player2['Health']= 175
            if dict["M Won Set"] ==3:
                print(dict)
                self.player1["M Won Set"] = 0
                self.player2["M Won Set"] = 0
    
    
    
    def summary(self,gameState: TekkenGameState):
        

        return  self.p1Win,self.p2Wins
    
    
    def take_action(self,action,gameState: TekkenGameState):
      
        pool = ThreadPool(processes=2)
        action = threading.Thread(target = self.action_handler,args=(action,gameState))
        
        watch =pool.apply_async(self.cyclopedia.Update,(gameState,(self.player2,self.player1)))
        action.start()
       
        
        while action.is_alive():
            
            gameState.Update()
            
            val2 , val4 =  watch.get()
            
            #print(self.player2["Health"],self.player1["Health"] )
            
            if gameState.WasFightReset() or self.isFightOver():
                action.join()
                break

            if(gameState.IsBotGettingHit()) and not gameState.IsBotBlocking() :
               #print("OW!")
               action.join()
               time.sleep(.02)
               break
               
            if(gameState.IsBotWhiffingAlt() and not gameState.IsOppBlocking() and not gameState.IsOppGettingHit()):
                #print("pint wiff!")
                action.join()
                break
            
          
        pool.terminate()
        return self.update_obs(val2,val4,gameState)

    
    
    
    
    def update_obs(self,val1,val2,gameState: TekkenGameState):
        if val1 and val1 != ['None']:
            self.update_obs_helper(val1)
        
        elif val2 and val2 != ['None']:
            self.update_obs_helper(val2)
        else:
             self.state['Frames'] = (0,0)
        #to do, do not currently have a handle for when one or both whiffs, won't be 0 frames 
        self.state['Timer'] = 62- (time.time()-self.timer)
        self.state['Health'] = (self.player1['Health'], self.player2['Health'])
        
        #over  = self.isFightOver(gameState)
        return self.state

        
    
    
    def update_obs_helper (self,val):
          self.state['Frames'] = (int(val[-1]),int(val[-1]))


    def action_handler(self,action,gameState: TekkenGameState ):
        if action < 6:
            times = random.randint(1,2)
            if(action==0):
                for i in range(times):
                    self.botCommands.BlockMidFull()
            if(action==1):
                for i in range(times):
                    self.botCommands.SidestepLeft()
            if(action==2):  
                 for i in range(times):
                    self.botCommands.SidestepRight()
            if(action==3):  
                 for i in range(times):
                    self.botCommands.Backdash()
            if(action==4):  
                 for i in range(times):
                    self.botCommands.BlockLowFull()
            if(action==5):  
                 for i in range(times):
                    self.botCommands.WalkForward(1)
              
        else:
            action -= 6
            actions = self.update_actions()
            self.botCommands.addNewCommand(actions[action])
      
        self.gameController.Update(gameState.IsForegroundPID(), gameState.IsBotOnLeft())
        self.botCommands.Update(gameState)
        
    
    
   
        
        
    
        

#print(lo.membs())
lo = ActionHandler()
print()
lol = lo.update_actions()
lol= np.insert(lol,1,['1,1']) 
lol = np.insert(lol,3,['2,1'])
print(lol)
#print(lo.rewards())
#print(lo.update_actions())
print(lo.update_actions()[8].split('+'))


class Test():
    def __init__(self):
        self.one = 'q'
        self.twp= '12'
        self.three = '121'


#lo = ActionHandler()
#lo.exm()



"""
       
lo = ActionHandler()
print(lo.used)
print(lo.pan)
#print(lo.update_actions())
lu = lo.update_actions()
lu = lo.update_actions()
lo.update_actions()
uu = np.array(['Move','Stup','Boop','Hoop'])

#print(np.concatenate((uu,lu)) )
print(lo.used)
print(lo.pan)

my_dict = {'Basic Movement' : np.array(range(3)), 'b': np.array(range(4))}

"""
#a_dict = {'ham': np.array([],dtype='<U20')}
#a_dict['ham']  = np.append(a_dict['ham'],'dd' )
num_names = np.array(['ALISA',
'Asuka',
'BOB_SATSUMA',
'Bryan',
'CLAUDIO',
'DEVIL_JIN',  
'Dragunov',
'EDDY'
'FENG',
'Gigas',
'HEIHACHI',
'HWOARANG',
'Jack',
'JIN',
'JOSIE',
'KATARINA',
'KAZUMI',
'KAZUYA',
'KING',
'Kuma',
'Lars',
'LAW',
'LEE',
'LIDIA'
'Eleonor',
'EMILIE',
'Chloe',
'FRV',
'Miguel',
'NINA',
'PANDA',
'Paul',
'SHAHEEN',
'Steve_Fox',
'Lin_Xiaoyu',
'YOSHIMITSU',
'Mr.X',
'Vampire',
'Geese_Howard',
'Noctis',
'ANNA',
'Lei_Wulong',
'MARDUK',
'ARMOR_KING',
'JULIA',
'Negan',
'ZAFINA',
'GANRYU',
'NSB',
'NSC',
'Kunimitsu'])

names = ['ALISA',
'Asuka',
'BOB_SATSUMA',
'Bryan',
'CLAUDIO',
'DEVIL_JIN',  
'Dragunov',
'EDDY'
'FENG',
'Gigas',
'HEIHACHI',
'HWOARANG',
'Jack',
'JIN',
'JOSIE',
'KATARINA',
'KAZUMI',
'KAZUYA',
'KING',
'Kuma',
'Lars',
'LAW',
'LEE',
'LIDIA'
'Eleonor',
'EMILIE',
'Chloe',
'FRV',
'Miguel',
'NINA',
'PANDA',
'Paul',
'SHAHEEN',
'Steve_Fox',
'Lin_Xiaoyu',
'YOSHIMITSU',
'Mr.X',
'Vampire',
'Geese_Howard',
'Noctis',
'ANNA',
'Lei_Wulong',
'MARDUK',
'ARMOR_KING',
'JULIA',
'Negan',
'ZAFINA',
'GANRYU',
'NSB',
'NSC',
'Kunimitsu']

