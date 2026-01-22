import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
import sys
import copy      
import renderer
class TrafficSignal(gym.Env):
    metadata = {"render_modes": ["human"], "render_fps": 4}
    max_step=1000
    def __init__(self,render_mode=None):
        super(TrafficSignal, self).__init__()
        self.render_mode = render_mode

        self.observation_space =spaces.Dict({"a":spaces.Box(low=0,high=10,shape=(4,),dtype=np.int8),
                                            "b":spaces.Box(low=0, high=1000, shape=(4,), dtype=np.float64)})
        self.action_space = spaces.Discrete(4) 
        self.traffic_density=[0]*4
        self.episode_length = 1000
        self.grid = np.zeros((4, 10), dtype=np.int8)
        self.wait_times= np.zeros((4,10), dtype=np.float64)  
        self.frame_to_pass = 2     
        self.step_passed=0
        self.current_open=0
        self.total_step=0
        self.passing=False
        if self.render_mode == "human":
            self.renderer = renderer.Renderer()
               
    def reset(self,options=None, seed=None):
        self.traffic_density = [np.random.randint(1,10)/10 for _ in range(4)]
        self.grid = np.zeros((4, 10), dtype=np.int8)
        self.wait_times= np.zeros((4,10), dtype=np.float64)
        self.step_passed=0
        self.current_open=0
        self.total_step=0
        return {"a":[0]*4,"b":[0]*4}, {}


    def step(self, action):
        reward=0
        passed=False
        if [np.count_nonzero(i) for i in self.grid][action]==0:
            reward -=1
        
        if action != self.current_open:
            self.current_open=action
            self.step_passed=0
            self.passing=False
        
        if self.step_passed >= self.frame_to_pass:
            self.passing=True
            self.grid[action]=np.concatenate((self.grid[action][1:], np.array([0])))
            self.wait_times[action]=np.concatenate((self.wait_times[action][1:], np.array([0])))
            reward += 0.5
            passed=True
        else:
            self.step_passed+=1
            
        for i in range(4):
            if passed and i == self.current_open:
                pass
            else:
                for j in range(1,10):
                    if self.grid[i][j-1] == 0 and self.grid[i][j] == 1:
                        self.grid[i][j-1] = 1
                        self.grid[i][j] = 0
                        
                        self.wait_times[i][j-1]= self.wait_times[i][j]
                        self.wait_times[i][j]=0
        
        # for i in range(4):
        #     if np.random.random()>self.traffic_density[i]:
        #         self.grid[i][-1] = 1   
        
        lane=np.random.randint(0, 4)
        if self.total_step % 1==0:
            if np.random.random() < self.traffic_density[lane] :
                self.grid[lane][-1] = 1
                   
        self.total_step += 1
        
        done = self.total_step >= self.episode_length
        self.wait_times+= self.grid * 1
        wait_time_avg=self.wait_times.mean(axis=1)
        reward-=np.power(wait_time_avg[wait_time_avg>15].sum(),2)/10
        # reward-=0.25
        print(reward)
        if self.render_mode == "human":
            self.render()
            
        if self.total_step >= self.max_step:
            done = True
            print("Episode finished after {} timesteps".format(self.total_step))
        return {"a":[np.count_nonzero(i) for i in self.grid],"b":wait_time_avg}, reward, done, False, {}

    def render(self):
        print("Rendering the environment...")
        self.renderer.draw(self.grid, self.current_open)