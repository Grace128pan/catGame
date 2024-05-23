import pygame
import random

# Initialize Pygame
pygame.init()

# Game settings
GRID_SIZE = 5
CELL_SIZE = 100
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
#NUM_TURNS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 0, 255)
BUTTON_HOVER_COLOR = (0, 100, 255)

# Set up display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 50))
pygame.display.set_caption("Cat Catching Rat Game")

# Fonts
font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 28)

# Load images
cat_image = pygame.image.load('image/jumpingCat.jpg')
cat_image = pygame.transform.scale(cat_image, (CELL_SIZE, CELL_SIZE))
rat_image = pygame.image.load('image/rat.jpg')
rat_image = pygame.transform.scale(rat_image, (CELL_SIZE, CELL_SIZE))

def draw_grid():
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        for y in range(0, WINDOW_SIZE, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

def draw_positions(cat_position, rat_position):
    cat_rect = pygame.Rect(cat_position[1] * CELL_SIZE, cat_position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    rat_rect = pygame.Rect(rat_position[1] * CELL_SIZE, rat_position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    screen.blit(cat_image, cat_rect)
    screen.blit(rat_image, rat_rect)

def move_position(position, move):
    if move == 'up' and position[0] > 0:
        position[0] -= 1
    elif move == 'down' and position[0] < GRID_SIZE - 1:
        position[0] += 1
    elif move == 'left' and position[1] > 0:
        position[1] -= 1
    elif move == 'right' and position[1] < GRID_SIZE - 1:
        position[1] += 1

def draw_button(text, position, size, hover=False):
    color = BUTTON_HOVER_COLOR if hover else BUTTON_COLOR
    rect = pygame.Rect(position, size)
    pygame.draw.rect(screen, color, rect)
    text_surf = button_font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)
    return rect

def show_instructions():
    screen.fill(WHITE)
    instructions = [
        "Instructions:",
        "1. Use arrow keys to move the cat.",
        "2. Catch the rat within 10 turns.",
        "3. The rat moves randomly after each turn.",
        "4. Press 'Stop' to exit the game.",
        "5. Press 'Restart' to start a new game."
    ]
    y_offset = 50
    for line in instructions:
        text_surf = font.render(line, True, BLACK)
        screen.blit(text_surf, (20, y_offset))
        y_offset += 40
    pygame.display.flip()
    pygame.time.wait(5000)
