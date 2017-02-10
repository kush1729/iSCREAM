"""
Welcome to iSCREAM!
This is a game about an icecream that wants to eat fruits and
survive monsters.
Launch by either double-clicking on main.py, or by launching from command line as:
python main.py
"""


import sys
sys.path.append('.\\modules\\') 

import pygame
pygame.init()

import events
from page import *

screen = pygame.display.set_mode((595, 665))
pygame.display.set_caption('iSCREAM')
pygame.display.set_icon(pygame.image.load('.\\images\\icon.jpg').convert())

introduction_page = IntroductionPage(screen)
instruction_page = InstructionPage(screen)
level_page = LevelPage(screen)
game_page = GamePage(screen)
results_page = ResultsPage(screen)

introduction_page.level_page = level_page
introduction_page.instruction_page = instruction_page

instruction_page.level_page = level_page

level_page.game_page = game_page

game_page.introduction_page = introduction_page
game_page.results_page = results_page

results_page.game_page = game_page
results_page.introduction_page = introduction_page

introduction_page.display()

events.start()