import pygame
import fonts
import colors
import button
import json
import game
import threading
import events

class Page(object):
	def __init__(self, screen):
		self.screen = screen
		self.buttons = []
		self.texts = []
		self.screen_horizontal_center = self.screen.get_rect().center[0]

	def display(self, caption="iSCREAM"):
		self.screen.fill(colors.WHITE)
		for text, text_rect in self.texts:
			self.screen.blit(text, text_rect)
		for button in self.buttons:
			button.display()
		pygame.display.flip()
	
	def clean(self):
		for button in self.buttons:
			button.clean()

class IntroductionPage(Page):
	def __init__(self, screen):
		Page.__init__(self, screen)
		welcome_to = fonts.MEDIUM.render('WELCOME TO', True, colors.LIGHT_RED)
		welcome_to_rect = welcome_to.get_rect()
		welcome_to_rect.center = (self.screen_horizontal_center, 100)

		self.texts.append((welcome_to, welcome_to_rect))

		iscream = fonts.X_LARGE.render('iSCREAM', True, colors.CHOCOLATE)
		iscream_rect = iscream.get_rect()
		iscream_rect.center = (self.screen_horizontal_center, 275)

		self.texts.append((iscream, iscream_rect))

		def goto_play():
			self.clean()
			self.level_page.display()
		
		play = button.Button(
			'PLAY',
			pygame.Rect(50, 450, 125, 125),
			colors.GREEN,
			colors.BLACK,
			goto_play,
			self.screen
		)

		self.buttons.append(play)

		def goto_instructions():
			self.clean()
			self.instruction_page.display()

		instructions = button.Button(
			'INSTRUCTIONS',
			pygame.Rect((self.screen.get_rect().width - 175) / 2, 450, 175, 125),
			colors.ORANGE,
			colors.BLACK,
			goto_instructions,
			self.screen
		)

		self.buttons.append(instructions)

		def quitter():
			events.stop()

		quit = button.Button(
			'QUIT',
			pygame.Rect((self.screen.get_rect().width - 175), 450, 125, 125),
			colors.RED,
			colors.BLACK,
			quitter,
			self.screen
		)

		self.buttons.append(quit)
	
	def display(self):
		Page.display(self, "Welcome to iSCREAM")

class LevelPage(Page):
	def __init__(self, screen):
		Page.__init__(self, screen)

		heading = fonts.MED_LARGE.render("CHOOSE LEVEL", True, colors.CHOCOLATE)
		heading_rect = heading.get_rect()
		heading_rect.center = (self.screen_horizontal_center, 65)

		self.texts.append((heading, heading_rect))

		with open('.\\levels\\gamelevels.json') as game_file:
			level_files = json.loads(game_file.read())['gameLevels']

		level_button_margin_top = 150
		level_button_margin_left = 25
		num_level_buttons_in_row = 5
		level_button_width = 94
		level_button_height = 80
		gap = 25

		def level_navigator(level_file):
			def nav():
				self.clean()
				self.game_page.display(level_file)
			return nav
		
		for level_number, level_file in enumerate(level_files):
			level_button = button.Button(
				'LEVEL {level_number}'.format(level_number=level_number + 1),
				pygame.Rect(
					level_button_margin_left + ((level_number) % num_level_buttons_in_row) * (gap + level_button_width),
					level_button_margin_top + ((level_number) / 5) * (level_button_height + gap),
					level_button_width,
					level_button_height
				),
				colors.GREEN,
				colors.BLACK,
				level_navigator(level_file),
				self.screen
			)
			self.buttons.append(level_button)
	
	def display(self):
		Page.display(self, "Select Level")

class GamePage(Page):
	def __init__(self, screen):
		Page.__init__(self, screen)
		self.image = pygame.Surface((self.screen.get_rect().width, self.screen.get_rect().height), pygame.SRCALPHA)

		for i in xrange(17):
			update_rect_1 = pygame.Rect(35 * i, 0, 35, 35)
			update_rect_2 = pygame.Rect(35 * i, 560, 35, 35)
			self.draw_border_rect(update_rect_1)
			self.draw_border_rect(update_rect_2)

		for i in xrange(1, 16):
			update_rect_1 = pygame.Rect(0, 35 * i, 35, 35)
			update_rect_2 = pygame.Rect(560, 35 * i, 35, 35)
			self.draw_border_rect(update_rect_1)
			self.draw_border_rect(update_rect_2)
	
	def draw_border_rect(self, update_rect):
		pygame.draw.rect(self.image, colors.MED_BLUE, update_rect)
		pygame.draw.rect(self.image, colors.BLACK, update_rect, 1)

	def display(self, level_file):
		self.level_file = level_file

		def score_cb(score):
			text = fonts.SMALL.render(str(score), True, colors.BLACK)
			textRect = text.get_rect()
			textRect.bottomleft = (0, 665)
			
			self.screen.fill(colors.WHITE, pygame.Rect(0, 595 + 40, 150, 40))
			self.screen.blit(text, textRect)
			
			pygame.display.update(pygame.Rect(0, 595 + 40, 150, 40))
		
		def end_callback(user_won, score, time):
			def clear_screen():
				self.results_page.display(user_won, score, time, level_file)
				self.clean()
			
			clear_scheduler = threading.Timer(1, clear_screen)
			clear_scheduler.start()
		
		Page.display(self)
		self.screen.blit(self.image, (0, 0))
		pygame.display.flip()

		current_game = game.Game(self.screen, (35, 35), level_file, score_cb, end_callback)
		current_game.start()

