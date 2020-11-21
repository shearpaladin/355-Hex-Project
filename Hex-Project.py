
import pygame, sys
from pygame.locals import *

# GLOBALS
# Define Grid Size
grid = [ [1] * 8 for n in range(8)]

# Store Hexagons
hexagon_list = []
# define shape sizes
w = 70
# define colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (220,220,220)

# Vertices
INITIAL_HEXAGON_VERTICES = ((-40,-40),(40,-40),(45,0),(40,40),(-40,40),(-45,0))

# Size of Grid
GRID_HEIGHT = 10
GRID_WIDTH = 10

# Each Vertice in the hexagon
VERTEX_COUNT = 6

# Hexagon class to know each Hexagon Number Generated
class Hexagon:

    def __init__(self,num,ver):

        self.number = num
        self.vertices = ver


# set up pygame
pygame.init()

# Resolution Size let's make it fixed so we can calculate
# how big our rectangles take up on our board
windowSurface = pygame.display.set_mode((800, 600),0, 32)

# Set Caption of Project
pygame.display.set_caption('Hex Project')

# Background Color
#windowSurface.fill(WHITE)


index = 0
for column in range(GRID_WIDTH):
    for row in range(GRID_HEIGHT):

        points = []
        lift_hexagon = 0

        if column % 2 != 0:
            lift_hexagon = 40

        for point in range(VERTEX_COUNT):

            points.append(  ((INITIAL_HEXAGON_VERTICES[point][0] + (85 * column)),
                            ((INITIAL_HEXAGON_VERTICES[point][1] + (80 * row))-lift_hexagon)  ) )

        new_hexagon = Hexagon(index,points)
        hexagon_list.append(new_hexagon)
        index += 1


windowSurface.fill(GRAY)

for i in range(len(hexagon_list)):
    pygame.draw.polygon(windowSurface,BLACK,hexagon_list[i].vertices,3)

pygame.display.flip()




# draw the window onto the screen
#pygame.display.update()

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
