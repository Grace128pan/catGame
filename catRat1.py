import pygame
import random

# Initialize Pygame
pygame.init()

# Game settings
GRID_SIZE = 5
CELL_SIZE = 100
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
NUM_TURNS = 10

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

# Initialize positions
cat_position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
rat_position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]

def draw_grid():
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        for y in range(0, WINDOW_SIZE, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

def draw_positions():
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

def main_game():
    global cat_position, rat_position
    running = True
    turn = 0

    cat_position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
    rat_position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]

    while running and turn < NUM_TURNS:
        screen.fill(BLACK)
        draw_grid()
        draw_positions()

        # Draw buttons
        instruction_button = draw_button("Instructions", (20, WINDOW_SIZE + 10), (150, 30))
        stop_button = draw_button("Stop", (200, WINDOW_SIZE + 10), (100, 30))
        restart_button = draw_button("Restart", (330, WINDOW_SIZE + 10), (120, 30))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    move_position(cat_position, 'up')
                elif event.key == pygame.K_DOWN:
                    move_position(cat_position, 'down')
                elif event.key == pygame.K_LEFT:
                    move_position(cat_position, 'left')
                elif event.key == pygame.K_RIGHT:
                    move_position(cat_position, 'right')

                # Check if the cat caught the rat
                if cat_position == rat_position:
                    win_text = font.render("Cat caught the rat! You win!", True, BLACK)
                    screen.fill(WHITE)
                    screen.blit(win_text, (20, WINDOW_SIZE // 2))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    return

                # Move the rat randomly
                rat_move = random.choice(['up', 'down', 'left', 'right'])
                move_position(rat_position, rat_move)

                turn += 1

                if turn >= NUM_TURNS:
                    lose_text = font.render("Out of turns! The rat got away!", True, BLACK)
                    screen.fill(WHITE)
                    screen.blit(lose_text, (20, WINDOW_SIZE // 2))
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if instruction_button.collidepoint(mouse_pos):
                    show_instructions()
                elif stop_button.collidepoint(mouse_pos):
                    running = False
                elif restart_button.collidepoint(mouse_pos):
                    main_game()
                    return

    pygame.quit()

main_game()
