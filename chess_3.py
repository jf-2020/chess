# chess_3.py - this prgm will attempt to build the basic backbone to a chess game 
#			   loosely implemented via the pygame.
#			 - 4/27 UPDATE: MVP completed.
#			   
# jf - 4/27

# --- Imports ---
import pygame
from pprint import pprint

# --- Globals ---
# color necessary for background & image transparency
WHITE = (255, 255, 255)
# board size
BOARD_WIDTH = 450
BOARD_HEIGHT = 450

# --- Classes ---
class Board:
	""" this class represents the chess board. """
	# static variables
	board_image = "images/board.png" # relative path to board image
	# below represents the file/rank notation for the board
	board_matrix = [['ABCDEFGH'[i]+str(j) for i in range(8)] 
					for j in reversed(range(1,9))]
	# below represents the top left coordinates corresponding to each
	# cell on board
	board_coordinates = [[(14 + i*53, 14 + j*53) for i in range(8)] 
						for j in range(8)]

	def __init__(self):
		""" constructor: creates the image of the board. """
		# load background image
		self.background = pygame.image.load(Board.board_image).convert_alpha()
		# situate top left of image @ (0, 0)
		self.pos = [0, 0]
		# use a list to keep track of pieces on board
		self.pieces = list()
		# build out the initial board setup
		self.build_initial_board()

	# TODO: potentially refactor #
	def build_initial_board(self):
		""" build out the initial setup of the board. """
		# Kings
		black_king = King("black", Board.board_matrix[0][4])
		self.add_piece(black_king, 0, 4)
		white_king = King("white", Board.board_matrix[7][4])
		self.add_piece(white_king, 7, 4)
		# Queens
		black_queen = Queen("black", Board.board_matrix[0][3])
		self.add_piece(black_queen, 0, 3)
		white_queen = Queen("white", Board.board_matrix[7][3])
		self.add_piece(white_queen, 7, 3)
		# Rooks
		black_rook_queen = Rook("black", Board.board_matrix[0][0])
		self.add_piece(black_rook_queen, 0, 0)
		black_rook_king = Rook("black", Board.board_matrix[0][7])
		self.add_piece(black_rook_king, 0, 7)
		white_rook_queen = Rook("white", Board.board_matrix[7][0])
		self.add_piece(white_rook_queen, 7, 0)
		white_rook_king = Rook("white", Board.board_matrix[7][7])
		self.add_piece(white_rook_king, 7, 7)
		# Bishops
		black_bishop_queen = Bishop("black", Board.board_matrix[0][2])
		self.add_piece(black_bishop_queen, 0, 2)
		black_bishop_king = Bishop("black", Board.board_matrix[0][5])
		self.add_piece(black_bishop_king, 0, 5)
		white_bishop_queen = Bishop("white", Board.board_matrix[7][2])
		self.add_piece(white_bishop_queen, 7, 2)
		white_bishop_king = Bishop("white", Board.board_matrix[7][5])
		self.add_piece(white_bishop_king, 7, 5)
		# Knights
		black_knight_queen = Knight("black", Board.board_matrix[0][1])
		self.add_piece(black_knight_queen, 0, 1)
		black_knight_king = Knight("black", Board.board_matrix[0][6])
		self.add_piece(black_knight_king, 0, 6)
		white_knight_queen = Knight("white", Board.board_matrix[7][1])
		self.add_piece(white_knight_queen, 7, 1)
		white_knight_king = Knight("white", Board.board_matrix[7][6])
		self.add_piece(white_knight_king, 7, 6)
		# Pawns
		for i in range(8):
			black_pawn = Pawn("black", Board.board_matrix[1][i])
			self.add_piece(black_pawn, 1, i)
			white_pawn = Pawn("white", Board.board_matrix[6][i])
			self.add_piece(white_pawn, 6, i)

	def draw(self, screen):
		""" draw the board to the screen. """
		screen.fill(WHITE)
		screen.blit(self.background, self.pos)

	def get_pieces(self):
		""" return a list of the board's current pieces. """
		return self.pieces

	def add_piece(self, piece, row, column):
		""" add a piece to the board. """
		# first, add it to the board's list of pieces
		self.pieces.append(piece)
		# then update its coordinates
		piece.update_coordinates(*Board.board_coordinates[row][column])

	def locate_position_on_board(self, x, y):
		""" given an (x, y) pair (coordinates of a mouse click), locate the 
		respective (rank, file) position on board. """
		for row in range(8):
			for column in range(8):
				# get the coordinates to test against, namely the
				# top left (X, Y)
				X = Board.board_coordinates[row][column][0]
				Y = Board.board_coordinates[row][column][1]
				# check if x between X & X + 53
				if X <= x and x < X + 53:
					# check if y between Y & Y + 53
					if Y <= y and y < Y + 53:
						return Board.board_matrix[row][column]

	def get_coordinates_by_position(self, position):
		""" find the top left coordinates of a given position. """
		for row in range(8):
			for column in range(8):
				# check to see if it's the right position
				if Board.board_matrix[row][column] == position:
					# then grab the corresponding coordinates in the 
					# board_coordinates class var
					return Board.board_coordinates[row][column]

	def get_piece_by_position(self, position):
		""" find and return a piece by its position on the board. """
		# find the piece
		for piece in self.pieces:
			if piece.get_position() == position:
				return piece
		# otherwise nothing is there, so explicity return none
		return None

	def remove_piece(self, piece):
		""" remove a piece from the board's list of pieces. """
		# by rebuild the list of pieces
		new_pieces = list()
		for other_piece in self.pieces:
			# check to see if the piece to delete is the current piece in
			# traversal
			if other_piece == piece:
				# if so, skip it
				continue
			else:
				# if not, add it to the new list of board pieces
				new_pieces.append(other_piece)
		# lastly, reassign the attribute
		self.pieces = new_pieces

