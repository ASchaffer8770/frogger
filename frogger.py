"""
Alex Schaffer
March 3, 2025
Homework 8 - Pygame Moving Objects
Schaffer_HW8_MovingObjects
Description: Simple frogger game using pygame and Python 3
"""
import pygame
import helper_functions
import math
import random

# Initialize Pygame
pygame.init()

# GLOBAL CONSTANTS
WIDTH = 1080
HEIGHT = 720
FPS = 60
LANE_COUNT = 3
TIME_LIMIT = 60
STARTING_LIVES = 3

# Colors
COLORS = {
    "BLACK": "black",
    "WHITE": "white",
    "GRAY": "gray",
    "GREEN": "green",
    "RED": "red",
    "PURPLE": "purple",
    "DARK_GREEN": "dark green",
    "DARK_GRAY": "dark gray"
}

# Game states
PLAYING, WIN, TITLE, GAME_OVER = 0, 1, 2, 3

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Frogger Dodger")
clock = pygame.time.Clock()
base_font_size = 48
font = pygame.font.SysFont(None, base_font_size)
small_font = pygame.font.SysFont(None, 36)

def setup_game():
    """Initialize sprites and groups with randomized car positions and speeds"""
    all_sprites = pygame.sprite.Group()
    cars = pygame.sprite.Group()

    frog = helper_functions.Frog(WIDTH, HEIGHT)
    all_sprites.add(frog)

    lane_height = (HEIGHT - 150) // LANE_COUNT
    cars_data = [
        ("red", (50, 20), random.randint(-50, WIDTH), 75 + lane_height // 4, random.randint(150, 250)),
        ("blue", (70, 30), random.randint(-70, WIDTH), 265 + 3 * lane_height // 4, -random.randint(150, 250)),
        ("yellow", (40, 25), random.randint(-40, WIDTH), 455 + lane_height // 4, random.randint(150, 250)),
        ("green", (60, 40), random.randint(-60, WIDTH), 205 + lane_height // 2, -random.randint(100, 200)),
        ("grey", (70, 30), random.randint(-70, WIDTH), 75 + 3 * lane_height // 4, -random.randint(100, 200)),
        ("orange", (70, 30), random.randint(-70, WIDTH), 440 + 3 * lane_height // 4, random.randint(100, 200))
    ]

    for color, size, x, y, speed in cars_data:
        car = helper_functions.Car(color, size, x, y, speed)
        all_sprites.add(car)
        cars.add(car)

    return all_sprites, cars, frog, cars_data

def reset_game(frog, cars, cars_data):
    """Reset frog and car positions with new random values"""
    frog.reset(WIDTH, HEIGHT)
    lane_height = (HEIGHT - 150) // LANE_COUNT
    new_cars_data = [
        ("red", (50, 20), random.randint(-50, WIDTH), 75 + lane_height // 4, random.randint(150, 250)),
        ("blue", (70, 30), random.randint(-70, WIDTH), 265 + 3 * lane_height // 4, -random.randint(150, 250)),
        ("yellow", (40, 25), random.randint(-40, WIDTH), 455 + lane_height // 4, random.randint(150, 250)),
        ("green", (60, 40), random.randint(-60, WIDTH), 205 + lane_height // 2, -random.randint(100, 200)),
        ("grey", (70, 30), random.randint(-70, WIDTH), 75 + 3 * lane_height // 4, -random.randint(100, 200)),
        ("orange", (70, 30), random.randint(-70, WIDTH), 440 + 3 * lane_height // 4, random.randint(100, 200))
    ]
    for car, (color, size, x, y, speed) in zip(cars, new_cars_data):
        car.reset(x, y)
        car.speed = speed
    return new_cars_data

def handle_events(game_state, frog, restart_button, quit_button, running, cars, cars_data, lives):
    """Handle all game events and return updated lives"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return game_state, False, cars_data, lives
        if game_state == TITLE and event.type == pygame.KEYDOWN:
            return PLAYING, running, cars_data, lives
        if game_state == PLAYING and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                frog.move(0, -50)
            elif event.key == pygame.K_DOWN:
                frog.move(0, 50)
            elif event.key == pygame.K_LEFT:
                frog.move(-50, 0)
            elif event.key == pygame.K_RIGHT:
                frog.move(50, 0)
        if game_state == WIN and event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                new_cars_data = reset_game(frog, cars, cars_data)
                return PLAYING, running, new_cars_data, lives
            elif quit_button.collidepoint(event.pos):
                return game_state, False, cars_data, lives
        if game_state == GAME_OVER and event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                return TITLE, running, cars_data, lives
            elif quit_button.collidepoint(event.pos):
                return game_state, False, cars_data, lives
    return game_state, running, cars_data, lives

def update_game(game_state, all_sprites, frog, cars, dt, timer, lives):
    """Update game objects, timer, and lives; return updated state and lives"""
    if game_state == PLAYING:
        screen_rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        frog.update(dt)
        frog.rect.clamp_ip(screen_rect)

        for car in cars:
            car.update(dt, WIDTH)

        if pygame.sprite.spritecollide(frog, cars, False):
            lives -= 1
            frog.reset(WIDTH, HEIGHT)
            if lives <= 0:
                return GAME_OVER, lives

        timer -= dt
        if timer <= 0:
            return GAME_OVER, lives

        if frog.rect.y < 75:
            return WIN, lives
    return game_state, lives

def draw_game(screen, game_state, all_sprites, frog, cars, timer, lives):
    """Handle all drawing"""
    screen.fill(COLORS["BLACK"])

    if game_state == TITLE:
        draw_title_screen(screen)
    elif game_state == GAME_OVER:
        draw_game_over_screen(screen)
    else:
        draw_game_elements(screen, all_sprites)
        if game_state == PLAYING:
            draw_hud(screen, timer, lives)
        if game_state == WIN:
            draw_win_dialog(screen)

    pygame.display.flip()

def draw_title_screen(screen):
    """Draw title screen"""
    texts = [
        ("Frogger Dodger", HEIGHT // 2 - 50),
        ("Press any key to start", HEIGHT // 2 + 110),
        ("Use the up down left right arrows to move frogger", HEIGHT // 2 + 50)
    ]
    for text, y in texts:
        surface, pos = helper_functions.create_text(font, text, COLORS["WHITE"], WIDTH // 2, y)
        screen.blit(surface, pos)

def draw_game_elements(screen, all_sprites):
    """Draw main game elements"""
    pygame.draw.rect(screen, COLORS["DARK_GREEN"], (0, 0, WIDTH, 75))
    pygame.draw.rect(screen, COLORS["DARK_GREEN"], (0, HEIGHT - 75, WIDTH, 75))

    lane_height = (HEIGHT - 150) // LANE_COUNT
    for lane in range(LANE_COUNT):
        y = 75 + lane * lane_height
        pygame.draw.line(screen, COLORS["GRAY"], (0, y), (WIDTH, y), 2)
        pygame.draw.line(screen, COLORS["GRAY"], (0, y + lane_height), (WIDTH, y + lane_height), 2)
        helper_functions.draw_dashed_line(screen, y + lane_height // 2, WIDTH)

    all_sprites.draw(screen)

def draw_hud(screen, timer, lives):
    """Draw timer and lives HUD"""
    timer_text = small_font.render(f"Time: {int(timer)}s", True, COLORS["WHITE"])
    lives_text = small_font.render(f"Lives: {lives}", True, COLORS["WHITE"])
    screen.blit(timer_text, (10, 10))
    screen.blit(lives_text, (WIDTH - lives_text.get_width() - 10, 10))

def draw_win_dialog(screen):
    """Draw win dialog with pulsating restart button and text"""
    dialog_rect = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 175, 600, 350)
    base_restart_rect = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 80, 100, 50)
    quit_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 80, 100, 50)

    helper_functions.draw_dialog(screen, dialog_rect, COLORS["GRAY"], COLORS["BLACK"])

    win_text = "Roger Roger we have a Dodger!"
    text_surface, text_pos = helper_functions.create_text(font, win_text, COLORS["WHITE"],
                                                         WIDTH // 2, HEIGHT // 2 - 50)
    screen.blit(text_surface, text_pos)

    time = pygame.time.get_ticks() / 1000
    pulse_scale = 1 + 0.1 * math.sin(time * 5)
    restart_width = int(100 * pulse_scale)
    restart_height = int(50 * pulse_scale)
    restart_x = WIDTH // 2 - 120 - (restart_width - 100) // 2
    restart_y = HEIGHT // 2 + 80 - (restart_height - 50) // 2
    restart_button = pygame.Rect(restart_x, restart_y, restart_width, restart_height)

    restart_font_size = int(base_font_size * pulse_scale * 0.6)
    restart_font = pygame.font.SysFont(None, restart_font_size)
    restart_text = restart_font.render("Restart", True, COLORS["WHITE"])

    pygame.draw.rect(screen, COLORS["GREEN"], restart_button)
    pygame.draw.rect(screen, COLORS["WHITE"], restart_button, 2)
    pygame.draw.rect(screen, COLORS["RED"], quit_button)

    screen.blit(restart_text, (restart_button.x + (restart_width - restart_text.get_width()) // 2,
                              restart_button.y + (restart_height - restart_text.get_height()) // 2))
    quit_text = font.render("Quit", True, COLORS["WHITE"])
    screen.blit(quit_text, (quit_button.x + (100 - quit_text.get_width()) // 2,
                           quit_button.y + (50 - quit_text.get_height()) // 2))

def draw_game_over_screen(screen):
    """Draw game over screen with options"""
    dialog_rect = pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 175, 600, 350)
    restart_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 80, 100, 50)
    quit_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 80, 100, 50)

    helper_functions.draw_dialog(screen, dialog_rect, COLORS["GRAY"], COLORS["BLACK"])

    game_over_text = "Game Over!"
    text_surface, text_pos = helper_functions.create_text(font, game_over_text, COLORS["WHITE"],
                                                         WIDTH // 2, HEIGHT // 2 - 50)
    screen.blit(text_surface, text_pos)

    pygame.draw.rect(screen, COLORS["GREEN"], restart_button)
    pygame.draw.rect(screen, COLORS["RED"], quit_button)

    restart_text = font.render("Menu", True, COLORS["WHITE"])
    quit_text = font.render("Quit", True, COLORS["WHITE"])
    screen.blit(restart_text, (restart_button.x + (100 - restart_text.get_width()) // 2,
                              restart_button.y + (50 - restart_text.get_height()) // 2))
    screen.blit(quit_text, (quit_button.x + (100 - quit_text.get_width()) // 2,
                           quit_button.y + (50 - quit_text.get_height()) // 2))

def main():
    """Main game loop"""
    all_sprites, cars, frog, cars_data = setup_game()
    game_state = TITLE
    running = True
    restart_button = pygame.Rect(WIDTH // 2 - 120, HEIGHT // 2 + 80, 100, 50)
    quit_button = pygame.Rect(WIDTH // 2 + 20, HEIGHT // 2 + 80, 100, 50)
    timer = TIME_LIMIT
    lives = STARTING_LIVES

    while running:
        dt = clock.tick(FPS) / 1000
        game_state, running, cars_data, lives = handle_events(game_state, frog, restart_button, quit_button,
                                                              running, cars, cars_data, lives)
        if game_state == PLAYING and timer > 0:
            game_state, lives = update_game(game_state, all_sprites, frog, cars, dt, timer, lives)
            timer -= dt
        elif game_state == TITLE:
            timer = TIME_LIMIT
            lives = STARTING_LIVES
            all_sprites, cars, frog, cars_data = setup_game()
        elif game_state == WIN:
            timer = TIME_LIMIT
            lives = STARTING_LIVES

        draw_game(screen, game_state, all_sprites, frog, cars, timer, lives)

    pygame.quit()

if __name__ == "__main__":
    main()