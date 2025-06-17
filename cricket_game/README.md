
# Cricket Batting Game

This is a simple cricket batting game created using Python and the Pygame library. The game allows the player to simulate a short cricket match by timing their hits to score runs. The goal is to chase down a randomly generated target score within a limited number of balls.

# How the Game Works

- The player controls a batsman placed on the screen.
- A ball is bowled automatically from the top of the screen toward the batsman.
- When the player presses the spacebar, the batsman swings the bat and attempts to hit the ball.
- The timing of the hit determines how far the ball travels and how many runs are scored.
- The player has six balls to chase a randomly set target.
- If the player reaches or exceeds the target within the allotted balls, they win.

# Key Features

- Background image of a cricket stadium for visual appeal.
- Batsman sprite to replace simple rectangles and make the game feel more realistic.
- Ball physics with basic arc simulation when hit.
- Sound effects when the ball is hit to increase immersion.
- On-screen scoreboard showing the current score, target, balls remaining, and game result.
- Basic animation and game loop control.
- Randomized target score for replay value.


# Requirements

Make sure you have Python installed. You will also need to install the `pygame` library.

To install Pygame, run:

python3 -m pip install pygame

# Running the Game

Navigate to the project folder in your terminal, then run:

python3 main.py

Make sure all image and sound files (such as `batsman.png`, `stadium.webp`, and `hit.mp3`) are located in the same folder as `main.py`.

# Project Files

- `main.py` – Contains all the source code for the game.
- `batsman.png` – Sprite image of the batsman.
- `stadium.webp` – Background image of the cricket stadium.
- `hit.mp3` – Sound effect for hitting the ball.
- `requirements.txt` – Python packages required to run the project.
- `resource.txt` – Log of prompts and AI responses used to develop the game.
- `README.md` – This file.
- `cheer.mp3` – Sound effect for cheering

