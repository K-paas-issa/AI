import numpy as np
import gym
from balloon_learning_environment.env import balloon_env
from balloon_learning_environment.env import generative_wind_field
from balloon_learning_environment.utils import run_helpers
wf = generative_wind_field.GenerativeWindField
agents = []
envs = []
for agent in [ 'dqn']:
  envs.append(gym.make('BalloonLearningEnvironment-v0', wind_field_factory=wf))
  agents.append(run_helpers.create_agent(
      agent,
      envs[-1].action_space.n,
      observation_shape=envs[-1].observation_space.shape))
# @title Run simulation
seed = 0  # @param {type: 'number'}
num_steps = 5000  # @param {type: 'number'}
frame_skip = 8  # @param {type: 'number'}
data=[]
times = []
flight_paths = {}
for i, agent in enumerate(agents):
  agent_name = agent.get_name()
  print(f'Running simulation for {agent_name}')
  total_reward = 0.0
  steps_within_radius = 1
  flight_paths[agent_name] = list()

  envs[i].seed(seed)
  observation = envs[i].reset()
  action = agent.begin_episode(observation)
  observation = envs[i].reset()
  action = agent.begin_episode(observation)

  step_count = 0
  while step_count < num_steps:
    observation, reward, is_done, info = envs[i].step(action)
    action = agent.step(reward, observation)

    total_reward += reward
    sim_state = envs[i].get_simulator_state()
    balloon_state = sim_state.balloon_state
    if step_count % frame_skip == 0:
      altitude = sim_state.atmosphere.at_pressure(balloon_state.pressure).height
#      charge = balloon_state.battery_soc * 1.0
      charge=0
      flight_paths[agent_name].append((balloon_state.x.km, balloon_state.y.km,
                                       altitude.km, charge))
      data.append([balloon_state.x.km,balloon_state.y.km,
                                       altitude.km,reward])
      if i == 0:
        times.append(balloon_state.date_time)

    step_count += 1

    if is_done:
      break

  agent.end_episode(reward, is_done)
np.save('./data.npy',np.array(data))
