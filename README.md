# Wordle Battle
wordle.py is an executable Python/Python3 script that launches a PvP Wordle game where the user competes against an AI to guess the target word in a total of 6 tries. Whoever guesses the word first wins!

## Notes
The wordle.py file defines a class called WordleGame and has functions to operate the game and process the AI's guesses using the First-Choice Hill Climbing algorithm. Outside of the class, an instance of WordleGame is initialized and while there are still turns available, the user and AI will be prompted to make their guesses. If neither guess the word in the end, the game ends in a draw.

## Usage
To execute this file, please ensure Python/Python3 is installed on your device and run the following in the terminal: `python3 ./wordle.py`
