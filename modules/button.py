import pygame
import events
import fonts


class Button(object):

	def __init__(self, text, rect, color, second_color, text_color, callback, screen):
		self.rect = rect
		self.image = pygame.Surface((rect.width, rect.height))
		self.callback = callback
		self.screen = screen
		text = fonts.SMALL.render(text, True, text_color)
		text_rect = text.get_rect()
		text_rect.center = self.image.get_rect().center
		pygame.draw.rect(self.image, color, pygame.Rect(
			0, 0, rect.width, rect.height))
		self.image.blit(text, text_rect)
		self.first_image = self.image
		self.second_image = pygame.Surface((rect.width, rect.height))
		pygame.draw.rect(self.second_image, second_color, pygame.Rect(
			0, 0, rect.width, rect.height))
		self.second_image.blit(text, text_rect)
		
	def onhover(self):
		self.screen.blit(self.second_image, self.rect)
		pygame.display.update(self.rect)
			
	def onleave(self):
		self.screen.blit(self.first_image, self.rect)
		pygame.display.update(self.rect)

	def display(self):
		self.screen.blit(self.image, self.rect)
		pygame.display.update(self.rect)
		events.add_click_listener(self, self.callback)
		events.add_mouseenter_listener(self, self.onhover)
		events.add_mouseleave_listener(self, self.onleave)

	def clean(self):
		events.remove_click_listener(self)
		events.remove_mouseenter_listener(self)
		events.remove_mouseleave_listener(self)
