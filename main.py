from functionalities.utility import (
    pygame, screen, font, draw_grid, draw_positions, 
    move_position, draw_button, show_instructions, 
    WINDOW_SIZE, CELL_SIZE, GRID_SIZE, WHITE, BLACK, random, cat_image, rat_image
)

NUM_TURNS = 10

def main_game():
    global cat_position, rat_position
    running = True
    turn = 0

    cat_position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
    rat_position = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]

    while running and turn < NUM_TURNS:
        screen.fill(BLACK)
        draw_grid()
        draw_positions(cat_position, rat_position)

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

if __name__ == "__main__":
    main_game()
