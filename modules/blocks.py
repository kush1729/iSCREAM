import boardpiece
import pygame
import colors

class Block(boardpiece.BoardPiece):
    def __init__(self, given_board_location, given_board, surface, color):

        boardpiece.BoardPiece.__init__(self, given_board_location, given_board, surface)
        self.rect = pygame.Rect(0, 0, self.board.square_side, self.board.square_side)
        self.rect.topleft = self.position
        self.image = pygame.Surface((self.board.square_side, self.board.square_side))
        self.color = color

        self.draw_board_rect()

        self.is_attacked = False

        self.board.reserve_location(self.board_location, self)
        self.draw()
    
    def draw_board_rect(self):
        pygame.draw.rect(self.image, self.color, pygame.Rect(0, 0, self.board.square_side, self.board.square_side))
        pygame.draw.rect(self.image, colors.BLACK, pygame.Rect(0, 0, self.board.square_side, self.board.square_side), 1)
    
    def set_attacked(self):
        self.is_attacked = True

    def kill(self):
        self.board.free_location(self.board_location)

class IceBlock(Block):
    def __init__(self, given_board_location, given_board, surface):
        Block.__init__(self, given_board_location, given_board, surface, colors.LIGHT_BLUE)
    
        
class WallBlock(Block):
    def __init__(self, given_board_location, given_board, surface):
        Block.__init__(self, given_board_location, given_board, surface, colors.MED_BLUE)
