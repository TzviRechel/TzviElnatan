import random
import time
import os

def matrix_effect(columns=80, speed=0.05, density=0.1):
    """
    Create a simple Matrix-style falling text effect.

    :param columns: Number of columns (width of the screen).
    :param speed: Delay between each frame (lower is faster).
    :param density: Probability of a column generating a new character.
    """
    # Initialize a list to store positions of characters for each column
    positions = [0] * columns

    try:
        while True:
            # Clear the screen
            os.system('cls' if os.name == 'nt' else 'clear')

            # Create the Matrix effect row by row
            for i in range(columns):
                # Randomly decide if the column should generate a character
                if random.random() < density:
                    positions[i] = random.randint(1, 25)  # Length of falling text

                # Decrease the position of the text (simulate falling)
                if positions[i] > 0:
                    print(chr(random.randint(33, 126)), end="")  # Random ASCII characters
                    positions[i] -= 1
                else:
                    print(" ", end="")

            print()  # Move to the next row
            time.sleep(speed)
    except KeyboardInterrupt:
        print("\nMatrix effect terminated.")

# Run the Matrix effect
if __name__ == "__main__":
    matrix_effect(columns=80, speed=0.05, density=0.2)
