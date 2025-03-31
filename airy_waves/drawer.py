"""
airy_waves/drawer.py

This module defines the AiryWavesDrawer class which uses pygame to display the
1D Airy wave and a field of velocity vectors beneath the free surface.
"""

import numpy as np
import pygame


class AiryWavesDrawer:
    def __init__(
        self,
        wave,
        width=800,
        height=600,
        arrow_scale=0.5,
        grid_x=20,
        grid_y=10,
    ):
        """
        Initializes the drawer.

        Parameters:
            wave: An instance of the AiryWaves simulation.
            width: Width of the pygame window in pixels.
            height: Height of the pygame window in pixels.
            arrow_scale: Scaling factor for velocity arrows.
            grid_x: Number of grid points in the horizontal direction for the
            velocity field. grid_y: Number of grid points in the vertical
        direction for the velocity field.
        """
        self.wave = wave
        self.width = width
        self.height = height
        self.arrow_scale = arrow_scale
        self.grid_x = grid_x
        self.grid_y = grid_y

        # Define simulation domain for display.
        # Horizontal domain: 0 to 2 * wavelength.
        self.x_min = 0
        self.x_max = 2 * wave.wavelength
        # Vertical domain: from water bottom (-water_depth) to a top margin
        # above the free surface.
        self.margin = 1.0
        self.y_top = wave.a + self.margin
        self.y_bottom = -wave.h

        # Scaling factors to convert simulation coordinates (meters) to screen
        # coordinates (pixels).
        self.scale_x = self.width / (self.x_max - self.x_min)
        self.scale_y = self.height / (self.y_top - self.y_bottom)

        # Initialize pygame.
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Airy Waves Simulation")
        self.clock = pygame.time.Clock()

    def sim_to_screen(self, x, y):
        """
        Converts simulation coordinates (x, y) to screen coordinates (sx, sy).

        In simulation, y increases upward; in pygame, y increases downward.
        """
        sx = (x - self.x_min) * self.scale_x
        sy = (self.y_top - y) * self.scale_y
        return int(sx), int(sy)

    def draw(self):
        """
        Draws the current state of the wave and the velocity field.
        """
        # Fill background (sky blue).
        self.screen.fill((135, 206, 250))

        # Draw water surface (free surface line).
        n_points = 200
        x_vals = np.linspace(self.x_min, self.x_max, n_points)
        surface_points = []
        for x in x_vals:
            y = self.wave.get_water_height(x)
            surface_points.append(self.sim_to_screen(x, y))
        if len(surface_points) > 1:
            pygame.draw.lines(
                self.screen, (0, 0, 255), False, surface_points, 2
            )

        # Draw velocity field as arrows.
        # Use a nonlinear mapping for vertical grid to concentrate arrows near
        # the free surface.
        for i in range(self.grid_x):
            for j in range(self.grid_y):
                # Horizontal coordinate is still uniformly spaced.
                x = self.x_min + i * (self.x_max - self.x_min) / (
                    self.grid_x - 1
                )
                # Compute a normalized parameter p in [0,1] and use p^2 to
                # concentrate near the top.
                p = j / (self.grid_y - 1)
                y = self.y_top - (self.y_top - self.y_bottom) * (p**2)
                free_surface = self.wave.get_water_height(x)
                if y <= free_surface:
                    u, v = self.wave.get_water_velocity(x, y)
                    start_pos = self.sim_to_screen(x, y)
                    # Draw the arrow with the specified scale.
                    dx_screen = int(u * self.arrow_scale * self.scale_x)
                    dy_screen = -int(v * self.arrow_scale * self.scale_y)
                    end_pos = (
                        start_pos[0] + dx_screen,
                        start_pos[1] + dy_screen,
                    )
                    pygame.draw.line(
                        self.screen, (255, 0, 0), start_pos, end_pos, 2
                    )
                    pygame.draw.circle(self.screen, (255, 0, 0), end_pos, 3)

        pygame.display.flip()

    def handle_events(self):
        """
        Processes pygame events.
        Returns True if the simulation should continue, or False if a quit
        event is detected.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def tick(self, fps=60):
        """
        Regulates the frame rate.
        """
        self.clock.tick(fps)