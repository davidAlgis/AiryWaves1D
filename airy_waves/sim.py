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
        Computes the water velocity (u, v) at a given point (x, y).

        For points above the free surface, returns (0, 0).

        Parameters:
            x: Horizontal coordinate.
            y: Vertical coordinate.

        Returns:
            A tuple (u, v) representing the water velocity components.
        """
        eta = self.get_water_height(x)
        if y > eta:
            return (0.0, 0.0)

        u = (
            (self.a * self.g * self.k / self.omega)
            * (np.cosh(self.k * (y + self.h)) / np.cosh(self.k * self.h))
            * np.cos(self.k * x - self.omega * self.t)
        )
        v = (
            (self.a * self.g * self.k / self.omega)
            * (np.sinh(self.k * (y + self.h)) / np.cosh(self.k * self.h))
            * np.sin(self.k * x - self.omega * self.t)
        )
        return (u, v)