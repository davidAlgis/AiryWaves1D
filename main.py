"""
main.py

Entry point for the 1D Airy wave simulation with pygame visualization.
"""

import argparse

import pygame
from airy_waves.drawer import AiryWavesDrawer
from airy_waves.sim import AiryWaves


def main():
    parser = argparse.ArgumentParser(
        description="Simulate and display a 1D Airy wave using pygame."
    )
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
        "--dt",
        type=float,
        default=0.1,
        help="Time step for simulation (default: 0.1 seconds)",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=100.0,
        help="Total simulation duration in seconds (default: 10.0; use 0 for"
        "infinite)",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=800,
        help="Window width in pixels (default: 800)",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=600,
        help="Window height in pixels (default: 600)",
    )
    parser.add_argument(
        "--arrow_scale",
        type=float,
        default=0.5,
        help="Scaling factor for velocity arrows (default: 0.5)",
    )
    parser.add_argument(
        "--grid_x",
        type=int,
        default=20,
        help="Number of grid points in x direction for velocity field"
        "(default: 20)",
    )
    parser.add_argument(
        "--grid_y",
        type=int,
        default=10,
        help="Number of grid points in y direction for velocity field"
        "(default: 10)",
    )
    parser.add_argument(
        "--fps", type=int, default=60, help="Frames per second (default: 60)"
    )
    args = parser.parse_args()

    # Create the simulation instance.
    wave = AiryWaves(
        amplitude=args.amplitude,
        wavelength=args.wavelength,
        water_depth=args.water_depth,
        gravity=args.gravity,
    )

    # Create the drawer instance.
    drawer = AiryWavesDrawer(
        wave,
        width=args.width,
        height=args.height,
        arrow_scale=args.arrow_scale,
        grid_x=args.grid_x,
        grid_y=args.grid_y,
    )

    current_time = 0.0
    running = True

    while running:
        # Process pygame events.
        running = drawer.handle_events()

        # If a positive duration is set and the simulation time is exceeded,
        # exit.
        if args.duration > 0 and current_time > args.duration:
            running = False
            continue

        # Update the simulation state.
        wave.update(current_time)

        # Draw the current state.
        drawer.draw()

        # Increment simulation time.
        current_time += args.dt

        # Regulate the frame rate.
        drawer.tick(args.fps)

    pygame.quit()


if __name__ == "__main__":
    main()