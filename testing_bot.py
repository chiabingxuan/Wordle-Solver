import pickle
import csv
from wordle_solver import WordleGame, WordleSolver


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
    with open("possible_solutions_word_data.pkl", "rb") as file:
        possible_solutions_word_data = pickle.load(file)
    with open("valid_guesses_data.pkl", "rb") as file:
        valid_guesses_data = pickle.load(file)
    with open("wordle_bot.pkl", "rb") as file:
        solver = pickle.load(file)
    solver.solve()
    end = input("Enter any key to quit: ")
