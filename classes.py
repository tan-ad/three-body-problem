import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
import plotly.graph_objects as go

class Body: # camelcase for class names
    def __init__(self, mass: float, position: np.ndarray, velocity: np.ndarray):
        # position and velocity should be 1D arrays
        self.m = mass
        self.r = position
        self.v = velocity
        
    def __repr__(self):
        return f"Mass: {self.m}, Position: {self.r}, Velocity: {self.v}"

class System:
    G = 6.67430e-11 # gravitational constant (N*m^2*kg^-2)

    def __init__(self, bodies: list[Body], dimensions: int = 3):
        self.bodies = bodies
        self.size = len(bodies)
        self.dim = dimensions

    def get_state(self) -> np.ndarray: # returns 1D array with all positions and all velocities concatenated, in that order. e.g.: for 2 dimensions and 2 bodies, [r1_x, r1_y, r2_x, r2_y, v1_x, v1_y, v2_x, v2_y]
        positions = np.concatenate([body.r for body in self.bodies])
        velocities =  np.concatenate([body.v for body in self.bodies])
        return np.concatenate([positions, velocities])

    def set_state(self, state_vector: np.ndarray):
        for i, body in enumerate(self.bodies):
            body.r=state_vector[self.dim * i : self.dim * (i+1)]
            body.v=state_vector[self.dim * (self.size + i) : self.dim * (self.size + i + 1)]

    def get_COM_position_and_velocity(self) -> tuple[list[float],list[float]]: # returns position_of_COM,velocity_of_COM
        position_of_COM = []
        velocity_of_COM = []
        for dimension in range(self.dim): # note: could change variable names? dk what is ideal.
            numerator_r = 0 # total mass*position
            numerator_v = 0 # total mass*velocity (momentum)
            denominator = 0 # total mass
            for i in range(self.size):
                numerator_r += self.bodies[i].m*self.bodies[i].r[dimension]
                numerator_v += self.bodies[i].m*self.bodies[i].v[dimension]
                denominator += self.bodies[i].m
            answer_r = numerator_r/denominator # position of COM in one dimension
            answer_v = numerator_v/denominator # velocity of COM in one dimension
            position_of_COM.append(answer_r)
            velocity_of_COM.append(answer_v)
        return position_of_COM,velocity_of_COM
    
    def set_to_COM_reference(self):
        position_of_COM, velocity_of_COM = self.get_COM_position_and_velocity()
        for dimension in range(self.dim):
            for i in range(self.size):
                self.bodies[i].r[dimension] -= position_of_COM[dimension]
                self.bodies[i].v[dimension] -= velocity_of_COM[dimension]

    def differential_equations(self, time: np.ndarray, state: np.ndarray, masses: np.ndarray)->np.ndarray:
        state_length = len(state)
        array_shape = (self.size, self.dim)
        positions = state[:state_length//2].reshape(array_shape)
        dR_over_dt = state[state_length//2:].reshape(array_shape)
        dv_over_dt = np.zeros(array_shape)
        for i in range(self.size):
            for j in range(self.size):
                if i != j:
                    r_ij = positions[i] - positions[j]
                    dist_ij = np.linalg.norm(r_ij)
                    dv_over_dt[i] += - System.G * masses[j] * r_ij / dist_ij**3
        
        derivatives = np.concatenate((dR_over_dt.flatten(), dv_over_dt.flatten()))
        return derivatives
    
    def get_solution(self, simulation_length):
        masses = []
        for body in self.bodies:
            masses.append(body.m)
        initial_state = self.get_state()
        t_span = [0.0,simulation_length]
        t_eval = np.arange(t_span[0], t_span[1], 0.01) # or 
        # t_eval = np.linspace(t_span[0], t_span[1], 1000) # difference is explicit interval length vs explicit number of intervals
        solution = solve_ivp(self.differential_equations, t_span, initial_state, args=(masses,), t_eval=t_eval)
        # fun fact: in numpy, a 2d array is indexed using array[row_indices, column_indices]
        # another fun fact: can slice columns like solution.y[:,0]
        return solution

    # ALL PLOTTING FUNCTIONS WRITTEN FOR 3D
    # wherever I use self.dim, I may as well just use 3
    def plot_lines_matplotlib(self, solution): # initial attempt at visualizing - not very good. for 3 bodies
        solution_states = solution.y # array of 2*dim*size arrays, each containing values for each time value we chose to compute
        positions = solution_states[:self.size * self.dim].reshape((self.size, self.dim, -1)) 
        # we slice solution_states to get just the position data, which is a tensor of shape (size*dim, number of time instances)
        # need to reshape to 3d tensor of shape (size, dim, number of time instances) so that the first layer of elements corresponds to values for each body, next layer corresponds to positions in each dimension, and last layer corresponds to positions in each dimension at specific times. 
        # -1 is a placeholder that tells numpy to automatically calculate the size of this dimension based on the length of the array and the other specified dimensions.

        fig = plt.figure()
        ax = fig.add_subplot(221, projection='3d')
        for i in range(self.size):
            ax.plot(positions[i, 0], positions[i, 1], positions[i, 2], label=f'Body {i+1}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        plt.show()

    def plot_lines_plotly(self, solution): # second attempt, more or less the same as first, need to figure out better visualization
        positions = solution.y[:self.size * self.dim].reshape((self.size, self.dim, -1)) 

        fig = go.Figure()
        for i in range(self.size):
            fig.add_trace(go.Scatter3d(
                x=positions[i, 0, :],
                y=positions[i, 1, :],
                z=positions[i, 2, :],
                mode='lines',
                name=f'Body {i+1}'
            ))
        fig.update_layout(
            scene=dict(
                xaxis=dict(title='X', range=[positions[:, 0, :].min(), positions[:, 0, :].max()]),
                yaxis=dict(title='Y', range=[positions[:, 1, :].min(), positions[:, 1, :].max()]),
                zaxis=dict(title='Z', range=[positions[:, 2, :].min(), positions[:, 2, :].max()]),
                aspectmode='cube'
            ),
            title='3D Trajectories of Bodies'
        )

        fig.show()

    def plot_animation(self, solution, tail_length=50):
        positions = solution.y[:self.size * 3].reshape((self.size, 3, -1))
        fig = go.Figure()
        frames = []

        # n-body implementation
        colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'purple', 'orange', 'brown'] # len = 10
        for n in range(self.size):
            fig.add_trace(go.Scatter3d(x=[positions[n,0,0]], y=[positions[n,1,0]], z=[positions[n,2,0]], mode='markers', marker=dict(size=5, color=colors[n%10]), name=f'Body {n+1}'))
            fig.add_trace(go.Scatter3d(x=[], y=[], z=[], mode='lines', line=dict(width=2, color=colors[n%10]), name=f'Tail {n+1}'))


        # n-body
        for i in range(len(solution.t)):
            frame_data = [go.Scatter3d(x=[positions[n,0,i]], y=[positions[n,1,i]], z=[positions[n,2,i]], mode='markers', marker=dict(size=5, color=colors[n%10])) for n in range(self.size)]
            if i > tail_length:
                for n in range(self.size):
                    frame_data.append(go.Scatter3d(x=positions[n,0][i-tail_length:i], y=positions[n,1][i-tail_length:i], z=positions[n,2][i-tail_length:i], mode='lines', line=dict(width=2, color=colors[n%10])))
            else:
                for n in range(self.size):
                    frame_data.append(go.Scatter3d(x=positions[n,0][:i], y=positions[n,1][:i], z=positions[n,2][:i], mode='lines', line=dict(width=2, color=colors[n%10])))
            frames.append(go.Frame(data=frame_data))

        fig.frames = frames

        fig.update_layout(updatemenus=[dict(type='buttons', showactive=False, buttons=[dict(label='Play', method='animate', args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=True)])])])

        fig.show()

    def __repr__(self):
        COM_position, COM_velocity = self.get_COM_position_and_velocity()
        return f"SYSTEM DESCRIPTION: \nBodies: \n{self.bodies}, \nSize: {self.size}, Dimension: {self.dim}, \nState: {self.get_state()}, \nCOM position: {COM_position}, COM velocity: {COM_velocity}"

