import numpy as np
from classes import *

# masses (kg) 
m1 = 10.0**11
m2 = 10.0**11
m3 = 10.0**11

# initial positions (m)
r1_initial = np.array([0.0, 0.0, 0.0])
r2_initial = np.array([1.0, 0.0, 0.0])
r3_initial = np.array([0.5, np.sqrt(3)/2, 0.0])

# initial velocities (m/s)
v1_initial = np.array([1.0, -np.sqrt(3), 0.0])
v2_initial = np.array([1.0, np.sqrt(3), 0.0])
v3_initial = np.array([-2.0, 0.0, 0.0])


# object construction
b1 = Body(m1, r1_initial, v1_initial)
b2 = Body(m2, r2_initial, v2_initial)
b3 = Body(m3, r3_initial, v3_initial)
bodies = np.array([b1,b2,b3])
system = System(bodies)

# solve initial value problem
system.set_to_COM_reference()
# system.plot_lines_matplotlib(system.get_solution())
print(system)
solution = system.get_solution(10)
# system.plot_lines_plotly(solution)
system.plot_animation(solution)
