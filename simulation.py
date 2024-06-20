import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import plotly.graph_objects as go

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
r1_initial = [0.0, 0.0, 0.0]
r2_initial = [-1.0, 0.0, 0.0]
r3_initial = [1.0, 0.0, 0.0]

# initial velocities (m/s)
v1_initial = [0.0, 0.0, 0.0]
v2_initial = [0.0, 1.0, 0.0]
v3_initial = [0.0, -1.0, 0.0] 

