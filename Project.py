import numpy as np
import random
import pygame
import sys
import math

#set color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (95, 141, 250)
YELLOW = (250, 239, 82)
RED = (252, 58, 58)


#define constant
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
PLAYER_PIECE = 1
AI = 1
AI_PIECE = 2
EMPTY = 0
WINDOW_LENGTH = 4
SQUARESIZE = 100

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
				return True

def evaluate_window(window, piece):
	heuristic = 0
	opp_piece = PLAYER_PIECE
	if piece == PLAYER_PIECE:
		opp_piece = AI_PIECE

	if window.count(piece) == 4:
		heuristic += 100
	elif window.count(piece) == 3 and window.count(EMPTY) == 1:
		heuristic += 5
	elif window.count(piece) == 2 and window.count(EMPTY) == 2:
		heuristic += 2

	if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
		heuristic -= 4

	return heuristic

def heuristic_position(board, piece):
	heuristic = 0

	## heuristic center column
	center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
	center_count = center_array.count(piece)
	heuristic += center_count * 3

	## heuristic Horizontal
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r, :])]
		for c in range(COLUMN_COUNT - 3):
			window = row_array[c: c + WINDOW_LENGTH]
			heuristic += evaluate_window(window, piece)

	## heuristic Vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:, c])]
		for r in range(ROW_COUNT - 3):
			window = col_array[r:r + WINDOW_LENGTH]
			heuristic += evaluate_window(window, piece)

	## heuristic positive sloped diagonal
	for r in range(ROW_COUNT - 3):
		for c in range(COLUMN_COUNT - 3):
			window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
			heuristic += evaluate_window(window, piece)

	## heuristic positive sloped diagonal
	for r in range(ROW_COUNT - 3):
		for c in range(COLUMN_COUNT - 3):
			window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
			heuristic += evaluate_window(window, piece)

	return heuristic

def is_terminal_node(board):
	return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, maximizimg_player):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 and is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None,  1000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -1000000000000)
			else: #game is over, no more valid moves
				return (None, 0)
		else: # depth is zero
			return (None, score_position(board, AI_PIECE))
	if maximizimg_player:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_score = minimax(b_copy, depth - 1, False)[1]
			if new_score > value:
				value = new_score
				column = col
			return column, value
	else: #Minimizing Player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_score = minimax(b_copy, depth - 1, True,)[1]
			if new_score < value:
				value = new_score
				column = col
			return column, value

def  minimaxab(board, depth, alpha, beta, maximizingPlayer):
	valid_locations = get_valid_locations(board)
	is_terminal = is_terminal_node(board)
	if depth == 0 or is_terminal:
		if is_terminal:
			if winning_move(board, AI_PIECE):
				return (None,  100000000000000)
			elif winning_move(board, PLAYER_PIECE):
				return (None, -100000000000000)
			else: # Game is over, no more valid moves
				return (None, 0)
		else: # Depth is zero
			return (None, heuristic_position(board, AI_PIECE))
	if maximizingPlayer:
		value = -math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, AI_PIECE)
			new_heuristic = minimaxab(b_copy, depth-1, alpha, beta, False)[1]
			if new_heuristic > value:
				value = new_heuristic
				column = col
			alpha = max(alpha, value)
			if alpha >= beta:
				break
		return column, value

	else: # Minimizing player
		value = math.inf
		column = random.choice(valid_locations)
		for col in valid_locations:
			row = get_next_open_row(board, col)
			b_copy = board.copy()
			drop_piece(b_copy, row, col, PLAYER_PIECE)
			new_heuristic = minimaxab(b_copy, depth - 1, alpha, beta, True)[1]
			if new_heuristic < value:
				value = new_heuristic
				column = col
			beta = min(beta, value)
			if alpha >= beta:
				break
		return column, value

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, (r + 1) * SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, WHITE, (int((c + 1/2) * SQUARESIZE), int((r + 3/2) * SQUARESIZE)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == PLAYER_PIECE:
				pygame.draw.circle(screen, RED, (int((c + 1/2) * SQUARESIZE), height - int((r + 1/2) * SQUARESIZE)), RADIUS)
			elif board[r][c] == AI_PIECE: 
				pygame.draw.circle(screen, YELLOW, (int((c + 1/2) * SQUARESIZE), height - int((r + 1/2) * SQUARESIZE)), RADIUS)
	pygame.display.update()

board = np.zeros((ROW_COUNT,COLUMN_COUNT))
game_over = False

pygame.init()

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == PLAYER:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
			
			# Ask for Player 1 Input
			if turn == PLAYER:
				posx = event.pos[0]
				col = int(math.floor(posx / SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, PLAYER_PIECE)

					if winning_move(board, PLAYER_PIECE):
						label = myfont.render("Player 1 wins!!", 1, RED)
						screen.blit(label, (40, 10))
						game_over = True

					turn = (turn + 1) % 2

					draw_board(board)


	# Ask for Player 2 Input
	if turn == AI and not game_over:				

		col, minimax_heuristic = minimaxab(board, 6, -math.inf, math.inf, True)

		if is_valid_location(board, col):
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, AI_PIECE)
			if winning_move(board, AI_PIECE):
				label = myfont.render("Player 2 wins!!", 1, YELLOW)
				screen.blit(label, (40,10))
				game_over = True

			draw_board(board)

			turn = (turn + 1) % 2

	if game_over:
		pygame.time.wait(2000)