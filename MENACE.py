"""
MENACE.py
Python 3 Implementation of MENACE
Machine Educable Naughts and Crosses Engine
Author: Gurleen Singh <gs585@drexel.edu>
Department of Computer Science, Drexel University
"""

import os
import math
import random
import pickle
import argparse
from tqdm import tqdm

# Command line arguments
parser = argparse.ArgumentParser(description="Machine Educable Naughts and Crosses Engine (MENACE)")
parser.add_argument('--learn', '-l', nargs=1, type=int)

# Constants
BLANK = 0
HUMAN = 1
COMPUTER = 2
DRAW = -1

record = [0,0,0]	# Wins, Losses, Draws

# Game state
matchboxes = {}
board = [0,0,0,0,0,0,0,0,0]
played = {}
learn_mode = False

def dprint(*argv):
	if learn_mode:
		return
	for arg in argv:
		print(arg, end=' ')
	print()

def end_session():
	f = open("mboxes.pkl", "wb")
	pickle.dump(matchboxes, f)
	f.close()
	f = open("record", "w")
	f.write(str(record))
	f.close()
	print("Wins:", record[0], "Losses:", record[1], "Draws:", record[2])
	print("Matchboxes saved to mboxes.pkl")
	quit()


def int_input():
	while True:
		try:
			s = "> "
			if learn_mode:
				s = ""
			inp = input(s)
			if inp == 'quit':
				end_session()
			else:
				inp = int(inp)
		except ValueError:
			dprint("Invalid input")
			continue
		else:
			return inp

def encode_board(board): 
	i = 0
	n = 0
	for pos in board:
		n += pos * (3**i)
		i += 1
	return n

def print_board(board):
	for idx, num in enumerate(board):
		if num == HUMAN:
			print("H", end=" ")
		elif num == COMPUTER:
			print("C", end=" ")
		else:
			print("_", end=" ")
		if idx in [2,5,8]:
			nums = (idx-2, idx-1, idx)
			print("\t", nums[0], nums[1], nums[2])
			pass

def human():
	print_board(board)
	dprint("Enter a board pos ")
	while True:
		pos = int_input()
		if pos not in range(0,9):
			dprint("Invalid input")
			pass
		elif board[pos] != BLANK:
			dprint("Position already taken")
			pass
		else:
			break
	board[pos] = HUMAN

def auto_teach():
	available = [i for i in range(0,9) if board[i] == BLANK]
	board[random.choice(available)] = HUMAN

def get_matchbox(idx):
	if idx not in matchboxes:
		matchboxes[idx] = [10 if i==BLANK else 0 for i in board]
	return matchboxes[idx]

def pick_bead(entry, total, idx):
	beads = []
	for i, qty in enumerate(matchboxes[idx]):
		for _ in range(0, qty):
			beads.append(i)
	if len(beads) == 0 or beads is None:
		dprint("Dead end")
		process_win(HUMAN)
		return -1
	chosen = random.choice(beads)
	played[idx] = chosen
	return chosen
	
def menace():
	idx = encode_board(board)
	dprint("Getting matchbox #{0}...".format(idx))
	entry = get_matchbox(idx)
	total = sum(entry)
	chosen = pick_bead(entry, total, idx)
	if chosen == -1:
		return
	dprint("MENACE chose:", chosen)
	board[chosen] = COMPUTER

def check_win():
	locs = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
	for loc in locs:
		if board[loc[0]] == board[loc[1]] and board[loc[1]] == board[loc[2]]:
			return board[loc[0]]
		else:
			continue
	if 0 not in board:
		return -1
	else:
		return -2

def process_win(winner):
	adj = 0
	if winner == HUMAN:
		dprint("You won")
		record[1] += 1
		adj = -1
	elif winner == COMPUTER:
		dprint("MENACE won")
		record[0] += 1
		adj = 3
	elif winner == DRAW:
		dprint("It's a draw")
		record[2] += 1
		adj = 1
	dprint("MENACE's moves:")
	dprint(played)
	feedback(adj)
	reset()
	dprint("------New Game------")

def feedback(adj):
	for box in played:
		matchboxes[box][played[box]] += adj

def reset():
	global board
	global played
	board = [0,0,0,0,0,0,0,0,0]
	played = {}

def learn_loop(ngames):
	print("Doing", ngames, "iterations...")
	for _ in tqdm(range(0, ngames)):
		auto_teach()
		state = check_win()
		if state in [COMPUTER, HUMAN, DRAW]:
			process_win(state)
			continue
		menace()
		if state in [COMPUTER, HUMAN, DRAW]:
			process_win(state)
	end_session()

def human_loop():
	while True:
		human()
		state = check_win()
		if state in [COMPUTER, HUMAN, DRAW]:
			process_win(state)
			continue
		menace()
		state = check_win()
		if state in [COMPUTER, HUMAN, DRAW]:
			process_win(state)

def main():
	print("Welcome to MENACE:")
	print("Machine Educable Naughts and Crosses Engine")
	global matchboxes
	global learn_mode
	args = parser.parse_args()
	ngames = 0
	if os.path.exists("mboxes.pkl"):
		print("Loading existing matchboxes...")
		f = open("mboxes.pkl", "rb")
		matchboxes = pickle.load(f)
		f.close()
	if args.learn:
		learn_mode = True
		learn_loop(args.learn[0])
	else:
		human_loop()

if __name__ == '__main__':
	main()
