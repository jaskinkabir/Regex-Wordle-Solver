import sys
import random
from solver import Solver
from tiny_solver import TinySolver

def getcolors(true_word, guess):
    r = ""
    true_word_list = list(true_word)
    for t, g in zip(true_word, guess):
        if t == g:
            r += 'g'
            true_word_list.remove(t)
        elif g in true_word_list:
            r += 'y'
            true_word_list.remove(g)
        else:
            r += 'b'
    return r

words = [word.strip() for word in open("words.txt").readlines()]
wordlist = []
for i in range(10):
    random.seed(i*69)
    random.shuffle(words)
    wordlist.append(words[:100])

def guess_word(solver, guess, real):
    solver.guess(guess, getcolors(real, guess))
    return solver.get_solutions()[0]

def solve_tiny(firstword="trash"):
    total_guesses = 0
    for l in wordlist:
        for word in l:
            guess_c = 1
            solver = Solver()
            next_guess = guess_word(solver, firstword, word)
            while next_guess != word:
                next_guess = guess_word(solver, next_guess, word)
                guess_c += 1
            total_guesses += guess_c
    return total_guesses

def solve_old():
    solver = Solver()
    solver.guess()

if __name__ == "__main__":
    # if len(sys.argv) < 2:
    #     print("please enter which algorithm to use. options are old, tiny.")
    #     exit(1)
    solve_tiny()
    # if sys.argv[1] == "old": solve_old()
    # if sys.argv[1] == "tiny": solve_tiny()