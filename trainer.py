import gymnasium as gym
from environment import TrafficSignal
from gymnasium.envs.registration import register
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3 import PPO
import os
import time
import renderer
from stable_baselines3 import SAC
from stable_baselines3.common.monitor import Monitor
import re
def get_next_model_path(model_dir="models", prefix="newmodel", extension=".zip"):
    pattern = re.compile(r'-v(\d+)' + re.escape(extension) + r'$')
    max_version = -1

    for filename in os.listdir(model_dir):
        match = pattern.search(filename)
        if match:
            version = int(match.group(1))
            max_version = max(max_version, version)

    next_version = max_version + 1
    next_model_name = f"{prefix}-v{next_version}"
    next_model_path = os.path.join(model_dir, next_model_name)
    return next_model_path



env_id= "TrafficSignal-v0"
model_name='PPO-v0'
register(env_id,entry_point=TrafficSignal)
# env= gym.make(env_id,render_mode="human")
# env= gym.make(env_id)
if __name__ == "__main__":
    # env_fns = [lambda: gym.make(env_id) for _ in range(20)]
    # env = gym.vector.AsyncVectorEnv(env_fns)  # Async for true multiprocessing
    # env = make_vec_env(env_id, n_envs=50)
    env= gym.make(env_id)
    


   
    model_path = os.path.join(os.getcwd(), "models", model_name)
    print(env.reset())
    if os.path.exists(model_path+ ".zip"):
            print("Loading existing model")
            model = PPO.load(model_path, env=env)
            model.set_env(env)
            
            print("Loaded existing model")
    else:
        model = PPO("MultiInputPolicy", env,verbose=1)
            
        #model = PPO("MultiInputPolicy",env, verbose=1,tensorboard_log="./ppo_tensorboard/")
        #model = PPO("MlpPolicy",env, verbose=1,tensorboard_log="./ppo_tensorboard/")
        
    obs,info = env.reset()
    
    last_saved_model=0
    

    

    # Example usage
    
    
    while True:
        print("started training")
        model.learn(total_timesteps=100000,reset_num_timesteps=False,log_interval=1) 
       
        model.save(model_path) 
        print("saved model")
        print("saving copy")
        next_path = get_next_model_path(prefix="PPO")
        
        model.save(next_path) 