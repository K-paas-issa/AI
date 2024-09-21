
import gym
from balloon_learning_environment.env import balloon_env
from balloon_learning_environment.env import generative_wind_field
from balloon_learning_environment.utils import run_helpers
from balloon_learning_environment.agents import dqn_agent
from balloon_learning_environment.agents import networks

wf = generative_wind_field.GenerativeWindField

agent_name = 'dqn'

env = gym.make(('BalloonLearningEnvironment-v0'),wind_field_factory=wf)
run_helpers.bind_gin_variables(agent_name)
agent = run_helpers.create_agent(agent_name,
env.action_space.n,
env.observation_space.shape)



# @title Run simulation
seed = 0  # @param {type: 'number'}
num_steps = 500  # @param {type: 'number'}
frame_skip = 8  # @param {type: 'number'}
data=[]
times = []
flight_paths = {}
for agen in agent:
  agent_name = agen.get_name()
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


