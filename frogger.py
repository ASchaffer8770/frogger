"""
Alex Schaffer
March 3, 2025
Homework 8 - Pygame Moving Objects
Schaffer_HW8_MovingObjects
Description: Simple frogger game using pygame and Python 3
"""
import pygame
import helper_functions

# init pygame
pygame.init()

#GLOBAL VARIABLES
# setup screen
width = 1080
height = 720
screen = pygame.display.set_mode((width, height))

# set window title
pygame.display.set_caption("Frogger Dodger")

# setting fps
clock = pygame.time.Clock()
dt = 0
speed = 60

# Define the screen rectangle for clamping
screen_rect = pygame.Rect(0, 0, width, height)

#Dialog button rectangles
restart_button = pygame.Rect(width // 2 - 100, height // 2 + 20, 80, 40)
quit_button = pygame.Rect(width // 2 + 20, height // 2 + 20, 80, 40)

#font for text
font = pygame.font.SysFont(None, 48) #title size 48

# Sprite Classes
class Frog(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30,30)) #30 X 30 Sprite
        self.image.fill("green")
        pygame.draw.circle(self.image, "black", (8,8), 5)#left eye
        pygame.draw.circle(self.image, "black", (22, 8), 5) #right eye
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height - 75 + 37) #area center
        self.reset() #reset on restart

    def reset(self):
        self.rect.center = (width // 2, height - 75 + 37)

class Car(pygame.sprite.Sprite):
    def __init__(self, color, size, start_x, start_y, speed):
        super().__init__()
        self.image = pygame.Surface(size) #custom size (width, height)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = start_x
        self.rect.y = start_y
        self.speed = speed
        self.reset(start_x, start_y) #reset on restart

    def reset(self, start_x, start_y):
        self.rect.x = start_x
        self.rect.y = start_y

# Create sprite groups and instances
all_sprites = pygame.sprite.Group()
cars = pygame.sprite.Group()

frog = Frog()
all_sprites.add(frog)

# TODO: Refactor using functions

lane_height = (height - 150) // 3  # Calculate lane height once
car1 = Car("red", (50, 20), 0, 75 + lane_height // 4, 200)  # Lane 1 top, fast car
car2 = Car("blue", (70, 30), width, 265 + 3 * lane_height // 4, -200)  # Lane 2 bottom, truck
car3 = Car("yellow", (40, 25), 0, 455 + lane_height // 4, 200)  # Lane 3 top, compact car
car4 = Car("green", (60,40), 0, 205 + lane_height // 2, -100) # Lane 1 bottom. semi truck
car5 = Car("grey", (70,30), width, 150 + 3 * lane_height // 4, -150) # Lane 2 top, truck
car6 = Car("orange", (70,30), 0, 440 + 3 * lane_height // 4, 150)# Lane 3 bottom, truck
all_sprites.add(car1, car2, car3, car4, car5, car6)
cars.add(car1, car2, car3, car4, car5, car6)

# TODO: add collision detection

# TODO: add score tracking

# TODO: add timer

#game state variables
PLAYING = 0
WIN = 1
PAUSE = 2
TITLE = 3
game_state = TITLE

"""GAME LOOP"""
running = True
while running:
    """Handle events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_state == TITLE and event.type == pygame.KEYDOWN:
            game_state = PLAYING
        if game_state == PLAYING and event.type == pygame.KEYDOWN:  # Frog movement
            if event.key == pygame.K_UP:
                frog.rect.y -= 50
            if event.key == pygame.K_DOWN:
                frog.rect.y += 50
            if event.key == pygame.K_LEFT:
                frog.rect.x -= 50
            if event.key == pygame.K_RIGHT:
                frog.rect.x += 50
            #Checking for Pause action
            if event.key == pygame.K_ESCAPE:
                game_state = PAUSE
        if game_state == WIN and event.type == pygame.MOUSEBUTTONDOWN:  # Button clicks
            if restart_button.collidepoint(event.pos):
                frog.reset()
                car1.reset(0, 75 + lane_height // 4)
                car2.reset(width, 265 + 3 * lane_height // 4)
                car3.reset(0, 455 + lane_height // 4)
                game_state = PLAYING
            elif quit_button.collidepoint(event.pos):
                running = False

    """Update game state"""
    if game_state == PLAYING:
        #set car speed
        car1.rect.x += car1.speed * dt
        #set car direction
        if car1.rect.x > width:
            car1.rect.x = -car1.rect.width
        # TODO: Make cars 4,5,6 move appropriately
        #speed
        car4.rect.x += car4.speed * dt
        #direction
        if car4.rect.x > width:
            car4.rect.x = -car4.rect.width
        #speed
        car2.rect.x += car2.speed * dt
        #direction
        if car2.rect.x < -car2.rect.width:
            car2.rect.x = width
        car3.rect.x += car3.speed * dt
        if car3.rect.x > width:
            car3.rect.x = -car3.rect.width
        #Boundary for frog
        frog.rect.clamp_ip(screen_rect)

    #Check for win condition
    if frog.rect.y < 75:
        game_state = WIN

    """draw to the screen"""
    # clear screen
    screen.fill("black")

    if game_state == TITLE:
        # Draw title text
        title_text = font.render("Frogger Dodger", True, "white")
        screen.blit(title_text, (width // 2 - title_text.get_width() // 2, height // 2 - 50))
        # Draw start prompt
        start_text = font.render("Press any key to start", True, "white")
        how_text = font.render("Use the up down left right arrows to move frogger", True, "white")
        pause_text = font.render("Esc key to pause the game", True, "white")
        #draw text
        screen.blit(pause_text, (width // 2 - pause_text.get_width() // 2, height // 2 + 10))
        screen.blit(how_text, (width // 2 - how_text.get_width() // 2, height // 2 + 50))
        screen.blit(start_text, (width // 2 - start_text.get_width() // 2, height // 2 + 110))
    else:

        #Finish line rectangle
        pygame.draw.rect(screen, "dark green", pygame.Rect((0,0), (width, 75) ))
        #Lower rect start area for frog
        pygame.draw.rect(screen, "dark green", pygame.Rect((0,height - 75), (width, 75) ))

        #Lane variables
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

        # Draw the sprites
        all_sprites.draw(screen)

    # Draw win dialog if applicable
    if game_state == WIN:
        # Dialog background
        dialog_rect = pygame.Rect(width // 2 - 200, height // 2 - 125, 400, 250)
        pygame.draw.rect(screen, "gray", dialog_rect)
        pygame.draw.rect(screen, "black", dialog_rect, 2)  # Border

        # "You Win!" text
        win_text = font.render("Roger Roger we have a Dodger!", True, "white")
        screen.blit(win_text, (width // 2 - win_text.get_width() // 2, height // 2 - 80))

        # TODO: Fix the alignment on the win dialogue
        # Buttons
        pygame.draw.rect(screen, "green", restart_button)  # Restart button
        pygame.draw.rect(screen, "red", quit_button)  # Quit button
        restart_text = font.render("Restart", True, "white")
        quit_text = font.render("Quit", True, "white")
        screen.blit(restart_text, (restart_button.x + 10, restart_button.y + 10))
        screen.blit(quit_text, (quit_button.x + 25, quit_button.y + 10))

    # TODO finish pause screen, need a main menu button, a resume button, and a exit program button
    if game_state == PAUSE:
        #Dialog for Pause game
        dialog_rect = pygame.Rect(width // 2 -200, height // 2 - 125, 400, 350)
        pygame.draw.rect(screen, "purple", dialog_rect)
        pygame.draw.rect(screen, "green", dialog_rect, 2)

    # update screen
    pygame.display.flip()

    # fps
    dt = clock.tick(speed) / 1000

# quit app
pygame.quit()