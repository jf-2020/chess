# chess_2.py - this prgm will attempt to build the basic backbone
#			   to a chess game implemented via the pygame
#			   library.
#
# jf - 4/25


# --- Imports ---
import pygame

# debugging
from pprint import pprint


# --- Global Constants ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# store colors in list for random choice
colors = [BLACK, WHITE, RED, GREEN, BLUE]

# board size
BOARD_WIDTH = 450
BOARD_HEIGHT = 450


# --- Classes ---
class Board:
	""" this class represents the chess board. """
	
	# static variables
	size = [450, 450] # dimensions of the board
	position = [0, 0] # where to place the board on the screen
	board_image = "images/board.png" # relative path to board image
	piece_in_motion = None # store piece that's in motion

	# TODO: figure out better way to code this in
	board_matrix = [ 
						['ABCDEFGH'[i]+'8' for i in range(8)],
						['ABCDEFGH'[i]+'7' for i in range(8)],
						['ABCDEFGH'[i]+'6' for i in range(8)],
						['ABCDEFGH'[i]+'5' for i in range(8)],
						['ABCDEFGH'[i]+'4' for i in range(8)],
						['ABCDEFGH'[i]+'3' for i in range(8)],
						['ABCDEFGH'[i]+'2' for i in range(8)],
						['ABCDEFGH'[i]+'1' for i in range(8)]
					]

	board_coordinates = [[(14 + i*53, 14 + j*53) for i in range(8)] for j in range(8)]


	def __init__(self):
		""" constructor: creates the image of the board. """
		self.background = pygame.image.load(Board.board_image).convert_alpha()
		self.pos = Board.position
		self.pieces = list()

		self.build_initial_board()

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
		piece.update(*Board.board_coordinates[row][column])

	def locate_position_on_board(self, x, y):
		""" given an (x, y) pair (coordinates of a mouse click),
		locate the respective (rank, file) position on board. """
		for row in range(8):
			for column in range(8):

				# get the coordinates to test against, namely the
				# top left (X, Y)
				X = Board.board_coordinates[row][column][0]
				Y = Board.board_coordinates[row][column][1]

				# testing
				# print(X, type(X))
				# print(x, type(x))

				# check if x between X & X + 53
				if X <= x and x < X + 53:
					# check if y between Y & Y + 53
					if Y <= y and y < Y + 53:

						return Board.board_matrix[row][column]

	def get_piece_by_position(self, position):
		""" find and return a piece by its position on the board. """
		for piece in self.pieces:
			if piece.get_position() == position:
				return piece

	'''
	def remove_piece(self, piece):
		""" remove a piece from the board's list of pieces. """

		# get the piece's position on the board
		from_position = piece.get_position()

		# remove it
		del self.pieces[from_position]
	'''


# N.B. NOT MEANT TO BE CALLED DIRECTLY #
class Piece(pygame.sprite.Sprite):
	""" this class represents the abstract class template
	for all pieces in the game. """
	
	def __init__(self, color, cell, file_path, name = str()):
		# call the parent class constructor
		super().__init__()

		# create an image that will hold the 
		self.image = pygame.image.load(file_path).convert_alpha()
		# set the color transparency
		self.image.set_colorkey(WHITE)

		# fetch the rectangle object that has the dimensions of the
		# image. then, update the pos of this obj by setting the
		# x,y coor values (n.b. via get center)
		self.rect = self.image.get_rect()

		# associate the piece with a color
		self.color = color

		# this corresponds to it's position on the board
		self.cell = cell 

		# give the piece a name
		self.name = name

		# prepare for piece movement events
		self.selected = False

	def rectangle(self):
		# return the piece's sprite rect
		return self.rect

	def get_color(self):
		# return the piece's color
		return self.color

	def get_position(self):
		# retun the piece's position
		return self.cell

	def get_coordinates(self):
		# return the piece's coordinates on the board
		return self.rect.x, self.rect.y

	def update(self, x, y):
		# move the piece

		# TODO: update it's board position

		self.rect.x = x
		self.rect.y = y

	def is_dragging(self):
		# boolean for whether or not it's being dragged
		return self.dragging == True

	def toggle(self):
		# toggle the dragging attribute
		if self.selected == False:
			self.selected = True
		else:
			self.selected = False

	def is_toggled(self):
		# access selected attribute
		return self.selected

	def draw(self, x, y):
		self.move_ip(x, y)

	def __str__(self):
		# create some readable output, if necessary
		return "{} >> {} on {}".format(type(self).__name__, self.color, self.cell)
	