class Piece(pygame.sprite.Sprite):
	""" this class represents the abstract class template
	for all pieces in the game. """
	def __init__(self, color, cell, file_path, name = str()):
		""" piece constructor. """
		# call the parent class constructor
		super().__init__()
		# create an image that will hold the 
		self.image = pygame.image.load(file_path).convert_alpha()
		# set the color transparency
		self.image.set_colorkey(WHITE)
		# fetch the rectangle object that has the dimensions of the
		# image.
		self.rect = self.image.get_rect()
		# associate the piece with a color
		self.color = color
		# this corresponds to it's position on the board
		self.cell = cell 
		# give the piece a name
		self.name = name

	def get_color(self):
		""" return the piece's color. """
		return self.color

	def get_position(self):
		""" retun the piece's position. """
		return self.cell

	def get_coordinates(self):
		""" return the piece's coordinates on the board. """
		return self.rect.x, self.rect.y

	def update_coordinates(self, x, y):
		""" move the piece by coordinates. """
		self.rect.x = x
		self.rect.y = y

	def update_position(self, position):
		""" move the piece by algebraic position. """
		self.cell = position

	def update_piece_position(self, move):
		""" this function updates the piece's position on the board, both
		by position & coordinates. """
		# move = (piece, algebraic position, coordinates position)
		piece, position, coordinates = move[0], move[1], move[2]
		# update its board position
		piece.update_position(position)
		# update its board coordinates
		piece.update_coordinates(coordinates[0], coordinates[1])

	def __str__(self):
		""" human readable string. """
		return "{} >> {} on {}".format(type(self).__name__, self.color, self.cell)
	
class King(Piece):
	""" this class represents the King. it inherits from Piece, so
	in turn it inherits from pygame's sprite class. """
	# static variables for image paths
	black = "images/_kingB2.png"
	white = "images/_kingW2.png"

	def __init__(self, color, cell):
		""" constructor: king. """
		# first, handle the colors separately
		if color == "black":
			# call the parent class constructor on the black image
			super().__init__(color, cell, King.black, name = "King")
		else:
			# call the parent class constructor on the white image
			super().__init__(color, cell, King.white, name = "King")
		# then, set value attributes
		self.value = 10**80 # arbitrarily large number per game conditions

class Queen(Piece):
	""" this class represents the Queen. it inherits from Piece, so
	in turn it inherits from pygame's sprite class. """
	# static variables for image paths
	black = "images/_queenB2.png"
	white = "images/_queenW2.png"

	def __init__(self, color, cell):
		""" constructor: queen. """
		# first, handle the colors separately
		if color == "black":
			# call the parent class constructor on the black image
			super().__init__(color, cell, Queen.black, name = "Queen")
		else:
			# call the parent class constructor on the white image
			super().__init__(color, cell, Queen.white, name = "Queen")
		# then, set the value
		self.value = 9

class Rook(Piece):
	""" this class represents the Rook. it inherits from Piece, so
	in turn it inherits from pygame's sprite class. """
	# static variables for image paths
	black = "images/_rookB2.png"
	white = "images/_rookW2.png"

	def __init__(self, color, cell):
		""" constructor: rook. """
		# first, handle the colors separately
		if color == "black":
			# call the parent class constructor on the black image
			super().__init__(color, cell, Rook.black, name = "Rook")
		else:
			# call the parent class constructor on the white image
			super().__init__(color, cell, Rook.white, name = "Rook")
		# then, set the value
		self.value = 5

