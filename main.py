import pickle
import csv
import os
from wordle_solver import WordleGame, WordleSolver
from config import game_mode


def test_and_write_to_csv(wordle_solver, filename, num_trials, header=False):
    trained_results = wordle_solver.test(num_trials)
    result_fields = ["epsilon"] + [str(i) for i in range(1, wordle_solver.num_tries + 1)]
    result_fields.extend(["failed", "success_rate", "average_number_of_attempts"])
    with open(filename, "a") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=result_fields)
        if header:
            writer.writeheader()
        writer.writerow(trained_results)
    print(f"Test results have been written to {filename}")


def train_and_save(wordle_solver, filename, num_trials):
    wordle_solver.train(num_trials)
    with open(filename, "wb") as bot_file:
        pickle.dump(wordle_solver, bot_file, -1)


if __name__ == "__main__":
    os.system("color")
    if game_mode == "human":
        with open("possible_solutions_word_data.pkl", "rb") as file:
            possible_solutions_word_data = pickle.load(file)
        with open("valid_guesses_data.pkl", "rb") as file:
            valid_guesses_data = pickle.load(file)
        game = WordleGame(possible_solutions_word_data, valid_guesses_data)
        game.play()
    else:
        with open("wordle_bot.pkl", "rb") as file:
            solver = pickle.load(file)
        if game_mode == "robot":
            solver.solve()
        elif game_mode == "simulate":
            solver.simulate()
        else:
            print("Invalid game mode, please check config.py and enter an appropriate game mode!")
    end = input("Enter any key to quit: ")
