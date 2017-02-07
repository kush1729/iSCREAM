import pygame
import player
import locations
import levelparser
import itertools
import events
import time
import threading

import colors


class Game(object):

	def __init__(self, screen, board_position, file_name, score_callback, tick_callback, end_callback):
		self.screen = screen

		self.mutex = threading.Lock()
		self.num_failures = 0

		def fruit_kill_function(fruit):
			decision = False
			self.mutex.acquire()
			try:
				if fruit in self.dataparser.objects[levelparser.FRUIT_WAVES][self.dataparser.wave_number][levelparser.STATIC_FRUITS] \
					or fruit in self.dataparser.objects[levelparser.FRUIT_WAVES][self.dataparser.wave_number][levelparser.MOVING_FRUITS]:
					self.num_fruits -= 1
					score_callback(self.user.score)
					self.num_failures = 0
				else:
					self.num_failures = 1
				if self.num_fruits == 0:
					decision = True
					self.num_fruits = 169
			finally:
				self.mutex.release()
			try:
				if decision:
					self.next_wave()
			except IndexError:
				end_callback(True, self.user.score, time.time() - self.start_time)
				self.not_suspended = False
				self.board.game_not_ended = False
		
		def game_kill():
			self.board.game_not_ended = False
			events.remove_keypress_listener(pygame.K_p, self.pause_toggle)
			events.remove_exit_listener(game_kill)
		
		def player_dead():
			self.board.game_not_ended = False
			end_callback(False, self.user.score, time.time() - self.start_time)

		events.add_exit_listener(game_kill)
		events.add_keypress_listener(pygame.K_p, self.pause_toggle)
		self.tick_callback = tick_callback
		self.dataparser = levelparser.Levelparser(file_name, board_position, self.screen, fruit_kill_function, player_dead)
		self.not_suspended = True
		self.num_fruits = 0

	def start(self):
		self.start_time = time.time()

		def ticker():
			while self.board.game_not_ended:
				time.sleep(1)
				self.tick_callback(time.time() - self.start_time)
		threading.Timer(0, ticker).start()

		self.board = self.dataparser.board
		self.user = self.dataparser.player

		self.dataparser.initiate_blocks()
		self.next_wave()
		self.board.start(self.user)

		pygame.display.flip()

	def next_wave(self):
		if self.dataparser.wave_number != -1:
			for monster in itertools.chain(
				self.dataparser.objects[levelparser.MONSTER_WAVES][self.dataparser.wave_number][levelparser.PATROLLING_MONSTERS],
				self.dataparser.objects[levelparser.MONSTER_WAVES][self.dataparser.wave_number][levelparser.CHASING_MONSTERS],
				self.dataparser.objects[levelparser.MONSTER_WAVES][self.dataparser.wave_number][levelparser.RANDOM_MONSTERS]):
				monster.kill()
		self.dataparser.next_wave()
		self.num_fruits = self.dataparser.get_current_wave_size() - self.num_failures
		self.activate_movables()
	
	def activate_movables(self):
		for movable in itertools.chain(
			self.dataparser.objects[levelparser.FRUIT_WAVES][self.dataparser.wave_number][levelparser.MOVING_FRUITS],
			self.dataparser.objects[levelparser.MONSTER_WAVES][self.dataparser.wave_number][levelparser.PATROLLING_MONSTERS],
			self.dataparser.objects[levelparser.MONSTER_WAVES][self.dataparser.wave_number][levelparser.CHASING_MONSTERS],
			self.dataparser.objects[levelparser.MONSTER_WAVES][self.dataparser.wave_number][levelparser.RANDOM_MONSTERS]):
			movable.activate()

	def pause_toggle(self):
		if self.board.game_not_paused:
			self.pause()
		else:
			self.resume()

	def pause(self):
		self.board.game_not_paused = False

	def resume(self):
		self.board.game_not_paused = True
		self.activate_movables()
