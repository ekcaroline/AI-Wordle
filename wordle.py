import random
import string

class WordleGame:
    """
    Attributes
    ----------
        solution_word_list : list
            all possible wordle solutions
        guess_word_list : list
            all possible valid guesses
        target_word : list
            wordle answer of the current game
        display_word : list
            current state of the word, showing only letters in their correct positions
        num_guesses : int
            current number of guesses
        max_guesses : int
            max number of guesses 
        guesses : set
            words that have already been guessed

    Methods
    -------
        read_word_list():
            Adds all the words from the CSV file to word_list.
        select_target_word():
            Randomly chooses the current game's wordle answer from word_list.
        check_guess(guess):
            Checks the guess to see if it is the correct word.
        ai_guess():
            During AI's turn, selects a word from the word_list to guess.
    """

    def __init__(self, solution_word_list_file, guess_word_list_file):
        self.solution_word_list = self.read_word_list(solution_word_list_file)
        self.guess_word_list = self.solution_word_list + self.read_word_list(guess_word_list_file)
        self.target_word = list(self.select_target_word())  
        self.display_word = ['*' for _ in self.target_word]  
        self.num_guesses = 0
        self.max_guesses = 6
        self.guesses = set()

        # Attributes only used by AI
            # Keep track of what letters are valid
            # Keep track of invalid letters
            # Keep track of what letters are correct and in the right and wrong position
            # Choose words from the word list that have valid letters in the correct pos and
            # avoid putting valid letters in wrong positions
        self.valid_letters = list(string.ascii_lowercase)
        self.invalid_letters = []
        self.correct_letters_correct_pos = []
        self.correct_letters_wrong_pos = []

    def read_word_list(self, word_list_file):
        """Reads the csv file line by line and adds all the words to the word_list"""
        with open(word_list_file, 'r') as file:
            return [word.strip().replace(",", "").lower() for word in file.readlines()]

    def select_target_word(self):
        """Chooses the wordle word randomly from the word_list"""
        return random.choice(self.solution_word_list)

    def check_guess(self, guess):
        """
        Checks the guess if it's correct.

        If incorrect, it will print what letters were in the correct position
        and print what letters are correct but in the wrong position.
        
        
        """
        if len(guess) != len(self.target_word):
            return False, "Guess length should match the length of the word."
        if guess in self.guesses:
            return False, "You've already guessed that word."
        if guess not in self.guess_word_list:                     
            return False, "That's not a real word!"
        self.num_guesses += 1
        self.guesses.add(guess)

        wrong_pos = []
        temp_target = [] # Holds the rest of letters in the target
        temp_guess = [] # Holds the rest of the letters in the guess

        # Check for any correct letters in the correct positions
        for i, letter in enumerate(guess):
            if letter == self.target_word[i]:
                self.display_word[i] = letter
            else:
                temp_guess.append(letter)
                temp_target.append(self.target_word[i])

        # Check for any correct letters in incorrect positions
        for letter in temp_guess:
            if letter in temp_target:
                wrong_pos.append(letter)
        
        # Print
        if guess == self.target_word:
            return True, "Congratulations! You've guessed the word: {}".format(''.join(self.target_word))
        else:
            if wrong_pos:
                return False, f"Correct letters {' '.join(wrong_pos)}, but not in the right position. The word so far is: {''.join(self.display_word)}"
            else:
                return False, "Incorrect guess. The word so far is: {}".format(''.join(self.display_word))
            

    def ai_guess(self):
        potential_words = []
        
        for word in self.solution_word_list:
            # Check if the word length matches the target word
            if len(word) != len(self.target_word):
                continue
            
            # Flag to check if the word is a potential match
            is_potential_match = True
            
            for i, letter in enumerate(word):
                if letter == self.target_word[i]:
                    continue
                # Check if the letter is correct but in the wrong position
                elif letter in self.target_word:
                    is_potential_match = False
                    break
                # Check if the letter is incorrect
                else:
                    continue
            
            # If the word is a potential match, add it to the list of potential words
            if is_potential_match:
                potential_words.append(word)
        
        # Randomly select a word from the list of potential words
        return random.choice(potential_words) if potential_words else random.choice(self.solution_word_list)


    def display_game_state(self):
        print("Target Word: {}".format(''.join(self.display_word)))
        print("Number of Guesses Left: {}".format(self.max_guesses - self.num_guesses))
        print("Previous Guesses: {}".format(', '.join(self.guesses)))


solution_word_list_file = "./valid_solutions.csv"  # Using Kaggle dataset
guess_word_list_file = "./valid_guesses.csv"
game = WordleGame(solution_word_list_file, guess_word_list_file)

while game.num_guesses < game.max_guesses:
    # Player's turn
    print("Player's turn:")
    player_guess = input().lower()
    is_correct, message = game.check_guess(player_guess)
    print(message)
    if is_correct:
        print("Player wins!")
        break
    
    # AI's turn
    print("==============================\n")
    print("\nAI's turn: Guessing...")
    ai_guess = game.ai_guess()
    print("AI guesses:", ai_guess)
    is_correct, message = game.check_guess(ai_guess)
    print(message)
    if is_correct:
        print("AI wins!")
        break

if not is_correct:
    print("Sorry, both player and AI have run out of guesses. The target word was: {}".format(''.join(game.target_word)))
