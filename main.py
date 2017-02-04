import sys
sys.path.append('.\\modules\\')
import time
import threading

import pygame
import game
import colors
import events
import button

pygame.init()

screen = pygame.display.set_mode((595, 665))
screen.fill(colors.WHITE)
for i in xrange(17):
    update_rect_1 = pygame.Rect(35 * i, 0, 35, 35)
    update_rect_2 = pygame.Rect(35 * i, 560, 35, 35)
    pygame.draw.rect(screen, colors.MED_BLUE, update_rect_1)
    pygame.draw.rect(screen, colors.MED_BLUE, update_rect_2)
    pygame.draw.rect(screen, colors.BLACK, update_rect_1, 1)
    pygame.draw.rect(screen, colors.BLACK, update_rect_2, 1)
for i in xrange(1, 16):
    update_rect_1 = pygame.Rect(0, 35 * i, 35, 35)
    update_rect_2 = pygame.Rect(560, 35 * i, 35, 35)
    pygame.draw.rect(screen, colors.MED_BLUE, update_rect_1)
    pygame.draw.rect(screen, colors.MED_BLUE, update_rect_2)
    pygame.draw.rect(screen, colors.BLACK, update_rect_1, 1)
    pygame.draw.rect(screen, colors.BLACK, update_rect_2, 1)

def score_cb(score):
    text = pygame.font.SysFont('comicsansms', 20).render(str(score), True, colors.BLACK)
    textRect = text.get_rect()
    textRect.bottomleft = (0, 665)
    
    screen.fill(colors.WHITE, pygame.Rect(0, 595 + 40, 150, 40))
    screen.blit(text, textRect)
    
    pygame.display.update(pygame.Rect(0, 595 + 40, 150, 40))

def end_callback(user_won, score):
    def clear_screen():
        screen.fill(colors.WHITE)
        if user_won:
            text = pygame.font.SysFont('comicsansms', 20).render('You won! Your', True, colors.BLACK)
        else:
            text = pygame.font.SysFont('comicsansms', 20).render('You lost!', True, colors.BLACK)
        textRect = text.get_rect()
        textRect.center = screen.get_rect().center
        screen.blit(text, textRect)
        pygame.display.flip()

        def say_hello():
            print "hello"

        button.Button(pygame.Rect(0, 0, 50, 50), colors.ORANGE, say_hello, screen)

    a = threading.Timer(1, clear_screen)
    a.start()

pygame.display.flip()

game = game.Game(screen, (35, 35), 'level1.level.json', score_cb, end_callback)
game.start()

events.start()