# @title Create environments and agents
import gym
from balloon_learning_environment.env import balloon_env
from balloon_learning_environment.env import generative_wind_field
from balloon_learning_environment.utils import run_helpers

wf = generative_wind_field.GenerativeWindField
agents = []
envs = []
for agent in ['dqn']:
  envs.append(gym.make('BalloonLearningEnvironment-v0',
                       wind_field_factory=wf))
  agents.append(run_helpers.create_agent(
      agent,
      envs[-1].action_space.n,
      observation_shape=envs[-1].observation_space.shape))

