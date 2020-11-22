
import pygame, sys
from pygame.locals import *

## GLOBALS ##

# Store Hexagons
hexagon_list = []



# define colors
BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (220,220,220)

# Map to center
# We can add a offset to Map our grid to the center
offset = 150

# Vertices
#INITIAL_HEXAGON_VERTICES = ((-40,-40),(40,-40),(45,0),(40,40),(-40,40),(-45,0))
#INITIAL_HEXAGON_VERTICES = ((-20,-20),(20,-20),(25,0),(20,20),(-20,20),(-25,0))
#INITIAL_HEXAGON_VERTICES = ((50,25),(100,0),(150,25),(150,75),(100,100),(50,75))
INITIAL_HEXAGON_VERTICES = ((50+offset,25+offset),(100+offset,0+offset),(150+offset,25+offset),(150+offset,75+offset),(100+offset,100+offset),(50+offset,75+offset))

# Size of Grid 3x3
GRID_HEIGHT = 3
GRID_WIDTH = 3

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
pygame.display.set_caption('Hex Project 3x3')

# Background Color
#windowSurface.fill(WHITE)


index = 0

for column in range(GRID_WIDTH):
    for row in range(GRID_HEIGHT):

        points = []
        #lift_hexagon = 0

        lift_hexagon_x = 0
        lift_hexagon_y = 0

        # if column % 2 != 0:
        #     lift_hexagon_x = 5

        if row % 2 != 0:
            lift_hexagon_x = -50
            lift_hexagon_y = 25

        elif row % 3 != 0:
            lift_hexagon_x = -100
            lift_hexagon_y = 50



        for point in range(VERTEX_COUNT):

            points.append(  ( (INITIAL_HEXAGON_VERTICES[point][0] + (100 * column) -lift_hexagon_x),
                            ( (INITIAL_HEXAGON_VERTICES[point][1] + (100 * row))-lift_hexagon_y)  ) )

        new_hexagon = Hexagon(index,points)
        hexagon_list.append(new_hexagon)
        index += 1


windowSurface.fill(GRAY)

for i in range(len(hexagon_list)):
    # parameters of pygame.draw.polygon (surface, color, points, width)
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
