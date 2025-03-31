import numpy as np
import pytest
from airy_waves.sim import AiryWaves


def test_water_height_at_origin():
    """
    At time t=0 and x=0 the free-surface elevation should be a * cos(0)=a.
    """
    amplitude = 2.0
    wavelength = 10.0
    water_depth = 50.0
    gravity = 9.81
    wave = AiryWaves(
        amplitude=amplitude,
        wavelength=wavelength,
        water_depth=water_depth,
        gravity=gravity,
    )
    wave.update(0.0)
    height = wave.get_water_height(0.0)
    assert np.isclose(height, amplitude, atol=1e-6), f"Expected {amplitude},"
    f"got {height}"


def test_water_velocity_above_free_surface():
    """
    Points above the free surface should return a velocity of (0, 0).
    """
    amplitude = 1.0
    wavelength = 10.0
    water_depth = 50.0
    gravity = 9.81
    wave = AiryWaves(
        amplitude=amplitude,
        wavelength=wavelength,
        water_depth=water_depth,
        gravity=gravity,
    )
    wave.update(0.0)
    # At x=0 the free surface is at amplitude (since cos(0)=1), so sample
    # slightly above.
    height = wave.get_water_height(0.0)
    velocity = wave.get_water_velocity(0.0, height + 0.1)
    assert velocity == (0.0, 0.0), f"Expected (0,0), got {velocity}"


def test_water_velocity_below_free_surface():
    """
    For a point inside the water (x=0, y=0 at t=0), the horizontal velocity
        should be: u = (a * g * k / ω) * (cosh(k*(0+h))/cosh(k*h)) = a * g * k
    / ω, and the vertical velocity should be zero since sin(0)=0.

    """
    amplitude = 1.0
    wavelength = 10.0
    water_depth = 50.0
    gravity = 9.81
    wave = AiryWaves(
        amplitude=amplitude,
        wavelength=wavelength,
        water_depth=water_depth,
        gravity=gravity,
    )
    wave.update(0.0)
    velocity = wave.get_water_velocity(0.0, 0.0)
    k = 2 * np.pi / wavelength
    omega = np.sqrt(gravity * k * np.tanh(k * water_depth))
    expected_u = amplitude * gravity * k / omega
    expected_v = 0.0
    assert np.isclose(velocity[0], expected_u, atol=1e-6), f"Expected"
    f"u={expected_u}, got {velocity[0]}"
    assert np.isclose(velocity[1], expected_v, atol=1e-6), f"Expected"
    f"v={expected_v}, got {velocity[1]}"


def test_time_update_effect():
    """
    Verify that the update method properly advances the simulation.
    At x=0:
      - At t=0, the height should be a * cos(0)= a.
      - At t=1, the height should be a * cos(-ω) = a * cos(ω).
    """
    amplitude = 1.0
    wavelength = 10.0
    water_depth = 50.0
    gravity = 9.81
    wave = AiryWaves(
        amplitude=amplitude,
        wavelength=wavelength,
        water_depth=water_depth,
        gravity=gravity,
    )
    # Time t=0
    wave.update(0.0)
    height0 = wave.get_water_height(0.0)
    # Time t=1
    wave.update(1.0)
    height1 = wave.get_water_height(0.0)
    k = 2 * np.pi / wavelength
    omega = np.sqrt(gravity * k * np.tanh(k * water_depth))
    expected_height0 = amplitude
    expected_height1 = amplitude * np.cos(-omega)
    assert np.isclose(height0, expected_height0, atol=1e-6), f"Expected"
    f"{expected_height0}, got {height0}"
    assert np.isclose(height1, expected_height1, atol=1e-6), f"Expected"
    f"{expected_height1}, got {height1}"