class Bishop(Piece):
	""" this class represents the Bishop. it inherits from Piece, so
	in turn it inherits from pygame's sprite class. """
	# static variables for image paths
	black = "images/_bishopB2.png"
	white = "images/_bishopW2.png"

	def __init__(self, color, cell):
		""" constructor: bishop. """
		# first, handle the colors separately
		if color == "black":
			# call the parent class constructor on the black image
			super().__init__(color, cell, Bishop.black, name = "Bishop")
		else:
			# call the parent class constructor on the white image
			super().__init__(color, cell, Bishop.white, name = "Bishop")
		# then, set the value
		self.value = 3

class Knight(Piece):
	""" this class represents the Knight. it inherits from Piece, so
	in turn it inherits from pygame's sprite class. """
	# static variables for image paths
	black = "images/_knightB2.png"
	white = "images/_knightW2.png"

	def __init__(self, color, cell):
		""" constructor: knight. """
		# first, handle the colors separately
		if color == "black":
			# call the parent class constructor on the black image
			super().__init__(color, cell, Knight.black, name = "Knight")
		else:
			# call the parent class constructor on the white image
			super().__init__(color, cell, Knight.white, name = "Knight")
		# then, set the value
		self.value = 3

class Pawn(Piece):
	""" this class represents the Pawn. it inherits from Piece, so
	in turn it inherits from pygame's sprite class. """
	# static variables for image paths
	black = "images/_pawnB2.png"
	white = "images/_pawnW2.png"

	def __init__(self, color, cell):
		""" constructor: pawn. """
		# first, handle the colors separately
		if color == "black":
			# call the parent class constructor on the black image
			super().__init__(color, cell, Pawn.black, name = "Pawn")
		else:
			# call the parent class constructor on the white image
			super().__init__(color, cell, Pawn.white, name = "Pawn")
		# then, set the value
		self.value = 1

class Game:
	""" this class represents an instance of the game. if game
	reset is necessary, just re-instantiate. """
	def __init__(self, screen):
		""" constructor: creates all attributes and
		initializes the game. """
		# load in the screen
		self.screen = screen
		# create the board
		self.board = Board()
		# create sprite lists for pieces
		self.white_pieces = pygame.sprite.Group()
		self.black_pieces = pygame.sprite.Group()
		self.all_pieces = pygame.sprite.Group()
		# add board pieces to the sprite lists
		for piece in self.board.get_pieces():
			# handle the sprite by color
			if piece.get_color() == "black":
				self.black_pieces.add(piece)
			else:
				self.white_pieces.add(piece)
			self.all_pieces.add(piece)

	def check_for_exit(self):
		""" event handler """
		for event in pygame.event.get():
			# check to see if exited:
			if event.type == pygame.QUIT:
				# if so, pass True to game loop
				return True
		# otherwise, continue the game
		return False

	def display_frame(self, screen):
		""" display everything to the screen. """
		self.board.draw(screen)
		self.all_pieces.draw(screen)
		pygame.display.flip()

	def get_move(self):
		""" ask user to input the algebraic notation corresponding to the
		piece they want to move & where to move it. then get said piece,
		and get its coordinates, returning all a triple of it all. """
		# first, have user input piece to move in algebraic notation
		move_this_piece = input("Enter piece to move: ")
		# second, get the piece on the board
		piece = self.board.get_piece_by_position(move_this_piece)
		# third, have user input where to move the piece
		move_to = input("Enter where to move: ")
		# then convert algebraic notation of target cell to coordinates
		coordinates_to = self.board.get_coordinates_by_position(move_to)
		# return triple
		return piece, move_to, coordinates_to

	def make_move(self, move):
		""" this function will take a piece, a target position & target
		coordinates and update the piece's position on the board as such. """
		# first, clear off target position on board. that is, if a piece is
		# already occupying the space, then remove it as it has been taken
		piece_to_remove = self.board.get_piece_by_position(move[1])
		# check that it's indeed non-empty:
		if piece_to_remove:
			# first, remove it from the board
			self.board.remove_piece(piece_to_remove)
			# then remove it from sprite list
			piece_to_remove.kill()
		# finally, make the move
		move[0].update_piece_position(move)

	def get_sprite_lists(self):
		""" return three lists: black, white and all sprites, respectively. """
		black_pieces = [piece for piece in self.black_pieces]
		white_pieces = [piece for piece in self.white_pieces]
		all_pieces = [piece for piece in self.all_pieces]
		return black_pieces, white_pieces, all_pieces

	def pieces_on_board(self):
		""" access board attribute, pieces. """
		return self.board.get_pieces()

	def turn_logic(self):
		""" this function will, effectively, perform the move. """
		move = self.get_move()
		self.make_move(move)

	def print_game_state(self, length = "y", lists = "y"):
		""" this function prints out the current game state. namely, it lists
		the current sprites in the game, the current pieces on the board, and
		the respective size of these lists. """
		print()
		print("=== GAME STATE ===")
		# get the sprites
		sprites = self.get_sprite_lists()[2]
		# get the board pieces
		pieces = self.pieces_on_board()
		# now print data
		if length == "y":
			print("number of sprites: %d" % len(sprites))
			print("number of pieces: %d" % len(pieces))
		print()
		if lists == "y":
			print("=== sprites list ===")
			for sprite in sprites:
				print(str(sprite))
			print()
			print("=== pieces on the board ===")
			for piece in pieces:
				print(str(piece))
			print()

