import pygame
import player
import locations
import levelparser
import itertools
import events

import colors


class Game(object):

	def __init__(self, screen, board_position, file_name, score_callback, end_callback):
		self.screen = screen

		def fruit_kill_function():
			self.num_fruits -= 1
			score_callback(self.user.score)
			try:
				if self.num_fruits == 0:
					self.next_wave()
			except IndexError:
				end_callback(True)
				self.not_suspended = False
				self.board.game_not_ended = False
		
		def game_kill():
			self.board.game_not_ended = False
		
		def player_dead():
			self.board.game_not_ended = False
			end_callback(False, self.user.score)

		events.add_exit_listener(game_kill)
		self.dataparser = levelparser.Levelparser(file_name, board_position, self.screen, fruit_kill_function, player_dead)
		self.not_suspended = True
		self.num_fruits = 0

	def start(self):
		self.board = self.dataparser.board
		self.user = self.dataparser.player

		self.dataparser.initiate_monsters()
		self.dataparser.initiate_blocks()
		self.next_wave()
		self.board.start(self.user)

		clock = pygame.time.Clock()

		for movable in itertools.chain(self.dataparser.objects[levelparser.PATROLLING_MONSTERS],
			self.dataparser.objects[levelparser.CHASING_MONSTERS],
			self.dataparser.objects[levelparser.FRUIT_WAVES][self.dataparser.wave_number][levelparser.MOVING_FRUITS],
			self.dataparser.objects[levelparser.RANDOM_MONSTERS]):
			movable.activate()

		pygame.display.flip()

	def next_wave(self):
		self.dataparser.next_fruit_wave()
		self.num_fruits = self.dataparser.get_current_wave_size()

	def suspend(self):
		self.not_suspended = False

	def restart(self):
		pass

	def continue_game(self):
		self.not_suspended = True
