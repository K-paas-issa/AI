# @title Create environments and agents
import gym
from balloon_learning_environment.env import balloon_env
from balloon_learning_environment.env import generative_wind_field
from balloon_learning_environment.utils import run_helpers
from balloon_learning_environment.agents import dqn_agent
from dopamine.jax.agents.dqn import JaxDQNagent
from balloon_learning_environment.agents import agent


wf = generative_wind_field.GenerativeWindField
agents = []
envs = []

agenth=dqn_agent.DQNAgent(agent.Agent,dqn_agent.JaxDQNAgent)


for agent in [agenth]:
  

  envs.append(gym.make('BalloonLearningEnvironment-v0',
                       wind_field_factory=wf))
  agents.append(agent)
print(clear)
