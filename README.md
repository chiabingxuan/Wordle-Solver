# Wordle Solver
## Introduction
This project presents an implementation of the game "Wordle", as well as an intelligent bot that can play the game with a success rate of more than 99%, solving puzzles in an average of 3.65 attempts per successful game.

## General Idea
Note that when a guess is made in "Wordle", we can make deductions from the result of the guess, eliminating words that are no longer possible. Hence, at the end of each guess, the bot will update the set of possible words remaining, before choosing a word from this set for the next guess. If this selection of words were made randomly, the bot would have a decent performance, but this can be improved significantly.

The goal, then, is to come up with a suitable metric which allows the bot to select words with a certain level of intelligence, enabling it to make more informed guesses and thus attain a better performance. For this, we introduce the idea of *cancelling power*. The *cancelling power of a word for a given turn* is defined to be the average fraction of possible words that are eliminated, after guessing that word in that turn. Suppose we have good estimates of the cancelling powers of every word for each of the 6 turns. Then at the start of each turn *n*, the bot will consider the set of possible words remaining, and choose the word with the highest cancelling power for that turn *n*. The underlying assumption is that for a given turn, a word with a higher cancelling power would be a smarter guess, since it eliminates a larger fraction of possible words.

It now remains for us to obtain good estimates of these cancelling powers. To do this, we first made sure that the bot stored a dictionary which would contain the cancelling powers of every word, for each of the 6 turns. The bot was then trained on a large number of simulation games. With the explore-exploit tradeoff in mind, an epsilon value of 0.25 was chosen. In other words, we ensured that words for each guess were selected either randomly (with a probability of 25%) or based on the *cancelling power metric* (with a probability of 75%). During this training process, the bot took note of the fraction of possible words eliminated after each guess, updating the cancelling powers accordingly.

The bot was subjected to 10000 testing games, both before and after training. The testing results can be found in the `Results of Bot Testing` folder.

## Results
For an untrained bot that simply chose words randomly, it had a success rate of around 97%, with an average of 4.27 attempts per successful game. After training on 50000 simulation games with epsilon = 0.25, the bot improved to a success rate of 99.2%, with an average of 3.65 attempts per successful game.

## How to Use
The bot provided in the repository, `wordle_bot.pkl`, was trained on 200000 simulation games.

1. Clone the repository as follows:
```
git clone https://github.com/chiabingxuan/Wordle-Solver.git
```
2. In `config.py`, you can configure the game to your desired game mode.
3. Set your working directory to the folder containing the cloned repository:
```
cd Wordle-Solver
```
4. Install necessary packages:
```
pip install -r requirements.txt
```  
5. Run the program:
```
python main.py
```
