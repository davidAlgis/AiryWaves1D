"""
main.py

This is the entry point for the 1D Airy wave simulation.
It parses command-line arguments to set the simulation parameters,
creates an instance of the AiryWaves simulation, and then runs a
simulation loop printing the wave state.
"""

import argparse

from airy_waves.sim import AiryWaves  # Ensure your simulation class is defined

# in airy_waves/sim.py


def main():
    parser = argparse.ArgumentParser(description="Simulate a 1D Airy wave.")
    parser.add_argument(
        "--amplitude",
        type=float,
        default=1.0,
        help="Wave amplitude (default: 1.0)",
    )
    parser.add_argument(
        "--wavelength",
        type=float,
        default=10.0,
        help="Wavelength (default: 10.0)",
    )
    parser.add_argument(
        "--water_depth",
        type=float,
        default=50.0,
        help="Water depth (default: 50.0)",
    )
    parser.add_argument(
        "--gravity",
        type=float,
        default=9.81,
        help="Gravitational acceleration (default: 9.81)",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=10.0,
        help="Total simulation duration in seconds (default:" "10.0)",
    )
    parser.add_argument(
        "--dt",
        type=float,
        default=0.1,
        help="Time step for simulation (default: 0.1)",
    )
    parser.add_argument(
        "--x",
        type=float,
        default=5.0,
        help="x position to sample water height and velocity" "(default: 5.0)",
    )
    parser.add_argument(
        "--y",
        type=float,
        default=0.0,
        help="y position to sample water velocity (default:" "0.0)",
    )
    args = parser.parse_args()

    # Create the AiryWaves simulation instance with the provided parameters
    wave = AiryWaves(
        amplitude=args.amplitude,
        wavelength=args.wavelength,
        water_depth=args.water_depth,
        gravity=args.gravity,
    )

    current_time = 0.0

    while current_time <= args.duration:
        wave.update(current_time)
        water_height = wave.get_water_height(args.x)
        water_velocity = wave.get_water_velocity(args.x, args.y)
        current_time += args.dt
    print("Simulation done !")


if __name__ == "__main__":
    main()