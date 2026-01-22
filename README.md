# Traffic Light RL - Reinforcement Learning Traffic Signal Control

An intelligent traffic signal control system using deep reinforcement learning (PPO - Proximal Policy Optimization) to optimize traffic flow at a four-way intersection.

## Overview

This project implements a custom Gymnasium environment that simulates a four-way traffic intersection. A reinforcement learning agent learns to control traffic signal timing to minimize congestion and wait times for vehicles approaching the intersection.

## Project Structure

```
traffic_light_RL/
├── environment.py      # Custom Gymnasium environment for traffic simulation
├── trainer.py          # Training script for the RL agent (PPO)
├── tester.py           # Evaluation script to test trained models
├── renderer.py         # Pygame-based visualization for traffic simulation
├── test.ipynb          # Jupyter notebook for experimentation and analysis
├── models/             # Directory containing trained model checkpoints
└── __pycache__/        # Python cache files
```

## Requirements

- Python 3.8+
- gymnasium
- stable-baselines3
- numpy
- pygame

Install dependencies:

```bash
pip install gymnasium stable-baselines3 numpy pygame
```

## Components

### Environment (environment.py)

Custom Gymnasium environment that simulates a four-way traffic intersection with:

- **State Space**: Dictionary containing:
  - Vehicle count per lane (0-10 vehicles)
  - Wait times for vehicles in each lane
- **Action Space**: 4 discrete actions corresponding to which lane gets the green light (North, East, South, West)
- **Reward System**: Encourages minimizing wait times and penalizes opening lanes with no traffic
- **Traffic Dynamics**: Random traffic density per episode with vehicle queue simulation

### Trainer (trainer.py)

Implements the training pipeline using:

- **Algorithm**: PPO (Proximal Policy Optimization) from stable-baselines3
- **Features**:
  - Automatic model versioning (PPO-v0, PPO-v1, etc.)
  - Model loading and resuming training
  - Environment registration with Gymnasium

### Tester (tester.py)

Evaluates trained models by:

- Loading a pre-trained PPO model
- Running inference on the environment with visual rendering
- Displaying observations, rewards, and episode completion status

### Renderer (renderer.py)

Pygame-based visualization that displays:

- Four-way intersection layout
- Vehicle positions and movement
- Traffic signal states (Red/Green/Yellow)
- Real-time animation of traffic flow

## Usage

### Training

To train a new model or continue training from an existing checkpoint:

```bash
python trainer.py
```

The trainer will:

- Load the latest model if it exists, or create a new one
- Train using PPO algorithm
- Save checkpoints with incremental version numbers

### Testing/Evaluation

To visualize a trained model's performance:

```bash
python tester.py
```

This will:

- Load the base model (PPO-v0)
- Render the traffic intersection in real-time
- Display state and reward information
- Run until an episode completes

### Experimentation

Use `test.ipynb` for interactive testing, analysis, and experimentation with different aspects of the environment and model.

## Model Checkpoints

The trained model is stored as `PPO-v0.zip` in the `models/` directory.

## Key Features

- **Scalable Architecture**: Built on Gymnasium standard, compatible with various RL algorithms
- **Visual Feedback**: Pygame rendering for intuitive understanding of agent behavior
- **Progressive Training**: Save checkpoints frequently to track improvement
- **Real-time Metrics**: Observation and reward tracking during inference

## Future Improvements

- Multi-agent coordination for multiple intersections
- SAC (Soft Actor-Critic) algorithm experimentation (code already present)
- Vectorized environments for faster training
- Metrics logging and tensorboard integration
- Model validation on different traffic patterns
