import numpy as np

class Body: # camelcase for class names
    def __init__(self, mass: float, position: np.ndarray, velocity: np.ndarray):
        # position and velocity should be 1D arrays
        self.m = mass
        self.r = position
        self.v = velocity

    # maybe getter setter functions are unneccesary for this

    # def get_m(self) -> float:
    #     return self._m
    
    # def get_r(self) -> np.ndarray:
    #     return self._r

    # def get_v(self) -> np.ndarray:
    #     return self._v
    
    # def set_r(self, position: np.ndarray):
    #     self._r = position

    # def set_v(self, velocity: np.ndarray):
    #     self._v = velocity
        
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
            body.r(state_vector[self.dim * i : self.dim * (i+1)])
            body.v(state_vector[self.dim * (self.size + i) : self.dim * (self.size + i + 1)])

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

    def differential_equations(self, state: np.ndarray, time: np.ndarray, masses: np.ndarray)->np.ndarray:
        state_length = len(state)
        array_shape = (self.size, self.dim)
        positions = state[:state_length//2].reshape(array_shape) 
        velocities = state[state_length//2:].reshape(array_shape)
        accelerations = np.zeros(array_shape)

        for i in range(self.size):
            for j in range(self.size):
                if i != j:
                    r_ij = positions[i] - positions[j]
                    dist_ij = np.linalg.norm(r_ij)
                    accelerations[i] += - System.G * masses[j] * r_ij / dist_ij**3
        
        derivatives = np.concatenate((velocities.flatten(), accelerations.flatten()))
        return derivatives

    def __repr__(self):
        COM_position, COM_velocity = self.get_COM_position_and_velocity()
        return f"SYSTEM DESCRIPTION: \nBodies: {self.bodies}, \nSize: {self.size}, Dimension: {self.dim}, \nState: {self.get_state()}, \nCOM position: {COM_position}, COM velocity: {COM_velocity}"
