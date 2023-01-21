# Simple pygame program
import math

from HexGrid import HexGrid
from HexGridStorage import HexGridStorage



def axial_to_evenr(q, r):
    col = q + (r + (r % 2)) / 2
    row = -r
    return col - (row % 2) / 2, row * 0.75


# Import and initialize the pygame library

import pygame

pygame.init()

# Set up the drawing window
SIZE = [1000, 1000]
screen = pygame.display.set_mode(SIZE)

# Run until the user asks to quit
hexgrid = HexGridStorage(SIZE, screen, 10)

running = True
print(axial_to_evenr(0, -1))
while running:

    # Did the user click the window close button?
    events = pygame.event.get()
    for event in events:

        if event.type == pygame.QUIT:
            running = False
    hexgrid.handle(events)
    # Fill the background with white

    screen.fill((200, 200, 200))
    hexgrid.draw()

    # Flip the display

    # hexgrid.fill_square()
    pygame.display.flip()

# Done! Time to quit.

pygame.quit()
