import boardpiece
import pygame
import colors
import time
import threading

class Block(boardpiece.BoardPiece):

    def __init__(self, given_board_location, given_board, surface, color):

        boardpiece.BoardPiece.__init__(
            self, given_board_location, given_board, surface)
        self.rect = pygame.Rect(
            0, 0, self.board.square_side, self.board.square_side)
        self.rect.topleft = self.position
        self.image = pygame.Surface(
            (self.board.square_side, self.board.square_side))
        self.color = color

        self.draw_board_rect()

        self.dead = False

        self.board.reserve_location(self.board_location, self)
        self.draw()

    def draw_board_rect(self):
        pygame.draw.rect(self.image, self.color, pygame.Rect(
            0, 0, self.board.square_side, self.board.square_side))
        pygame.draw.rect(self.image, colors.BLACK, pygame.Rect(
            0, 0, self.board.square_side, self.board.square_side), 1)
        self.draw()

    def set_attacked(self):
        self.is_attacked = True

    def kill(self):
        self.board.free_location(self.board_location)
        self.dead = True
    
    def melt(self):
        def melt_flasher():
            color_index = 0
            flash_colors = [colors.RED, self.color]

            for i in xrange(50):
                if not self.dead:
                    time.sleep(0.1)
                    self.color = flash_colors[color_index]
                    color_index = (color_index + 1) % 2
                    self.draw_board_rect()
                else:
                    break
            
            self.kill()
        melt_scheduler = threading.Timer(0, melt_flasher)
        melt_scheduler.start()


class IceBlock(Block):

    def __init__(self, given_board_location, given_board, surface):
        Block.__init__(self, given_board_location,
                       given_board, surface, colors.LIGHT_BLUE)
        self.frozen = True


class WallBlock(Block):

    def __init__(self, given_board_location, given_board, surface):
        Block.__init__(self, given_board_location,
                       given_board, surface, colors.MED_BLUE)
