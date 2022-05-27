from gym import Env 
from matplotlib import pyplot as plt
import numpy as np
from gym.spaces import MultiBinary, Box
from TekkenGameState import *
from game_values import TekkenEncyclopedia
import time
import game_values
import gymTekken
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.vec_env import DummyVecEnv, VecFrameStack
import os

class ModelHandeler:
    def __init__(self):
        self.env = gymTekken.TekkenEnv()

        self.obs =  self.env.reset()
        self.gameState = TekkenGameState()
        self.count = 0
    
    def main(self):
        
        successfulUpdate = self.gameState.Update()
        if successfulUpdate:
    
            if self.gameState.IsOppAbleToAct() and self.count ==0:
                time.sleep(2.5)
                self.count = 1
                self.env.reset()
            
            if self.count !=0:
            
                obs, reward, done, info = self.env.step(self.env.action_space.sample(), self.gameState)
                time.sleep(.03)
                if(done):
                    self.count=0
                    self.obs =  self.env.reset()
                
                if reward > 0:
                    print(reward) 
                    print(info)

if __name__ == "__main__":

  
    launch = ModelHandeler()
    while(True):
        launch.main()
        time.sleep(.01)
        
        