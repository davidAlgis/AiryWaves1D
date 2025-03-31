"""
airy_waves/init_helper.py

This module contains a helper class that stores the parameters for the
AiryWaves simulation.
"""


class AiryWavesParams:
    def __init__(
        self, amplitude=1.0, wavelength=10.0, water_depth=50.0, gravity=9.81
    ):
        self.amplitude = amplitude
        self.wavelength = wavelength
        self.water_depth = water_depth
        self.gravity = gravity