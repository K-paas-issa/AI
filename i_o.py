from balloon_learning_environment.env import grid_based_wind_field
from balloon_learning_environment.env import generative_wind_field

import numpy as np
import datetime as dt
import jax

data = np.loadtxt('./data/data.csv',delimiter=',')
print(data[46000:46500],np.shape(data))
wind_field = generative_wind_field.GenerativeWindField()

data[:][:][:][:][0] = data[:][:][:][0][:]
data[:][:][:][:][1] = data[:][:][:][:][0]

rng = jax.random.PRNGKey(0)
wind_field.reset_forecast(rng, dt.datetime.now())
wind_field.field=data

np.shape(wind_field.field)
