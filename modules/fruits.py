import boardpiece
import pygame
import fixedpath
import colors

class Fruit(boardpiece.BoardPiece):
    def __init__(self, given_board_location, given_board, surface, given_score, given_image_string):
        boardpiece.BoardPiece.__init__(self, given_board_location, given_board, surface)
        self.score = given_score

        self.original_image = pygame.image.load(given_image_string).convert_alpha()
        self.image = pygame.Surface([self.board.square_side, self.board.square_side], pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.rect.topleft = self.board.get_position(self.board_location)
        self.draw()

        self.frozen = False
    
    def freeze(self):
        self.frozen = True
        self.draw(colors.LIGHT_BLUE)
    
    def unfreeze(self):
        self.frozen = False
        self.draw(colors.SNOW)
    
    def draw(self, background_color=colors.SNOW):
        update_rect = pygame.Rect((0, 0), (self.board.square_side, self.board.square_side))

        pygame.draw.rect(self.image, background_color, update_rect)
        self.image.blit(self.original_image, (1, 1))
        pygame.draw.rect(self.image, colors.BLACK, update_rect, 1)

        target_rect = pygame.Rect(update_rect)
        self.screen.blit(self.image, self.position)
        pygame.display.update(pygame.Rect(self.position, (self.board.square_side, self.board.square_side)))

class Strawberry(Fruit, fixedpath.FixedPathFollower):
    def __init__(self, given_board_location, given_board, surface, given_score, given_path):
        Fruit.__init__(self, given_board_location, given_board, surface, 200, ".\\images\\strawberry.png")
        fixedpath.FixedPathFollower.__init__(given_path)

class Apple(Fruit):
    def __init__(self, given_board_location, given_board, surface):
        Fruit.__init__(self, given_board_location, given_board, surface, 25, ".\\images\\apple.jpg")

class Banana(Fruit):
    def __init__(self, given_board_location, given_board, surface):
        Fruit.__init__(self, given_board_location, given_board, surface, 50, ".\\images\\banana.png")

class Grapes(Fruit):
    def __init__(self, given_board_location, given_board, surface):
        Fruit.__init__(self, given_board_location, given_board, surface, 100, ".\\images\\grapes.png")