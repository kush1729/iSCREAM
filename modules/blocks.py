import pygame
import colors

class Block(pygame.sprite.Sprite):
    def __init__(self, given_board_location, given_board, given_surface):
        pygame.sprite.Sprite.__init__(self)
        
        self.board = given_board
        self.board_location = given_board_location
        self.position = self.board.get_position(self.board_location)
        self.rect = pygame.Rect(0, 0, self.board.square_side, self.board.square_side)
        self.rect.topleft = self.position
        self.surface = given_surface
        self.image = pygame.Surface((self.board.square_side, self.board.square_side))
    
class IceBlock(Block):
    def __init__(self, given_board_location, given_board, given_surface):
        super(IceBlock, self).__init__(given_board_location, given_board, given_surface)
        self.color = colors.LIGHT_BLUE
        pygame.draw.rect(self.image, self.color, pygame.Rect(0, 0, self.board.square_side, self.board.square_side))
        pygame.draw.rect(self.image, colors.BLACK, pygame.Rect(0, 0, self.board.square_side, self.board.square_side), 1)
