import pygame
import events
import fonts
class Button(object):
    def __init__(self, text, rect, color, text_color, callback, screen):
        self.rect = rect
        self.image = pygame.Surface((rect.width, rect.height))
        self.callback = callback
        self.screen = screen
        text = fonts.SMALL.render(text, True, text_color)
        text_rect = text.get_rect()
        text_rect.center = self.image.get_rect().center
        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, rect.width, rect.height))
        self.image.blit(text, text_rect)
    
    def display(self):
        self.screen.blit(self.image, self.rect)
        pygame.display.update(self.rect)
        events.add_click_listener(self, self.callback)
    
    def clean(self):
        events.remove_click_listener(self)