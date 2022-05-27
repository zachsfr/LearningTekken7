import gym
from gym import spaces,Env
import numpy as np
from TekkenGameState import TekkenGameState
from event_handeler import *


Movements = { 'simple': np.array(['Block','SSL','SSR','BackDash','Duck']),
              'full': np.array(['Block','SSL','SSR','BackDash','Duck','Forward' ])
        
            }


class TekkenEnv(Env):
    """Custom Environment that follows gym interface"""
  
    # We need to observe several key things
    # our current frames, opp current frames
    # are either of us attacking
    # start the round by observing , not attacking, update actions as we go
    
    
    # 
    
    def __init__(self):
        super().__init__()
        self.action_handler = ActionHandler() 
        
        # Define action and observation space
        # They must be gym.spaces objects
        # Example when using discrete actions:
        #self.action_space = action
        # Example for using image as input (channel-first; channel-last also works):
        
        self.observation_space = spaces.Dict({
        'Round Timer': spaces.Box(low=0, high=60, shape=(1,), dtype=np.int32),

            'Health': spaces.Tuple( (
                spaces.Box(low=0, high=175, shape=(1,), dtype=np.int32), 
                spaces.Box(low=0, high=175, shape=(1,), dtype=np.int32),   

            )),

            'Frames':spaces.Tuple( (
                spaces.Box(low=-20, high=20, shape=(1,), dtype=np.int32), 
                spaces.Box(low=-20, high=20, shape=(1,), dtype=np.int32),   

            )),  
            'Opponet': spaces.Discrete(50),
            'State': spaces.Tuple((
                spaces.Discrete(4),
                spaces.Discrete(4)
            )),        
            'whiff': spaces.Tuple((
                spaces.Discrete(2),
                spaces.Discrete(2)
            )) 
        
        })
        
        self.action_space = spaces.Discrete(len(Movements['simple']))
        self.stepped = 0
        self.just_started = True



         


    def step(self, action,gameState: TekkenGameState):
        
  
        gameState.Update()
        
        observation = self.action_handler.take_action(action,gameState)
        
        done =gameState.WasFightReset() or self.action_handler.isFightOver()

        if self.just_started:
            # basic template of using prior knowledge to speed up learning
            # at the start of the round, player should not be  choosing to move forward or attack
            # safest bet is to wait and see what opponet does, this forces that to happen 
            # without having to make that behavior be learned 

            # to do, add more prior knowledge, such as automatically 
            # performing combos when a launcher is landed
            # using correct punisher attack when blocking an unsafe attack and so on
            
            self.update_actions(observation)
            
        
        if( done):
            print("oh no!")
            reward,info = self.action_handler.finished(gameState)
           
        else:
            info =  self.action_handler.info
            reward = 0

       
        
       
        
        return observation, reward, done, info
    
    def update_actions(self,obs):
        if self.stepped > 2:
            attacks = self.action_handler.update_actions()

            updated_actions = np.concatenate((Movements['full'],attacks))

            self.action_space = spaces.Discrete(len(updated_actions))
            self.just_started = False
        self.stepped +=1
        

        
        
    
    def reset(self):
        self.just_started =True
        self.stepped =0
        self.action_handler.reset()
        
        # basic template of game values to use for analysis
        # best to start simple and add as neccessary
        # too much information makes it difficult for any model to gain any meaniful insight
        # best to find the least number of variables required that give the most information
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
            #to do, dummy variable for opponet currently
            # will add a function that matches the gameState variale to a saved list
            # of all characters, using the index number for each opponet 
            'State': (
                0,
                0,
            #to do, dummey variable atm, state will check where opponet and palyer are
            # checking if they are standing, grounded, juggeled, wall splatted, counter hit ect.      
            ),        
            'whiff': (
                0,
                0
            ) 
        
        }
        
        
        return self.state  
    
    def close (self):
        return

