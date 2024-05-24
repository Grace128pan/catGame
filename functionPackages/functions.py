import pygame
import random

# Game settings
GRID_SIZE = 5
CELL_SIZE = 100
WINDOW_SIZE = GRID_SIZE * CELL_SIZE
NUM_TURNS = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (15, 164, 175)  # Hex: #0FA4AF
BUTTON_HOVER_COLOR = (10, 120, 128)

# Set up display
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 50))
pygame.display.set_caption("Cat Catching Rat Game")

# Fonts
pygame.font.init()
font = pygame.font.Font(None, 36)
button_font = pygame.font.Font(None, 24)
instructions_font = pygame.font.SysFont("timesnewroman", 24)


# Load images
cat_images = {
    0: pygame.image.load('image/jumpingCat.jpg'),
    1: pygame.image.load('image/dollar.jpg'),
    2: pygame.image.load('image/flower.png'),
    3: pygame.image.load('image/lucky.jpg'),
    4: pygame.image.load('image/niu.jpg'),
    5: pygame.image.load('image/sunny.jpeg')
}

for key in cat_images:
    cat_images[key] = pygame.transform.scale(cat_images[key], (CELL_SIZE, CELL_SIZE))

current_cat_image = cat_images[0]
rat_image = pygame.image.load('image/rat.jpg')
rat_image = pygame.transform.scale(rat_image, (CELL_SIZE, CELL_SIZE))
award_image = pygame.image.load('image/award.jpg')
award_image = pygame.transform.scale(award_image, (CELL_SIZE, CELL_SIZE))

# Load sounds
pygame.mixer.init()
background_music = pygame.mixer.Sound("audio/background.mp3")
win_sound = pygame.mixer.Sound("audio/win.mp3")
lose_sound = pygame.mixer.Sound("audio/lose.mp3")

# Initialize positions
cat_position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
rat_position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]

# Check if cat_position is the same as rat_position, and regenerate rat_position if needed
while cat_position == rat_position:
    rat_position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]

# Initialize game state
paused = False

def draw_grid():
    for x in range(0, WINDOW_SIZE, CELL_SIZE):
        for y in range(0, WINDOW_SIZE, CELL_SIZE):
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 1)

def draw_positions():
    cat_rect = pygame.Rect(cat_position[1] * CELL_SIZE, cat_position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    rat_rect = pygame.Rect(rat_position[1] * CELL_SIZE, rat_position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    screen.blit(current_cat_image, cat_rect)
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
    pygame.draw.rect(screen, color, rect, border_radius=10)
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
        "4. Press 'Try Again' to restart the game.",
        "5. Press 'Pause' to pause the game.",
        "6. Press 'Continue' to continue the paused game.",
        "7. Press 'Exit' to stop the game."
    ]
    y_offset = 20
    for line in instructions:
        text_surf = instructions_font.render(line, True, BLACK)
        screen.blit(text_surf, (20, y_offset))
        y_offset += 30
    pygame.display.flip()
    pygame.time.wait(5000)

def play_background_music():
    background_music.play(-1)

def get_user_cat_choice():
    screen.fill(WHITE)
    choice_text = font.render("Choose a cat image:", True, BLACK)
    screen.blit(choice_text, (20, 20))
    options = [
        "0: Default",
        "1: Dollar",
        "2: Flower",
        "3: Lucky",
        "4: Niu",
        "5: Sunny"
    ]
    y_offset = 70
    for option in options:
        option_text = font.render(option, True, BLACK)
        screen.blit(option_text, (20, y_offset))
        y_offset += 40
    pygame.display.flip()

    user_choice = None
    while user_choice is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5):
                    user_choice = int(event.unicode)
                    return user_choice

def end_game(message, win=False):
    background_music.stop()
    screen.fill(WHITE)
    end_text = font.render(message, True, BLACK)
    screen.blit(end_text, (20, WINDOW_SIZE // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    if win:
        throw_flowers()
        choice = get_user_cat_choice()
        if choice is not None:
            global current_cat_image
            current_cat_image = cat_images[choice]
            return True
    else:
        if draw_end_buttons():
            return True
        else:
            return False

def throw_flowers():
    for _ in range(20):
        x = random.randint(0, WINDOW_SIZE - CELL_SIZE)
        y = random.randint(0, WINDOW_SIZE - CELL_SIZE)
        screen.blit(award_image, (x, y))
        pygame.display.flip()
        pygame.time.wait(500)

def draw_end_buttons():
    running = True
    while running:
        screen.fill(WHITE)
        end_text = font.render("Game Over!", True, BLACK)
        screen.blit(end_text, (WINDOW_SIZE // 2 - 80, WINDOW_SIZE // 2- 40))
        try_again_button = draw_button("Try Again", (100, WINDOW_SIZE // 2 + 20), (150, 40))
        exit_button = draw_button("Exit", (300, WINDOW_SIZE // 2 + 20), (100, 40))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if try_again_button.collidepoint(mouse_pos):
                    return True
                elif exit_button.collidepoint(mouse_pos):
                    return False

def handle_mouse_buttons(event):
    global paused
    mouse_pos = event.pos
    if instruction_button.collidepoint(mouse_pos):
        show_instructions()
    elif pause_button.collidepoint(mouse_pos):
        paused = True
        background_music.stop()
    elif continue_button.collidepoint(mouse_pos):
        paused = False
        play_background_music()
    elif exit_button.collidepoint(mouse_pos):
        pygame.quit()
        exit()

def main_game():
    global cat_position, rat_position, paused, instruction_button, pause_button, continue_button, exit_button
    running = True
    turn = 0
    cat_position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
    rat_position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]

    play_background_music()

    while running and turn < NUM_TURNS:
        if not paused:
            screen.fill(BLACK)
            draw_grid()
            draw_positions()

            # Draw buttons
            instruction_button = draw_button("Instructions", (20, WINDOW_SIZE + 10), (150, 30))
            button_spacing = 10
            pause_button = draw_button("Pause", (WINDOW_SIZE - 270, WINDOW_SIZE + 10), (80, 30))
            continue_button = draw_button("Continue", (WINDOW_SIZE - 180 + button_spacing, WINDOW_SIZE + 10), (90, 30))
            exit_button = draw_button("Exit", (WINDOW_SIZE - 90 + 2 * button_spacing, WINDOW_SIZE + 10), (80, 30))

            pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not paused:
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
                    win_sound.play()
                    if end_game("Cat caught the rat! You win!", win=True):
                        return main_game()

                # Move the rat randomly
                possible_moves = ['up', 'down', 'left', 'right']
                if abs(cat_position[0] - rat_position[0]) + abs(cat_position[1] - rat_position[1]) > 1:
                    if cat_position[0] > rat_position[0]:
                        possible_moves.remove('up')
                    if cat_position[0] < rat_position[0]:
                        possible_moves.remove('down')
                    if cat_position[1] > rat_position[1]:
                        possible_moves.remove('left')
                    if cat_position[1] < rat_position[1]:
                        possible_moves.remove('right')
                rat_move = random.choice(possible_moves)
                move_position(rat_position, rat_move)

                turn += 1

                if turn >= NUM_TURNS:
                    lose_sound.play()
                    if end_game("Out of turns! The rat got away!", win=False):
                        return main_game()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_buttons(event)

    pygame.quit()


