#!/usr/bin/env python3
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
        # self.target_word = "CROSS"
        self.display_word = ['*' for _ in self.target_word]  
        self.num_guesses = 0
        self.max_guesses = 6
        self.guesses = set()

        # Attributes only used by AI
        self.valid_letters = set(list(string.ascii_uppercase))
        self.correct_letters_wrong_pos = {}
        self.potential_words = self.solution_word_list

    def read_word_list(self, word_list_file):
        """Reads the csv file line by line and adds all the words to the word_list"""
        with open(word_list_file, 'r') as file:
            return [word.strip().replace(",", "").upper() for word in file.readlines() if len(word.strip().replace(",", "")) == 5]

    def select_target_word(self):
        """Chooses the wordle word randomly from the word_list"""
        return random.choice(self.solution_word_list)

    def check_guess(self, guess):
        """
        Checks the guess if it's correct.

        If incorrect, it will print what letters were in the correct position
        and print what letters are correct but in the wrong position.

        Updates what letters are invalid.

        TO DO: Update what letters are correct but in the wrong position
        
        """
        # print("Guess:", guess)
        # print("Target word:", self.target_word)
        if len(guess) != len(self.target_word):
            return False, "Guess length should match the length of the word."
        if guess in self.guesses:
            return False, "You've already guessed that word."
        if guess not in self.guess_word_list:                     
            return False, "That's not a real word!"
        self.num_guesses += 1
        self.guesses.add(guess)
        
        wrong_pos = []
        temp_target = [] # Holds the rest of letters in the target after removing letters in the correct pos
        temp_guess = [] # Holds the rest of the letters in the guess after removing letters in the correct pos
        correct_word = True

        # Check for any correct letters in the correct positions
        # If any letters are incorrect, change correct_word to false
        for i, letter in enumerate(guess):
            if letter == self.target_word[i]:
                self.display_word[i] = letter
                temp_guess.append('*')
            else:
                temp_guess.append(letter)
                temp_target.append(self.target_word[i])
                correct_word = False

        # Return True if guess is the correct word
        if correct_word == True:
            return True, "Congratulations! The word is: {}".format(''.join(self.target_word))
        
        # Check for any correct letters in incorrect positions
        for i, letter in enumerate(temp_guess):
            if letter != "*":
                if letter in temp_target:
                    wrong_pos.append(letter)
                    # Save the letter and its incorrect position
                    if letter in self.correct_letters_wrong_pos:
                        self.correct_letters_wrong_pos[letter].add(i)
                    else:
                        self.correct_letters_wrong_pos[letter] = {i}
                else:
                    print("Invalid letters:", letter)
                    self.valid_letters.discard(letter) # For AI

        # For scenarios where double letters appear in the guess but only exist once in the target
        # Add the removed letters back into the valid letters set
        for letters in self.display_word:
            if letters != "*":
                self.valid_letters.add(letters) 

        print(self.correct_letters_wrong_pos)
        if wrong_pos:
            return False, f"Correct letters {' '.join(set(wrong_pos))}, but not in the right position. The word so far is: {''.join(self.display_word)}"
        else:
            return False, "Incorrect guess. The word so far is: {}".format(''.join(self.display_word))
            

    def ai_guess(self):
        """
            TO DO: 
            - AI should avoid using words that use invalid letters
            - Avoid using valid letters in incorrect positions
            - Iterate through all words in the solution word list and filter out words that do not meet the criteria
            - If there are multiple possible words, choose ones that do not repeat as many letters

        """

        # Filter out words containing invalid letters
        filter1 = [word for word in self.potential_words if all(letter in self.valid_letters for letter in word)]
        # print('Filter1:', filter1)

        # Filter out words that have already been guessed
        filter2 = [word for word in filter1 if word not in self.guesses]
        # print('Filter2:', filter2)

        # Filter out words that don't contain all possible letters
        filter3 = [word for word in filter2 if all(key in word for key in self.correct_letters_wrong_pos.keys())]
        # print('Filter3:', filter3)

        # Filter out words that don't contain the characters in the display word
        filter4 = []
        for word in filter3:
            include_word = True
            for i, letter in enumerate(self.display_word):
                if letter != '*':
                    if letter != word[i]:
                        include_word = False
                        break
            if include_word:
                filter4.append(word)
        # print('Filter4:', filter4)

        # Filter out words repeating letters in incorrect positions
        filter5 = []
        if filter4:
            for word in filter4:
                include_word = True
                for letter, positions in self.correct_letters_wrong_pos.items():
                    if letter in word and any(pos == i for pos in positions): # If the letter in the set is in the word
                        # If the index where the letter is matches any number in the set, set include to false
                        if word.index(letter) in positions:
                            include_word = False
                            break
                if include_word:
                    filter5.append(word)
        else: 
            filter5 = filter4
        self.potential_words = filter5
        print('Filter5:', filter5)

        # Choose words with fewer repeating letters
        if filter5:
            # print(filter5)
            word_counts = {word: sum(word.count(letter) for letter in self.valid_letters) for word in filter5}
            min_count = min(word_counts.values())
            best_words = [word for word, count in word_counts.items() if count == min_count]

            # Remove words that have already been guessed
            best_words = [word for word in best_words if word not in self.guesses]

            return random.choice(best_words)
        else:
            return random.choice(self.potential_words)



    def display_game_state(self):
        print("Target Word: {}".format(''.join(self.display_word)))
        print("Number of Guesses Left: {}".format(self.max_guesses - self.num_guesses))
        print("Previous Guesses: {}".format(', '.join(self.guesses)))


solution_word_list_file = "./valid_solutions.csv"  # Using Kaggle dataset
guess_word_list_file = "./valid_guesses.csv"
game = WordleGame(solution_word_list_file, guess_word_list_file)

while game.num_guesses < game.max_guesses:
    print("==============================\n")
    # Player's turn
    print(game.target_word)
    player_guess = input("Player's turn: ").upper()
    is_correct, message = game.check_guess(player_guess)
    print(message)
    if is_correct:
        print("Player wins!")
        break
    
    # AI's turn
    print("\nAI's turn: Guessing...")
    ai_guess = game.ai_guess()
    print("AI guesses:", ai_guess)
    is_correct, message = game.check_guess(ai_guess)
    print(message)
    if is_correct:
        print("AI wins!")
        break
    print("\n")

if not is_correct:
    print("Sorry, both player and AI have run out of guesses. The target word was: {}".format(''.join(game.target_word)))
