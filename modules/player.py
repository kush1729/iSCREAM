from movable import Movable
import pygame
import locations

class Player(Movable):
	"""Defines the player that the user controls.
	"""

	def __init__(self, given_board_location, given_board, surface):
		Movable.__init__(self, given_board_location, given_board, surface, ".\\images\\player.png")
		self.is_alive = True
	
	def handle_event(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_UP:
				self.move_to(self.board_location.up())
			elif event.key == pygame.K_DOWN:
				self.move_to(self.board_location.down())
			elif event.key == pygame.K_LEFT:
				self.move_to(self.board_location.left())
			elif event.key == pygame.K_RIGHT:
				self.move_to(self.board_location.right())
	
	def kill(self):
		self.is_alive = False