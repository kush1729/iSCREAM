from movable import Movable

class Player(Movable):
	"""Defines the player that the user controls.
	"""

	def __init__(self, given_board_location, given_board, surface, given_image_string):
		Movable.__init__(self, given_board_location, given_board, surface, given_image_string)
		self.is_alive = True
	
	def move(self, x_displacement, y_displacement):
		new_location = Point(
			self.position.x_coordinate + x_displacement,
			self.position.y_coordinate + y_displacement)
		if self.board.is_location_clear(new_location):
			self.move_to(new_location)
	
	def kill(self):
		self.is_alive = False