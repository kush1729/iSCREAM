import pygame


class BoardPiece(pygame.sprite.Sprite):

    def __init__(self, given_board_location, given_board, screen, collide_resolver):
        pygame.sprite.Sprite.__init__(self)

        self.board = given_board
        self.board_location = given_board_location

        if not self.board.is_empty(self.board_location):
            collide_resolver(self.board_location)
        else:
            self.board.reserve_location(self.board_location, self)

        self.position = self.board.get_position(self.board_location)
        self.screen = screen

        self.frozen = False

    def draw(self):
        self.screen.blit(self.image, self.position)
        pygame.display.update(self.rect)
