import numpy as np

class Body:
    def __init__(self, position: np.ndarray, velocity: np.ndarray):
        # position and velocity should be 1D arrays
        # really dont need this private public nonsense as python doesnt distinguish and i am the only developer working on this, but its good OOP practice?
        self.__position = position
        self.__velocity = velocity

    def get_position(self) -> np.ndarray:
        return self.__position

    def get_velocity(self) -> np.ndarray:
        return self.__velocity
    
    def set_position(self, position: np.ndarray):
        self.__position = position

    def set_velocity(self, velocity: np.ndarray):
        self.__velocity = velocity

    def __repr__(self):
        return f"Position: {self.__position}, Velocity: {self.__velocity}"

class System:
    def __init__(self, bodies: list):
        self.__bodies = bodies
        self.size = 

    def get_state_vector(self) -> np.ndarray:
        num_bodies = len(self.__bodies)
        state = np.concatenate([body.get_state() for body in self.bodies])
        return state

    def set_state_vector(self, state_vector: np.ndarray):
        for i, body in enumerate(self.bodies):
            body.set_state(state_vector[i*6:(i+1)*6])

    def __repr__(self):
        return f"Bodies: {self.bodies}"
