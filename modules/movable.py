import boardpiece

import pygame

class Movable(boardpiece.BoardPiece):
    def __init__(self, given_board_location, given_board, surface, given_image_string):
        boardpiece.BoardPiece.__init__(self, given_board_location, given_board, surface)
        
        self.image = pygame.image.load(given_image_string).convert()
        self.rect = self.image.get_rect()
        self.update()

        self.draw()

    def move_to(self, new_location):
        while self.board.moving:
            print 1
        self.board.moving = True
        self.board.move_if_clear(self.board_location, new_location)
        self.board.moving = False
        self.board_location = new_location
        self.update()
        self.draw()
    
    def update(self):
        self.position = self.board.get_position(self.board_location)
        self.rect.topleft = self.position
        self.draw()
        pygame.display.update(self.rect)