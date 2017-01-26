import boardpiece
import pygame
import fixedpath

class Fruit(boardpiece.BoardPiece):
    def __init__(self, given_board_location, given_board, surface, given_score, given_image_string):
        boardpiece.BoardPiece.__init__(self, given_board_location, given_board, surface)
        self.score = given_score

        self.image = pygame.image.load(given_image_string).convert()
        self.rect = self.image.get_rect()

        self.rect.topleft = self.board.get_position(self.board_location)
        self.draw()

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