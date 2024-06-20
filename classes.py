import numpy as np

class Body: # camelcase for class names
    def __init__(self, mass: float, position: np.ndarray, velocity: np.ndarray):
        # position and velocity should be 1D arrays
        self._m = mass
        self._r = position
        self._v = velocity

    def get_m(self) -> float:
        return self._m
    
    def get_r(self) -> np.ndarray:
        return self._r

    def get_v(self) -> np.ndarray:
        return self._v
    
    def set_r(self, position: np.ndarray):
        self._r = position

    def set_v(self, velocity: np.ndarray):
        self._v = velocity

    # def get_state() -> np.ndarray: dont really need this
        
    def __repr__(self):
        return f"Mass: {self._m}, Position: {self._r}, Velocity: {self._v}"

class System:
    def __init__(self, bodies: list, dimensions = 3):
        self.bodies = bodies
        self.size = len(bodies)
        self.dim = dimensions

    def get_state(self) -> np.ndarray: # returns 1D array with all positions and all velocities concatenated, in that order. e.g.: for 2 dimensions and 2 bodies, [r1_x, r1_y, r2_x, r2_y, v1_x, v1_y, v2_x, v2_y]
        positions = np.concatenate([body.get_r() for body in self.bodies])
        velocities =  np.concatenate([body.get_v() for body in self.bodies])
        return np.concatenate([positions, velocities])

    def set_state(self, state_vector: np.ndarray):
        for i, body in enumerate(self.bodies):
            body.set_r(state_vector[self.dim * i : self.dim * (i+1)])
            body.set_v(state_vector[self.dim * (self.size + i) : self.dim * (self.size + i + 1)])

    def __repr__(self):
        return f"Bodies: {self.bodies}, Dimension: {self.dim}"
