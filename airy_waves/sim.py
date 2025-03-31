"""
airy_wave.py
------------
This script simulates a one-dimensional Airy wave (linear water wave) using the
equation:
    η(x,t) = a cos(k x - ω t)

with the dispersion relation:

    ω = sqrt(g * k * tanh(k * h))

Parameters such as amplitude, wavelength, water depth, and simulation duration
can be modified.
"""

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np


def main():
    # Physical parameters
    g = 9.81  # gravitational acceleration (m/s^2)
    a = 1.0  # wave amplitude (m)
    wavelength = 10.0  # wavelength (m)
    k = 2 * np.pi / wavelength  # wave number (rad/m)
    h = 50.0  # water depth (m)

    # Dispersion relation: ω = sqrt(g*k*tanh(k*h))
    omega = np.sqrt(g * k * np.tanh(k * h))

    # Spatial domain for simulation
    x = np.linspace(0, 2 * wavelength, 500)

    # Set up the plot
    fig, ax = plt.subplots()
    (line,) = ax.plot(x, np.zeros_like(x), lw=2)
    ax.set_xlim(x[0], x[-1])
    ax.set_ylim(-2 * a, 2 * a)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("Surface Elevation (m)")
    ax.set_title("1D Airy Wave Simulation")

    # Time stepping parameters
    dt = 0.02  # time step (s)
    total_time = 10  # total simulation time (s)
    frames = int(total_time / dt)

    def update(frame):
        # Current time
        t = frame * dt
        # Calculate wave surface elevation using the Airy wave theory formula
        y = a * np.cos(k * x - omega * t)
        line.set_data(x, y)
        return (line,)

    # Create the animation
    ani = animation.FuncAnimation(
        fig, update, frames=frames, interval=dt * 1000, blit=True
    )

    plt.show()


if __name__ == "__main__":
    main()