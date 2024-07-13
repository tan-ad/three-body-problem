import numpy as np
from classes import *

def run_simulation(system: System, length:float):
    # solve initial value problem
    system.set_to_COM_reference()
    solution = system.get_solution(length)
    system.plot_animation(solution)

def main():
    # masses (kg) 
    m1 = 10.0**11
    m2 = 10.0**11
    m3 = 10.0**11
    m4 = 10.0**11

    # initial positions (m)
    r1_initial = np.array([0.0, 0.0, 0.0])
    r2_initial = np.array([1.0, 0.0, 0.0])
    r3_initial = np.array([0.5, np.sqrt(3)/2, 0.0])
    r4_initial = np.array([0.0, 0.0, 2.0])

    # initial velocities (m/s)
    v1_initial = np.array([1.0, -np.sqrt(3), 0.0])
    v2_initial = np.array([1.0, np.sqrt(3), 0.0])
    v3_initial = np.array([-2.0, 0.0, 0.0])
    v4_initial = np.array([1.0, 0.0, 0.0])

    # object construction
    b1 = Body(m1, r1_initial, v1_initial)
    b2 = Body(m2, r2_initial, v2_initial)
    b3 = Body(m3, r3_initial, v3_initial)
    b4 = Body(m4, r4_initial, v4_initial)
    bodies = np.array([b1,b2,b3, b4])
    system = System(bodies)

    # animate
    seconds = 10.0
    run_simulation(system, seconds)

if __name__ == "__main__":
    main()
