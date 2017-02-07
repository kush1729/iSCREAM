import boardpiece

import pygame

from threading import Lock


class Movable(boardpiece.BoardPiece):

    def __init__(self, given_board_location, given_board, surface, collide_resolver, given_image_string):
        boardpiece.BoardPiece.__init__(
            self, given_board_location, given_board, surface, collide_resolver)

        self.image = pygame.Surface(
            [self.board.square_side, self.board.square_side], pygame.SRCALPHA)
        self.image.blit(pygame.image.load(given_image_string).convert_alpha(), (1, 1))
        self.rect = self.image.get_rect()

        self.update()
        self.draw()

    def move_to(self, new_location):
        if self.board.is_location_clear(self.tolerated_types, new_location):
            self.board.move(self.board_location, new_location)
            self.board_location = new_location
        self.update()
        self.draw()

    def update(self):
        self.position = self.board.get_position(self.board_location)
        self.rect.topleft = self.position
        self.draw()
        pygame.display.update(self.rect)
