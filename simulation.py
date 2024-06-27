import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from classes import *

'''
constants and initial variables
'''

# gravitational constant (N*m^2*kg^-2)
GRAVITATIONAL_CONSTANT = 6.67430e-11 # all caps for constants is conventional

# masses (kg) 
m1 = 0.00001
m2 = 2.71828
m3 = 3.14159

# initial positions (m)
r1_initial = np.array([0.0, 0.0, 0.0])
r2_initial = np.array([-1.0, 0.0, 0.0])
r3_initial = np.array([1.0, 0.0, 0.0])

# initial velocities (m/s)
v1_initial = np.array([0.0, 0.0, 0.0])
v2_initial = np.array([0.0, 1.0, 0.0])
v3_initial = np.array([0.0, -1.0, 0.0])

# object construction
b1 = Body(m1, r1_initial, v1_initial)
b2 = Body(m2, r2_initial, v2_initial)
b3 = Body(m3, r3_initial, v3_initial)
bodies = np.array([b1,b2,b3])
system = System(bodies)
