from movable import Movable
import fruits
import blocks
import pygame
import locations
import directions

class Player(Movable):
	"""Defines the player that the user controls.
	"""

	MOVE_MAP = {
		pygame.K_UP: (0, -1),
		pygame.K_DOWN: (0, 1),
		pygame.K_LEFT: (-1, 0),
		pygame.K_RIGHT: (1, 0)
	}

	def __init__(self, given_board_location, given_board, surface):
		Movable.__init__(self, given_board_location, given_board, surface, ".\\images\\player.png")
		self.is_alive = True
		self.tolerated_types = (fruits.Fruit,)
		self.direction = (1, 0)
		self.score = 0
	
	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			try:
				new_location = self.board_location + self.MOVE_MAP[event.key]
				if new_location in self.board and self.board.is_of_type(new_location, fruits.Fruit) and self.board.is_location_clear(self.tolerated_types, new_location):
					self.score += self.board[new_location].score
					print self.score
				self.move_to(new_location)
				self.direction = self.MOVE_MAP[event.key]
			except KeyError:
				if event.key == pygame.K_SPACE:
					self.shoot()

	def kill(self):
		self.is_alive = False
	
	def shoot(self):
		ice_point = locations.Point.copy(self.board_location) + self.direction
		if ice_point in self.board:
			if self.board.is_frozen(ice_point):
				self.remove_ice()
			else:
				self.shoot_ice()
	
	def remove_ice(self):
		ice_point = locations.Point.copy(self.board_location) + self.direction
		while ice_point in self.board and self.board.is_frozen(ice_point):
			self.board.unfreeze(ice_point)
			ice_point += self.direction
	
	def shoot_ice(self):
		ice_point = locations.Point.copy(self.board_location) + self.direction
		while ice_point in self.board and self.board.is_location_clear(self.tolerated_types, ice_point):
			self.board.freeze(ice_point)
			ice_point += self.direction