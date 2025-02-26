"""
Alex Schaffer
February 26, 2025
Homework 7 - Pygame
Description: Simple frogger game using pygame and Python 3
"""
import pygame

# init pygame
pygame.init()

# setup screen
width = 1080
height = 720
screen = pygame.display.set_mode((width, height))

# set window title
pygame.display.set_caption("Frogger Dodger")

# setting fps
clock = pygame.time.Clock()
dt = 0
speed = 10

"""GAME LOOP"""
running = True
while running:
    """Handle events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    """Update game state"""

    """draw to the screen"""
    # clear screen
    screen.fill("black")

    #Finish line rectangle
    pygame.draw.rect(screen, "dark green", pygame.Rect((0,0), (width, 75) ))

    #Lower rect start area for frog
    pygame.draw.rect(screen, "dark green", pygame.Rect((0,height - 75), (width, 75) ))

    #Lane creation
    lane_height = (height - 150) // 3 #dividing middle area into 3 lanes
    middle_x = width // 2 #this is to divide the lane in half to draw dash
    dash_length = 20
    gap_length = 20

    #draw 3 lanes and split them into 2 with a dashed line
    for lane in range(3):
        lane_y_start = 75 + lane * lane_height
        #Outline each lane with solid gray to show more "road" no drawing on ends
        pygame.draw.line(screen, "gray", (0, lane_y_start), (width, lane_y_start), 2) #top edge
        pygame.draw.line(screen, "gray", (0, lane_y_start + lane_height), (width, lane_y_start + lane_height), 2) #bottom edge
        #dashed lane line
        dash_y = lane_y_start + lane_height // 2
        x = 0
        while x < width:
            pygame.draw.line(screen, "gray", (x, dash_y), (x + dash_length, dash_y), 2)
            x += dash_length + gap_length

    # update screen
    pygame.display.flip()

    # fps
    dt = clock.tick(speed) / 1000

# quit app
pygame.quit()