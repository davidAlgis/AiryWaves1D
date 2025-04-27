"""
airy_waves/sim.py

This module defines the AiryWaves class that simulates a 1D Airy wave.
It uses the parameters stored in the AiryWavesParams class from init_helper.
"""

import numpy as np
from airy_waves.init_helper import AiryWavesParams


class AiryWaves:
    def __init__(self, params: AiryWavesParams):
        """
                Initializes the Airy wave simulation using parameters from
        AiryWavesParams.
                Parameters:
                    params: An instance of AiryWavesParams containing the
                simulation parameters.

        """
        self.a = params.amplitude
        self.wavelength = params.wavelength
        self.h = params.water_depth
        self.g = params.gravity

        self.k = 2 * np.pi / self.wavelength  # Wave number (rad/m)
        self.omega = np.sqrt(
            self.g * self.k * np.tanh(self.k * self.h)
        )  # Angular frequency (rad/s)
        self.t = 0.0  # Initial time

    def update(self, t: float):
        """
        Updates the simulation time.

        Parameters:
            t: The new simulation time.
        """
        self.t = t

    def get_water_height(self, x: float) -> float:
        """
        Computes the free-surface elevation at a given horizontal position x.

        η(x,t) = a * cos(k*x - ω*t)

        Parameters:
            x: Horizontal coordinate.

        Returns:
            The water surface height at x.
        """
        return self.a * np.cos(self.k * x - self.omega * self.t)

    def get_water_velocity(self, x: float, y: float):
        """
        Computes the water velocity (u,v) at a given point (x,y).
        For points above the free surface, returns (0,0).

        Uses deep-water approximations when k*h is very large.
        """
        eta = self.get_water_height(x)
        if y > eta:
            return (0.0, 0.0)

        factor = np.exp(self.k * y)
        u = (
            (self.a * self.g * self.k / self.omega)
            * factor
            * np.cos(self.k * x - self.omega * self.t)
        )
        v = (
            (self.a * self.g * self.k / self.omega)
            * factor
            * np.sin(self.k * x - self.omega * self.t)
        )
        return (u, v)

    def get_water_velocity_t(self, x: float, y: float, t: float):
        """
        Computes the water velocity (u,v) at a given point (x,y).
        For points above the free surface, returns (0,0).

        Uses deep-water approximations when k*h is very large.
        """
        eta = self.get_water_height(x)
        if y > eta:
            return (0.0, 0.0)

        factor = np.exp(self.k * y)
        u = (
            (self.a * self.g * self.k / self.omega)
            * factor
            * np.cos(self.k * x - self.omega * t)
        )
        v = (
            (self.a * self.g * self.k / self.omega)
            * factor
            * np.sin(self.k * x - self.omega * t)
        )
        return (u, v)

    def get_water_force(self, x: float, y: float, mass: float, dt: float):
        """
                Estimates the force exerted by the water on a mass at the given point
        over time dt.
                The force is computed as:
                    F = mass * (water_velocity / dt)

                Parameters:
                  x: Horizontal coordinate.
                  y: Vertical coordinate.
                  mass: The mass of the particle.
                  dt: The time step over which the acceleration is applied.

                Returns:
                  A tuple (F_x, F_y) representing the force components.

        """
        u_new, v_new = self.get_water_velocity_t(x, y, self.t + dt)
        u_old, v_old = self.get_water_velocity_t(x, y, self.t)
        F_x = mass * (u_new - u_old) / dt
        F_y = mass * (v_new - v_old) / dt
        return (F_x, F_y)
