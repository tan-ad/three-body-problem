import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from classes import *

'''
constants and initial variables
'''



# masses (kg) 
m1 = 0.00001
m2 = 2.71828
m3 = 3.14159
masses = [m1, m2, m3]

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

COM_position, COM_velocity = system.get_COM_position_and_velocity()
print(system)
system.set_to_COM_reference()
print(system)

initial_state = system.get_state()
t_interval = np.arange(0, 25.0, 0.01)
t_span = [0.0,10.0]
t_eval = np.arange(t_span[0], t_span[1], 0.01) # or np.linspace(t_span[0], t_span[1], 1000), difference is explicit interval length vs explicit number of intervals
solution = solve_ivp(system.differential_equations, t_span, initial_state, args=(masses,), t_eval=t_eval)
# fun fact: in nump, a 2d array is indexed using array[row_indices, column_indices]
print(solution.y)
print(len(solution.y))
print(len(solution.y[0]))
for i in range(18):
    print(solution.y[i][0])

solution_states = solution.y # array of 2*dim*size arrays, each containing values for each time value we chose to compute

positions = solution_states[:system.size * system.dim]
# positions = solution_points.reshape((system.size, system.dim, -1)) # -1 is a placeholder that tells numpy to automatically calculate the size of this dimension based on the length of the array and the other specified dimensions


# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

# for i in range(num_bodies):
#     ax.plot(positions[i, 0], positions[i, 1], positions[i, 2], label=f'Body {i+1}')

# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
# ax.legend()
# plt.show()