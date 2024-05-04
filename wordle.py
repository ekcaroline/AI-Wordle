import random

class WordleGame:
    def __init__(self, word_list_file):
        self.word_list = self.read_word_list(word_list_file)
        self.target_word = list(self.select_target_word())  
        self.display_word = ['*' for _ in self.target_word]  
        self.num_guesses = 0
        self.max_guesses = 6
        self.guesses = set()

    def read_word_list(self, word_list_file):
        with open(word_list_file, 'r') as file:
            return [word.strip().lower() for word in file.readlines()]

    def select_target_word(self):
        return random.choice(self.word_list)

    def check_guess(self, guess):
        if len(guess) != len(self.target_word):
            return False, "Guess length should match the length of the word."
        if guess in self.guesses:
            return False, "You've already guessed that word."
        self.num_guesses += 1
        self.guesses.add(guess)
        
        correct_letters = set()
        
        # Check if the guessed letter is in the target word
        for i, letter in enumerate(self.target_word):
            if guess[i] == letter:
                self.display_word[i] = letter  
                correct_letters.add(letter)
        
        if self.display_word == self.target_word:
            return True, "Congratulations! You've guessed the word: {}".format(''.join(self.target_word))
        else:
            if correct_letters:
                return False, "Correct letters, but not in the right position. The word so far is: {}".format(''.join(self.display_word))
            else:
                return False, "Incorrect guess. The word so far is: {}".format(''.join(self.display_word))

    def ai_guess(self):
        potential_words = []
        
        for word in self.word_list:
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
        return random.choice(potential_words) if potential_words else random.choice(self.word_list)


    def display_game_state(self):
        print("Target Word: {}".format(''.join(self.display_word)))
        print("Number of Guesses Left: {}".format(self.max_guesses - self.num_guesses))
        print("Previous Guesses: {}".format(', '.join(self.guesses)))


word_list_file = ""  # Using Kaggle dataset
game = WordleGame(word_list_file)

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
