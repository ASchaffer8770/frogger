import pygame

class Frog(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.base_size = 30  # Base size of the frog
        self.image = pygame.Surface((self.base_size, self.base_size), pygame.SRCALPHA)  # Transparent background
        self.draw_frog(1.0)  # Initial draw with no scaling
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height - 50)
        self.base_y = self.rect.y
        self.hop_timer = 0
        self.hop_duration = 0.2
        self.hop_height = 20
        self.max_scale = 1.3  # Max size during hop (30% larger)

    def draw_frog(self, scale):
        """Draw the frog with scaling and eyes"""
        scaled_size = int(self.base_size * scale)
        self.image = pygame.Surface((scaled_size, scaled_size), pygame.SRCALPHA)
        # Draw body
        pygame.draw.ellipse(self.image, "green", (0, 0, scaled_size, scaled_size))
        # Draw eyes
        eye_size = int(scaled_size * 0.2)  # Eyes are 20% of frog size
        eye_offset = int(scaled_size * 0.25)  # Position eyes near top
        pygame.draw.circle(self.image, "white", (eye_offset, eye_offset), eye_size)  # Left eye
        pygame.draw.circle(self.image, "white", (scaled_size - eye_offset, eye_offset), eye_size)  # Right eye
        pygame.draw.circle(self.image, "black", (eye_offset, eye_offset), eye_size // 2)  # Left pupil
        pygame.draw.circle(self.image, "black", (scaled_size - eye_offset, eye_offset), eye_size // 2)  # Right pupil

    def update(self, dt):
        """Update frog position and size during hop"""
        if self.hop_timer > 0:
            progress = 1 - (self.hop_timer / self.hop_duration)
            # Parabolic hop offset
            hop_offset = self.hop_height * 4 * progress * (1 - progress)
            self.rect.y = self.base_y - hop_offset
            # Scale frog: grow to max_scale at peak (progress = 0.5), shrink back
            scale = 1.0 + (self.max_scale - 1.0) * 4 * progress * (1 - progress)
            # Redraw frog with new scale
            old_center = self.rect.center
            self.draw_frog(scale)
            self.rect = self.image.get_rect()
            self.rect.center = old_center
            # Update timer
            self.hop_timer -= dt
            if self.hop_timer <= 0:
                self.rect.y = self.base_y
                self.hop_timer = 0
                self.draw_frog(1.0)  # Reset to base size
                self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, dx, dy):
        """Move frog and trigger hop animation"""
        self.rect.x += dx
        self.base_y += dy
        self.rect.y = self.base_y
        self.hop_timer = self.hop_duration

    def reset(self, width, height):
        """Reset frog position and size"""
        self.rect.center = (width // 2, height - 50)
        self.base_y = self.rect.y
        self.hop_timer = 0
        self.draw_frog(1.0)  # Reset to base size
        self.rect = self.image.get_rect(center=self.rect.center)

class Car(pygame.sprite.Sprite):
    def __init__(self, color, size, x, y, speed):
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def update(self, dt, screen_width):
        self.rect.x += self.speed * dt
        if self.speed > 0 and self.rect.left > screen_width:
            self.rect.right = 0
        elif self.speed < 0 and self.rect.right < 0:
            self.rect.left = screen_width

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y

def create_text(font, text, color, x, y):
    surface = font.render(text, True, color)
    rect = surface.get_rect(center=(x, y))
    return surface, rect

def draw_dialog(screen, rect, fill_color, border_color):
    pygame.draw.rect(screen, fill_color, rect)
    pygame.draw.rect(screen, border_color, rect, 5)

def draw_dashed_line(screen, y, width):
    for x in range(0, width, 20):
        pygame.draw.line(screen, "white", (x, y), (x + 10, y), 2)