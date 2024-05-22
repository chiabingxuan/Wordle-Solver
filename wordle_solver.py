import pickle
import random
from termcolor import colored


class Guesser(object):
    def __init__(self, guesses_data, target_word, word_length=5):
        self.word_length = word_length
        self.valid_guesses_data = guesses_data
        self.target_word = target_word
        self.letters = dict()
        for char in self.target_word:
            if char not in self.letters:
                self.letters[char] = 0
            self.letters[char] += 1

    def get_guess_result(self, word_guessed):
        if word_guessed not in self.valid_guesses_data:
            return None
        result = [("", -1) for i in range(self.word_length)]
        correct_guesses = 0
        remaining_letters_count = self.letters.copy()
        for position in range(self.word_length):
            letter_in_word_guessed = word_guessed[position]
            if letter_in_word_guessed not in remaining_letters_count:
                result[position] = (letter_in_word_guessed, 0)
            elif letter_in_word_guessed == self.target_word[position]:
                result[position] = (letter_in_word_guessed, 2)
                remaining_letters_count[letter_in_word_guessed] -= 1
                correct_guesses += 1
        for position in range(self.word_length):
            if result[position] == ("", -1):
                letter_in_word_guessed = word_guessed[position]
                if remaining_letters_count[letter_in_word_guessed] > 0:
                    result[position] = (letter_in_word_guessed, 1)
                    remaining_letters_count[letter_in_word_guessed] -= 1
                else:
                    result[position] = (letter_in_word_guessed, 0)
        return result, correct_guesses


class WordleGame(Guesser):
    def __init__(self, solution_data, guesses_data, num_tries=6):
        super().__init__(guesses_data, random.choice(list(solution_data)))
        self.tries_initial = num_tries
        self.tries_left = num_tries

    def print_result(self, result):
        colours = {0: "white", 1: "yellow", 2: "green"}
        for pair in result:
            letter, outcome = pair
            print(colored(letter.upper(), colours[outcome]), end="")
        print()

    def single_round(self, robot_guess=None, hide_text=False):
        if robot_guess:
            word_guessed = robot_guess
            if not hide_text:
                print(
                    f"Attempt #{self.tries_initial - self.tries_left + 1} of {self.tries_initial}: Robot guessed the word {word_guessed.upper()}")
            result = self.get_guess_result(word_guessed)
        else:
            word_guessed = input(
                f"Guess a word (Attempt #{self.tries_initial - self.tries_left + 1} of {self.tries_initial}): ").lower()
            result = self.get_guess_result(word_guessed)
            while result is None:
                print("Invalid word!")
                word_guessed = input(
                    f"Guess a word (Attempt #{self.tries_initial - self.tries_left + 1} of {self.tries_initial}): ").lower()
                result = self.get_guess_result(word_guessed)
        result_array, correct_guesses = result
        if not hide_text:
            print("Result of guess:")
            self.print_result(result_array)
            print()
        self.tries_left -= 1
        return result_array, correct_guesses

    def play(self):
        print("You have started a new Wordle game:")
        print("-----------------------------------")
        while self.tries_left > 0:
            result_array, correct_guesses = self.single_round()
            if correct_guesses == self.word_length:
                num_attempts = self.tries_initial - self.tries_left
                print(f"Congratulations, you win! You took {num_attempts} attempt(s) to guess the word!\n")
                return
        print(f"Sorry, you lose! The word was {self.target_word.upper()}.\n")


