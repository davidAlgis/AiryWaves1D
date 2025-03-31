#!/usr/bin/env python3
"""
airy_wave.py

This module defines a class AiryWaves to simulate a one-dimensional Airy wave.
It contains methods to update the wave state, get the water surface height,
and compute the water velocity at a given point. Points above the free surface
yield a velocity of (0, 0).
"""

import numpy as np


class AiryWaves:
    """
    A class to simulate a one-dimensional Airy wave.
    """

    def __init__(
        self, amplitude=1.0, wavelength=10.0, water_depth=50.0, gravity=9.81
    ):
        """
        Initializes the Airy wave with given parameters.

        Parameters:
          amplitude   : Wave amplitude (a)
          wavelength  : Wavelength of the wave
          water_depth : Depth of the water (h)
          gravity     : Gravitational acceleration (g)
        """
        self.a = amplitude
        self.wavelength = wavelength
        self.h = water_depth
        self.g = gravity

        self.k = 2 * np.pi / wavelength  # Wave number (rad/m)
        self.omega = np.sqrt(
            self.g * self.k * np.tanh(self.k * self.h)
        )  # Angular frequency (rad/s)
        self.t = 0.0  # Initial time

    def update(self, t):
        """
        Updates the wave state to a new time t.

        Parameters:
          t : New time (float)
        """
        self.t = t

    def get_water_height(self, x):
        """
        Returns the water surface height at a given horizontal position x.

        Parameters:
          x : Horizontal coordinate (float)

        Returns:
          The water height at x.
        """
        return static_get_water_height(x, self)

    def get_water_velocity(self, x, y):
        """
        Returns the water velocity at a given point (x, y).

        Parameters:
          x : Horizontal coordinate (float)
          y : Vertical coordinate (float)

        Returns:
          A tuple (u, v) representing the water velocity.
        """
        return static_get_water_velocity(x, y, self)


def static_get_water_height(x, wave):
    """
    Returns the water surface elevation at horizontal position x based on the
    current state of the wave. The free surface is given by:

        η(x,t) = a * cos(k * x - ω * t)

    Parameters:
      x    : horizontal coordinate (float)
      wave : instance of AiryWaves providing a, k, ω, and current time t

    Returns:
      The water surface elevation at x.

    """
    return wave.a * np.cos(wave.k * x - wave.omega * wave.t)


def static_get_water_velocity(x, y, wave):
    """
            Returns the water velocity (u,v) at the given point (x,y).
            For points above the water surface (y > η(x,t)), the velocity is
    (0, 0).
            For points inside the water (y <= η(x,t)), the velocity components
            are computed using linear (Airy) wave theory. The velocity
        potential is given by:
                φ(x,y,t) = (a * g / ω) * (cosh(k*(y + h)) / cosh(k*h)) *
    sin(k*x - ω*t)
            so that:

                u = ∂φ/∂x = (a * g * k / ω) * (cosh(k*(y + h)) / cosh(k*h)) *
                cos(k*x - ω*t) v = ∂φ/∂y = (a * g * k / ω) * (sinh(k*(y + h)) /
        cosh(k*h)) * sin(k*x - ω*t)
            Parameters:
              x    : horizontal coordinate (float)
              y    : vertical coordinate (float)
              wave : instance of AiryWaves providing a, k, ω, h, g, and current
    time t
            Returns:
              A tuple (u, v) representing the horizontal and vertical water
            velocity components.

    
    """
    # Compute the free surface elevation at x
    eta = static_get_water_height(x, wave)
    # If the point is above the free surface, velocity is zero.
    if y > eta:
        return (0.0, 0.0)

    # Compute the velocity components using linear wave theory.
    u = (
        (wave.a * wave.g * wave.k / wave.omega)
        * (np.cosh(wave.k * (y + wave.h)) / np.cosh(wave.k * wave.h))
        * np.cos(wave.k * x - wave.omega * wave.t)
    )
    v = (
        (wave.a * wave.g * wave.k / wave.omega)
        * (np.sinh(wave.k * (y + wave.h)) / np.cosh(wave.k * wave.h))
        * np.sin(wave.k * x - wave.omega * wave.t)
    )
    return (u, v)


# Example usage (for testing purposes only; remove if integrating into a larger
# project)
if __name__ == "__main__":
    wave = AiryWaves(amplitude=1.0, wavelength=10.0, water_depth=50.0)
    wave.update(0.5)  # Update wave to time t = 0.5 seconds

    x_pos = 5.0
    height = wave.get_water_height(x_pos)
    print("Water height at x = {:.2f}: {:.3f}".format(x_pos, height))

    # Test water velocity at a point below the free surface
    velocity_inside = wave.get_water_velocity(x_pos, -1.0)
    print(
        "Water velocity at (x, y) = ({:.2f}, {:.2f}): (u, v) = ({:.3f},"
        "{:.3f})".format(x_pos, 0.0, velocity_inside[0], velocity_inside[1])
    )

    # Test water velocity at a point above the free surface
    velocity_above = wave.get_water_velocity(x_pos, height + 1.0)
    print(
        "Water velocity at (x, y) = ({:.2f}, {:.2f}): (u, v) = ({:.3f},"
        "{:.3f})".format(
            x_pos, height + 1.0, velocity_above[0], velocity_above[1]
        )
    )