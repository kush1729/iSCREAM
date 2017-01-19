from movables import Movable

class Player(Movable):
	"""Defines the player that the user controls.
	"""

	def __init__(self, given_board_location, given_image_string, given_board):
		super(Player, self).__init__(given_board_location, given_image_string, given_board)
		self.is_alive = True
	
	def move(self, x_displacement, y_displacement):
		new_location = Point(
			self.position.x_coordinate + x_displacement,
			self.position.y_coordinate + y_displacement)
		if self.board.is_location_clear(new_location):
			self.move_to(new_location)
	
	def kill(self):
		self.is_alive = False