class WordleSolver(object):
    def __init__(self, solution_data, guesses_data, epsilon, num_tries=6):
        self.game = None
        self.possible_words = None
        self.possible_solutions_word_data = solution_data
        self.valid_guesses_data = guesses_data
        self.num_tries = num_tries
        self.cancelling_power = {num_attempts: {word: [float(0), 0] for word in self.possible_solutions_word_data} for num_attempts in range(1, self.num_tries + 1)}
        self.epsilon = epsilon

    def check_possible_word(self, guess_result, word_checked):
        green_letters = dict()
        yellow_letters = dict()
        grey_letters = dict()
        green_positions = set()
        yellow_letters_possible_positions = dict()
        word_checked_letters = dict()
        for position, pair in enumerate(guess_result):
            letter, outcome = pair
            if outcome == 2:
                if word_checked[position] != letter:
                    return False
                if letter not in green_letters:
                    green_letters[letter] = set()
                green_letters[letter].add(position)
                green_positions.add(position)
            elif outcome == 1:
                if letter not in yellow_letters:
                    yellow_letters[letter] = set()
                yellow_letters[letter].add(position)
            else:
                if letter not in grey_letters:
                    grey_letters[letter] = set()
                grey_letters[letter].add(position)
        for yellow_letter, positions in yellow_letters.items():
            wrong_positions_for_yellow_letter = green_positions.union(positions)
            if yellow_letter in grey_letters:
                wrong_positions_for_yellow_letter = wrong_positions_for_yellow_letter.union(grey_letters[yellow_letter])
            valid_positions_for_yellow_letter = set(range(self.game.word_length)).difference(wrong_positions_for_yellow_letter)
            yellow_letters_possible_positions[yellow_letter] = valid_positions_for_yellow_letter
        for position, char in enumerate(word_checked):
            if position not in green_positions:
                if char not in word_checked_letters:
                    word_checked_letters[char] = set()
                word_checked_letters[char].add(position)
        filled_positions = green_positions.copy()
        for position, pair in enumerate(guess_result):
            letter, outcome = pair
            if outcome == 1:
                if letter not in word_checked_letters or not word_checked_letters[letter]:
                    return False
                possible_positions = yellow_letters_possible_positions[letter]
                word_checked_letter_position = word_checked_letters[letter].pop()
                if word_checked_letter_position not in possible_positions:
                    return False
                filled_positions.add(word_checked_letter_position)
        for position, char in enumerate(word_checked):
            if position not in filled_positions:
                if char in grey_letters:
                    return False
                if char in yellow_letters:
                    if position not in yellow_letters_possible_positions[char]:
                        return False
        return True

    def choose_best_word(self, testing_mode, num_attempts, show_top_few=False):
        if testing_mode:
            if not show_top_few:
                return sorted(list(self.possible_words), key=lambda word: self.cancelling_power[num_attempts][word][0], reverse=True)[0]
            return sorted(list(self.possible_words), key=lambda word: self.cancelling_power[num_attempts][word][0], reverse=True)
        choices = [sorted(list(self.possible_words), key=lambda word: self.cancelling_power[num_attempts][word][0], reverse=True)[0], random.choice(list(self.possible_words))]
        return random.choices(choices, weights=[1 - self.epsilon, self.epsilon], k=1)[0]

    def simulate(self, hide_text=False, testing_mode=True):
        if not hide_text:
            print("Robot has started playing a simulated game:")
            print("-------------------------------------------")
        self.game = WordleGame(self.possible_solutions_word_data, self.valid_guesses_data, self.num_tries)
        self.possible_words = self.possible_solutions_word_data
        while self.game.tries_left > 0:
            num_attempts = self.game.tries_initial - self.game.tries_left + 1
            best_word = self.choose_best_word(testing_mode, num_attempts)
            result_array, correct_guesses = self.game.single_round(best_word, hide_text=hide_text)
            if correct_guesses == self.game.word_length:
                if not hide_text:
                    print(f"The robot won! It took {num_attempts} attempt(s) to guess the word {best_word.upper()}!\n")
                self.game = None
                self.possible_words = None
                return num_attempts
            remaining_words = set()
            initial_count = 0
            remaining_count = 0
            for possible_word in self.possible_words:
                if self.check_possible_word(result_array, possible_word):
                    remaining_words.add(possible_word)
                    remaining_count += 1
                initial_count += 1
            if not testing_mode:
                proportion_cancelled = 1 - (remaining_count / initial_count)
                avg_cancelling_power, times_guessed = self.cancelling_power[num_attempts][best_word][0], self.cancelling_power[num_attempts][best_word][1]
                if times_guessed == 0:
                    self.cancelling_power[num_attempts][best_word][0] = proportion_cancelled
                    self.cancelling_power[num_attempts][best_word][1] = 1
                else:
                    self.cancelling_power[num_attempts][best_word][0] = (avg_cancelling_power * times_guessed + proportion_cancelled) / (times_guessed + 1)
                    self.cancelling_power[num_attempts][best_word][1] += 1
            self.possible_words = remaining_words
            if not hide_text:
                print(f"Robot has narrowed the possible words down to the following: {self.possible_words}\n")
        if not hide_text:
            print(f"The robot lost! The word was {self.game.target_word.upper()}.\n")
        self.game = None
        self.possible_words = None
        return None

    def train(self, num_trainings, testing_mode=False):
        results = dict()
        for count in range(1, self.num_tries + 1):
            results[count] = 0
        results[None] = 0
        for count in range(num_trainings):
            result = self.simulate(hide_text=True, testing_mode=testing_mode)
            results[result] += 1
            if testing_mode:
                print(f"Completed test game #{count + 1}")
            else:
                print(f"Completed training game #{count + 1}")
        return results

    def test(self, num_trials):
        results = self.train(num_trials, testing_mode=True)
        success_rate = (1 - (results[None] / num_trials)) * 100
        average_num_attempts = 0
        results_strings = dict()
        for result, count in results.items():
            if result is not None:
                results_strings[str(result)] = str(count)
                average_num_attempts += result * count
            else:
                results_strings["failed"] = str(count)
        average_num_attempts /= (num_trials - results[None])
        results_strings["success_rate"] = str(success_rate)
        results_strings["average_number_of_attempts"] = str(average_num_attempts)
        results_strings["epsilon"] = str(self.epsilon)
        return results_strings

    def print_cancelling_powers(self):
        words = list(self.cancelling_power[1].keys())
        for turn in range(1, self.num_tries + 1):
            print(f"For attempt {turn}: ")
            sorted_words = sorted(words, key=lambda word: self.cancelling_power[turn][word][0], reverse=True)
            for word in sorted_words:
                print(f"{word.upper()} (Score: {self.cancelling_power[turn][word][0]}, Number of trials: {self.cancelling_power[turn][word][1]})")
            print()

    def check_valid_guess_input(self, guess_input):
        if len(guess_input) != self.game.word_length:
            return False
        for char in guess_input:
            if char not in ["0", "1", "2"]:
                return False
        return True

    def solve(self, num_top_few_guesses_shown=5):
        print("Robot shall now try to play a Wordle game for you:")
        print("---------------------------------------------------")
        self.game = WordleGame(self.possible_solutions_word_data, self.valid_guesses_data, self.num_tries)
        self.possible_words = self.possible_solutions_word_data
        tries_left = self.num_tries
        while tries_left > 0:
            num_attempts = self.num_tries - tries_left + 1
            best_words = self.choose_best_word(testing_mode=True, num_attempts=num_attempts, show_top_few=True)
            best_word = best_words[0]
            print(f"Attempt #{num_attempts} of {self.num_tries}: Here are the best guesses, according to the robot (scores range from 0 to 1):")
            for count in range(min(num_top_few_guesses_shown, len(best_words))):
                top_word = best_words[count]
                print(f"{top_word.upper()} (Score: {self.cancelling_power[num_attempts][top_word][0]})")
            print(f"Robot suggests that you guess the word {best_word.upper()}")
            guess_input = input(f"Enter the result after guessing {best_word.upper()} (Green = 2, Yellow = 1, Grey = 0): ")
            while not self.check_valid_guess_input(guess_input):
                print("Invalid result!")
                guess_input = input(
                    f"Enter the result after guessing {best_word.upper()} (Green = 2, Yellow = 1, Grey = 0): ")
            correct_guesses = 0
            for digit in guess_input:
                if int(digit) == 2:
                    correct_guesses += 1
            if correct_guesses == self.game.word_length:
                print(f"\nCongratulations, the word {best_word.upper()} was guessed correctly after {num_attempts} attempt(s)!\n")
                self.possible_words = None
                return
            result_array = list()
            for char, digit in zip(best_word, guess_input):
                result_array.append((char, int(digit)))
            remaining_words = set()
            for possible_word in self.possible_words:
                if self.check_possible_word(result_array, possible_word):
                    remaining_words.add(possible_word)
            self.possible_words = remaining_words
            if not self.possible_words:
                print(f"\nRobot has determined that there are no possible words remaining! This may be due to one of the following reasons:")
                print("1. The guess results were entered incorrectly")
                print("2. The target word is not in the robot's lexicon\n")
                self.possible_words = None
                return
            print(f"\nRobot has narrowed the possible words down to the following: {self.possible_words}\n")
            tries_left -= 1
        print(f"Game over! Sorry, the robot was unable to help you guess the word.\n")
        self.possible_words = None


# Code used to train initial Wordle solver
if __name__ == "__main__":
    with open("possible_solutions_word_data.pkl", "rb") as file:
        possible_solutions_word_data = pickle.load(file)
    with open("valid_guesses_data.pkl", "rb") as file:
        valid_guesses_data = pickle.load(file)
    solver = WordleSolver(possible_solutions_word_data, valid_guesses_data, epsilon=0.25)
    solver.train(200000)
    with open("wordle_bot.pkl", "wb") as file:
        pickle.dump(solver, file, -1)