class ResultsPage(Page):
	def __init__(self, screen):
		Page.__init__(self, screen)
		
		def goto_play_again():
			self.clean()
			self.game_page.display(self.last_level_file)
		
		play_again = button.Button(
			'PLAY AGAIN',
			pygame.Rect(50, 450, 125, 125),
			colors.GREEN,
			colors.BLACK,
			goto_play_again,
			self.screen
		)

		self.buttons.append(play_again)

		def goto_introduction():
			self.clean()
			self.introduction_page.display()

		main_menu = button.Button(
			'MAIN MENU',
			pygame.Rect((self.screen.get_rect().width - 175) / 2, 450, 175, 125),
			colors.ORANGE,
			colors.BLACK,
			goto_introduction,
			self.screen
		)

		self.buttons.append(main_menu)

		def quitter():
			events.stop()

		quit = button.Button(
			'QUIT',
			pygame.Rect((self.screen.get_rect().width - 175), 450, 125, 125),
			colors.RED,
			colors.BLACK,
			quitter,
			self.screen
		)

		self.buttons.append(quit)
	
	def display(self, user_won, score, time, level_file):
		self.last_level_file = level_file
		self.texts = []
		
		win_message = fonts.LARGE.render('YOU WON' if user_won else 'YOU LOST', True, colors.ORANGE)
		win_message_rect = win_message.get_rect()
		win_message_rect.center = (self.screen_horizontal_center, 100)

		self.texts.append((win_message, win_message_rect))

		time_taken = fonts.MEDIUM.render(
			'TIME TAKEN: %d:%02d' % (int(time) // 60, int(time) % 60),
			True,
			colors.CHOCOLATE
		)
		time_taken_rect = time_taken.get_rect()
		time_taken_rect.center = (self.screen_horizontal_center, 225)

		self.texts.append((time_taken, time_taken_rect))

		score = fonts.MEDIUM.render(
			'YOUR SCORE: %d' % (score),
			True,
			colors.CHOCOLATE
		)
		score_rect = score.get_rect()
		score_rect.center = (self.screen_horizontal_center, 335)

		self.texts.append((score, score_rect))

		Page.display(self)


class InstructionPage(Page):
	def __init__(self, screen):
		Page.__init__(self, screen)
		instructions = '''
		AVOID THE MONSTERS AND EAT ALL THE FRUITS
		TO COMPLETE THE LEVEL!

		USE THE ARROW KEYS TO NAVIGATE
		USE THE SPACEBAR TO SHOOT AND BREAK ICE
		PRESS 'P' TO PAUSE
		'''

		heading = fonts.MED_LARGE.render('INSTRUCTIONS', True, colors.CHOCOLATE)
		heading_rect = heading.get_rect()
		heading_rect.center = (self.screen_horizontal_center, 65)

		self.texts.append((heading, heading_rect))

		instructions_height = 190

		for line_index, line in enumerate(instructions.strip().split('\n')):
			line_surface = fonts.SMALL.render(line.strip(), True, colors.MED_BLUE)
			line_rect = line_surface.get_rect()
			line_rect.center = (self.screen_horizontal_center, instructions_height + line_index * 40)
			self.texts.append((line_surface, line_rect))
		
		def goto_play():
			self.clean()
			self.level_page.display()
		
		play = button.Button(
			'PLAY',
			pygame.Rect(50, 500, 175, 75),
			colors.GREEN,
			colors.BLACK,
			goto_play,
			self.screen
		)

		self.buttons.append(play)

		def quitter():
			events.stop()

		quit = button.Button(
			'QUIT',
			pygame.Rect(self.screen.get_rect().width - 225, 500, 175, 75),
			colors.RED,
			colors.BLACK,
			quitter,
			self.screen
		)

		self.buttons.append(quit)
	
	def display(self):
		Page.display(self, "Instructions")


if __name__ == '__main__':
	import events
	pygame.init()
	screen = pygame.display.set_mode((595, 665))
	introduction_page = IntroductionPage(screen)
	instruction_page = InstructionPage(screen)
	level_page = LevelPage(screen)
	game_page = GamePage(screen)
	results_page = ResultsPage(screen)

	introduction_page.level_page = level_page
	introduction_page.instruction_page = instruction_page

	instruction_page.level_page = level_page

	level_page.game_page = game_page

	game_page.results_page = results_page

	results_page.game_page = game_page
	results_page.introduction_page = introduction_page

	introduction_page.display()

	#b.display('level1.level.json')
	events.start()
