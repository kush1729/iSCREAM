from board import Board
from locations import Point

import pygame

class Movable(pygame.sprite.Sprite):
    def __init__(self, given_board_location, given_image_string, given_board):
        pygame.sprite.Sprite.__init__(self)

        #The board on which the player is playing
        self.board = given_board

        #Location on the board
        self.board_location = given_board_location

        #Must be implemented as a pygame Sprite
        self.position = self.board.get_position(self.board_location)
        self.image = pygame.image.load(given_image_string).convert()
        self.rect = self.image.get_rect()

    def move_to(self, new_location):
        self.board.move(self.board_location, new_location)
        self.board_location = new_location
    
    def update(self):
        self.position = self.board.get_position(self.board_location)
        self.rect.topleft = self.position