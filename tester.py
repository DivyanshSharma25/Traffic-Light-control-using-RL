import gymnasium as gym
from stable_baselines3 import PPO
from gymnasium.envs.registration import register
from environment import TrafficSignal
import os
import time
env_id= "TrafficSignal-v0"
model_name='PPO-v0'
model_path = os.path.join(os.getcwd(), "models", model_name)
register(
    id=env_id,
    entry_point=TrafficSignal,
)
env= gym.make(env_id,render_mode='human')
model=PPO.load(model_path,env=env)
obs, info = env.reset()
while True:
    action, _states = model.predict(obs)  # Use learned policy
    obs, reward, done, _, _ = env.step(action)
    print(obs, reward, done, _, _)
    # env.render()  # Show environment in real-time
    time.sleep(0.3)  # Slow down the loop for better visualization
    if done:
        break  # Start a new episode