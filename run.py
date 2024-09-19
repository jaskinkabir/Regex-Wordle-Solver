from solver import Solver
from tiny_solver import TinySolver
import re

solver = TinySolver(word_file='words.txt')
for _ in range(4):
    while not re.match(r'^[a-z]{5}$', (guess := input("Guess: "))): guess = input("Invalid. 5 lowercase: ")
    while not re.match(r'^[bgy]{5}$', (colors := input("Colors: "))): colors = input("Invalid. 5 [bgy]: ")
    solver.guess(guess, colors)
    print(', '.join(solver.words))