# --- Testing ---
def test(game, screen):
	""" all tests will be handled here. """
	## first, see what pieces are on the board
	beginning_pieces_on_board = game.pieces_on_board()
	pprint(beginning_pieces_on_board)
	print()
	## second, determine their positions
	for piece in beginning_pieces_on_board:
		print(piece, "| pos: " + piece.get_position())
	## third, test get_move() function
	move = game.get_move()
	piece = move[0]
	print("piece:", piece)
	print("current pos: %s" % piece.get_position())
	print("current coor: (%d, %d)" % piece.get_coordinates())
	print("target pos: %s" % move[1])
	print("target coor: (%d, %d)" % move[2])
	# get lens of sprites lists before
	pieces_before = game.get_sprite_lists()
	black_sprites_len_before = len(pieces_before[0])
	white_sprites_len_before = len(pieces_before[1])
	all_sprites_len_before = len(pieces_before[2])
	# get len of board pieces list before
	before_pieces_on_board_len = len(game.pieces_on_board())
	## fourth, test make_move() function
	game.make_move(move)
	print("updated pos: %s" % piece.get_position())
	print("updated coor: (%d, %d)" % piece.get_coordinates())
	print()
	## fifth, see if board updates following a move
	game.display_frame(screen)

def test_2(game, screen):
	""" in the event pieces aren't working properly, use this to debug what's
	happening to the board pieces & sprite lists during each move. """
	# (1) sprites
	pieces = game.get_sprite_lists()
	print("=== black pieces ===")
	pprint(pieces[0])
	print()
	pprint("=== white pieces ===")
	pprint(pieces[1])
	print()
	pprint("=== all pieces ===")
	pprint(pieces[2])
	# check if the lens are different b/a (shouldn't be..)
	black_sprites_len_after = len(pieces[0])
	white_sprites_len_after = len(pieces[1])
	all_sprites_len_after = len(pieces[2])
	print("black: b4 = %d after = %d" % (black_sprites_len_before,
										black_sprites_len_after))
	print("white: b4 = %d after = %d" % (white_sprites_len_before,
										white_sprites_len_after))
	print("all: b4 = %d after = %d" % (all_sprites_len_before,
										all_sprites_len_after))
	print()
	# (2) the board
	board_pieces = game.pieces_on_board()
	print("=== pieces on board ===")
	pprint(board_pieces)
	# check if the lens are differnt b/a (shouln't be)
	print("b4 = %d after = %d" % (before_pieces_on_board_len,
								len(board_pieces)))

# --- Main ---
def main():
	""" main program function. """
	# init the game
	pygame.init()
	# open and set a window size
	size = [BOARD_WIDTH, BOARD_HEIGHT]
	screen = pygame.display.set_mode(size)
	# set the window's title
	pygame.display.set_caption("My Game")
	# use boolean to keep track of state of close button
	done = False
	# a measure of time
	clock = pygame.time.Clock()
	# don't hide the mouse cursor
	pygame.mouse.set_visible(True)
	# instantiate the necessary per game classes
	board = Board()
	game = Game(screen)
	# main game loop
	while not done:
		# draw the current frame
		game.display_frame(screen)
		# take a turn
		game.check_for_exit()
		game.turn_logic()
		# visual inspection of current state
		game.print_game_state(length = "y", lists = "n")
		# pause for next frame
		clock.tick(144)
	# quit
	pygame.quit()

# when running as script, call main
if __name__ == "__main__":
	main()