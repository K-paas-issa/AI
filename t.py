import datetime as dt
import numpy as np
import jax
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import rc
rc('animation', html='jshtml')
import gym
from balloon_learning_environment.env import balloon_env
from balloon_learning_environment.env import generative_wind_field
from balloon_learning_environment.utils import run_helpers

wind_field = generative_wind_field.GenerativeWindField()
rng = jax.random.PRNGKey(0)
wind_field.reset_forecast(rng, dt.datetime.now())
wf = generative_wind_field.GenerativeWindField

agents = []
envs = []
for agent in ['station_seeker', 'perciatelli44', 'random_walk']:
  envs.append(gym.make('BalloonLearningEnvironment-v0',
                       wind_field_factory=wf))
  agents.append(run_helpers.create_agent(
      agent,
      envs[-1].action_space.n,
      observation_shape=envs[-1].observation_space.shape))


print("clear")
