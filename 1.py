# Scirros - Jeb Edition - Pygame *INSIDE* Tkinter! (For Windows NT 10... or whatever)
# This is gonna be a GUI sandwich. Buckle up!

import tkinter as tk  # Tkinter, the bread of our GUI sandwich
from tkinter import ttk  # Themed Tkinter widgets. Fancy!
import pygame  # Pygame, the delicious filling!
import random  # For the computer's "brain"
import os  # For system-level magic (embedding Pygame)
import sys  # System stuff, for quitting cleanly

# --- Constants --- #
WIDTH = 600  # Window width. Nice and square-ish.
HEIGHT = 400  # Window height.
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
CHOICES = ["rock", "paper", "scissors"]
FPS = 30  # Frames per second. Gotta keep it smooth.


# --- Game Logic (same as before, but now in a class!) --- #


class ScirrosGame:
    """
    The brains of the Scirros operation! Handles game logic, player/computer choices.
    Now in CLASS form! Very object-oriented. Like a well-organized inventory.
    """

    def __init__(self):
        self.player_choice = None
        self.computer_choice = None
        self.result_text = ""

    def play_round(self, player_choice):
        """Plays a round of Scirros. Updates choices and result_text."""
        self.player_choice = player_choice
        self.computer_choice = random.choice(CHOICES)
        self.result_text = self.determine_winner()

    def determine_winner(self):
        """Figure out who won! Same logic as the CLI version, but now a method."""
        if self.player_choice == self.computer_choice:
            return "It's a tie!"
        elif (
            (self.player_choice == "rock" and self.computer_choice == "scissors")
            or (self.player_choice == "scissors" and self.computer_choice == "paper")
            or (self.player_choice == "paper" and self.computer_choice == "rock")
        ):
            return "You win!"
        else:
            return "Computer wins!"


# --- Pygame Display (embedded in Tkinter) --- #


class PygameDisplay:
    """
    Handles the Pygame part!  Draws animations or whatever inside the Tkinter window.
    """

    def __init__(self, parent, game):
        """Sets up Pygame, creates a canvas inside the Tkinter window."""
        self.parent = parent  # The Tkinter Frame we'll draw into
        self.game = game  # The ScirrosGame instance, to get the results

        # --- Embedding Magic! --- #
        os.environ["SDL_WINDOWID"] = str(
            parent.winfo_id()
        )  # Tell Pygame where to draw!
        if sys.platform == "win32":  # Special handling for Windows
            os.environ["SDL_VIDEODRIVER"] = "windib"
        pygame.init()  # Initialize ALL of Pygame, including the font module
        pygame.display.init()  # Start up the Pygame display
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Make a Pygame screen
        self.screen.fill(WHITE)  # Initial white background
        pygame.display.flip()
        self.clock = pygame.time.Clock()  # Clock for controlling FPS
        self.font = pygame.font.Font(None, 36)  # Initialize font here

    def update(self):
        """Updates and redraws the Pygame display. Called every frame."""
        self.screen.fill(WHITE)  # Clear the screen

        # --- Draw something!  For now, just text results --- #
        if self.game.player_choice:  # Only draw if a choice has been made
            # Player Choice
            player_text = self.font.render(
                f"You: {self.game.player_choice}", True, BLACK
            )
            player_rect = player_text.get_rect(center=(WIDTH // 4, HEIGHT // 2))
            self.screen.blit(player_text, player_rect)
            # Computer Choice
            computer_text = self.font.render(
                f"Computer: {self.game.computer_choice}", True, BLACK
            )
            computer_rect = computer_text.get_rect(center=(WIDTH * 3 // 4, HEIGHT // 2))
            self.screen.blit(computer_text, computer_rect)
            # Result text
            result_text = self.font.render(
                self.game.result_text,
                True,
                GREEN if "You" in self.game.result_text else BLACK,
            )
            result_rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            self.screen.blit(result_text, result_rect)

        pygame.display.flip()  # Update the Pygame display
        self.clock.tick(FPS)  # Maintain FPS


# --- Tkinter GUI --- #


class ScirrosApp:
    """
    The main Tkinter application!  Creates buttons, labels, and the Pygame embed.
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Scirros - Jeb Edition (Tkinter + Pygame!)")
        self.root.geometry(f"{WIDTH}x{HEIGHT}")  # Set window size

        self.game = ScirrosGame()  # Create a game instance

        # --- Tkinter Widgets --- #

        # Frame for buttons (top part)
        self.button_frame = ttk.Frame(root)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)

        self.rock_button = ttk.Button(
            self.button_frame, text="Rock", command=lambda: self.play("rock")
        )
        self.rock_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.paper_button = ttk.Button(
            self.button_frame, text="Paper", command=lambda: self.play("paper")
        )
        self.paper_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.scissors_button = ttk.Button(
            self.button_frame, text="Scissors", command=lambda: self.play("scissors")
        )
        self.scissors_button.pack(side=tk.LEFT, padx=10, pady=10)

        # Frame for the Pygame display (bottom part)
        self.pygame_frame = ttk.Frame(root)
        self.pygame_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        # Create Pygame display *after* creating the frame it goes into
        self.pygame_display = PygameDisplay(self.pygame_frame, self.game)

        # --- Main Loop Setup --- #
        self.root.after(0, self.update)  # Start the update loop

    def play(self, choice):
        """Handles button clicks.  Plays a round of Scirros."""
        self.game.play_round(choice)

    def update(self):
        """Called repeatedly to update the Pygame display within Tkinter."""
        self.pygame_display.update()  # Update the Pygame part
        self.root.after(int(1000 / FPS), self.update)  # Schedule the next update


# --- Run the App! --- #

if __name__ == "__main__":
    root = tk.Tk()
    app = ScirrosApp(root)
    root.mainloop()  # Start the Tkinter main loop!
