import random

# Game settings
grid_size = 5  # Size of the grid (5x5)
num_turns = 10  # Number of turns to catch the rat

# Initialize positions
cat_position = [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)]
rat_position = [random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)]

def print_grid(cat_pos, rat_pos):
    for i in range(grid_size):
        for j in range(grid_size):
            if [i, j] == cat_pos:
                print('C', end=' ')
            elif [i, j] == rat_pos:
                print('R', end=' ')
            else:
                print('.', end=' ')
        print()

def move_position(position, move):
    if move == 'up' and position[0] > 0:
        position[0] -= 1
    elif move == 'down' and position[0] < grid_size - 1:
        position[0] += 1
    elif move == 'left' and position[1] > 0:
        position[1] -= 1
    elif move == 'right' and position[1] < grid_size - 1:
        position[1] += 1

# Game loop
for turn in range(num_turns):
    print(f"Turn {turn + 1}/{num_turns}")
    print_grid(cat_position, rat_position)

    # Get user input
    move = input("Move cat (up, down, left, right): ").strip().lower()
    move_position(cat_position, move)

    # Check if the cat caught the rat
    if cat_position == rat_position:
        print("Congratulations! The cat caught the rat!")
        break

    # Move the rat randomly
    rat_move = random.choice(['up', 'down', 'left', 'right'])
    move_position(rat_position, rat_move)

    # Check if the rat moved out of bounds and correct it
    rat_position[0] = min(max(rat_position[0], 0), grid_size - 1)
    rat_position[1] = min(max(rat_position[1], 0), grid_size - 1)

    if turn == num_turns - 1:
        print("Out of turns! The rat got away.")
    print()

# Final state
print("Final positions:")
print_grid(cat_position, rat_position)
