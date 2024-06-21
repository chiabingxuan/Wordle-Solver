# Wordle Solver
## Introduction
This project presents an implementation of the game "Wordle", as well as an intelligent bot that can play the game with a success rate of more than 99%, solving puzzles in an average of 3.65 attempts per successful game.

## General Idea
Note that when a guess is made in "Wordle", we can make deductions from the result of the guess, eliminating words that are no longer possible. Hence, at the end of each guess, the bot will update the set of possible words remaining, before choosing a word from this set for the next guess. If this selection of words were made randomly, the bot would have a decent performance (success rate of around 97%, with an average of 4.27 attempts per successful game), but this can be improved significantly.

The goal, then, is to come up with a suitable metric which allows the bot to select words with a certain level of intelligence, enabling it to make more informed guesses and thus attain a better performance. For this, we introduce the idea of *cancelling power*. The *cancelling power of a word for a given turn* is defined to be the average fraction of possible words that are eliminated, after guessing that word in that turn. Suppose we have good estimates of the cancelling powers of every word for each of the 6 turns. Then at the start of each turn *n*, the bot will consider the set of possible words remaining, and simply choose the word with the highest cancelling power for that turn *n*. The underlying assumption is that for a given turn, a word with a higher cancelling power would be a smarter guess, since it eliminates a larger fraction of possible words.

It now remains for us to obtain good estimates of these cancelling powers. To do this, the bot was trained on 200000 simulation games.



## How to Use
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