class King(Piece):
	""" this class represents the King. it inherits from Piece, so
	in turn it inherits from pygame's sprite class. """

	# static variables for image paths
	black = "images/_kingB2.png"
	white = "images/_kingW2.png"

	def __init__(self, color, cell):

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

		# create sprite list for board cells
		self.board_cells = pygame.sprite.Group()

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

		# mouse position
		self.mouse_x = 0
		self.mouse_y = 0
		
		# list of selected pieces
		self.selected_pieces = list()

		# store 'move to' position
		self.move_to = list()

	def process_events(self):
		""" process all of the events. return 'True' if close window
		is necessary. """
		for event in pygame.event.get():

			# get the mouse position
			mouse_x = pygame.mouse.get_pos()[0]
			mouse_y = pygame.mouse.get_pos()[1]

			# click the exit button
			if event.type == pygame.QUIT:
				return True

			# left click only
			elif event.type == pygame.MOUSEBUTTONDOWN:
				
				print("selected pieces:", self.get_selected_pieces())

				# selecting a piece
				if event.button == 1 and not self.get_selected_pieces():

					# get board position and piece underlying mouse
					board_position = self.board.locate_position_on_board(mouse_x, mouse_y)
					piece = self.board.get_piece_by_position(board_position)

					# check if there's a collision with the cursor & a sprite
					if piece.rectangle().collidepoint(mouse_x, mouse_y):
						
						# update dragging attribute
						piece.toggle()
						print(piece, "<--> toggled: " + str(piece.is_toggled()))

						'''
						# get the mouse & piece coordinates
						piece_pos = piece.get_coordinates()
						'''

						# add it to selected pieces
						self.selected_pieces.append(piece)

				# dropping a piece
				elif event.button == 1 and self.get_selected_pieces() and not self.move_to:
					# store the new mouse position

					self.move_to.extend((mouse_x, mouse_y))

					print("move to:", self.move_to)

					# update the piece's position

					for piece in self.get_selected_pieces():

						piece.update(mouse_x, mouse_y)

						self.update_mouse_pos(mouse_x, mouse_y)

					# remove the piece from selected pieces
					self.selected_pieces = list()

		return False

	def run_logic(self):
		""" update positions & check for sprite collisions. to be run
		once for each frame. """

		for piece in self.all_pieces:

			if piece in self.get_selected_pieces():
				
				x, y = self.get_mouse_pos()

				# print("before:", self.get_selected_pieces())

				# get board position in which mouse cursor lies
				board_position = self.board.locate_position_on_board(x, y)

				piece.update(x, y)

				# print("after:", self.get_selected_pieces())

	def display_frame(self, screen):
		# display everything to screen
		self.board.draw(screen)
		self.all_pieces.draw(screen)

		pygame.display.flip()

	def get_selected_pieces(self):
		# returns a list of selected pieces
		return self.selected_pieces

	def update_mouse_pos(self, x, y):
		# change the mouse attribute's coordinates
		self.mouse_x = x
		self.mouse_y = y

	def get_mouse_pos(self):
		# return mouse position's coordinates
		return self.mouse_x, self.mouse_y


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

	board = Board()
	game = Game(screen)

	# main game loop
	while not done:

		# process events
		done = game.process_events()

		# update positions & check collisions
		game.run_logic()

		# draw the current frame
		game.display_frame(screen)

		# pause for next frame
		clock.tick(144)

	# quit
	pygame.quit()


# when running as script, call main
if __name__ == "__main__":
	main()