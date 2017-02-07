import pygame
import colors
import player
import fruits
import blocks
from threading import Lock
from locations import Point


class Board(object):

    def __init__(self, width, height):
        self.grid = [[None for i in xrange(width)] for j in xrange(width)]
        self.moving = False
        self.game_not_paused = True
        self.game_not_ended = True
        self.mutex = Lock()

    def __contains__(self, location):
        return 0 <= location.y_coordinate < len(self.grid) and 0 <= location.x_coordinate < len(self.grid[0])

    def __getitem__(self, location):
        return self.grid[location.y_coordinate][location.x_coordinate]

    def __setitem__(self, location, value):
        self.grid[location.y_coordinate][location.x_coordinate] = value

    def start(self, player):
        self.player = player

    def is_location_clear(self, tolerated, location):
        try:
            if location in self:
                return self[location] is None or any(
                    isinstance(self[location], board_piece_type) for board_piece_type in tolerated)\
                    if not isinstance(self[location], fruits.Fruit)\
                    else not self[location].frozen
            else:
                return False
        except IndexError:
            return False

    def reserve_location(self, location, boardpiece):
        self[location] = boardpiece

    def game_not_suspended(self):
        return self.game_not_ended and self.game_not_paused

    def move(self, from_point, to_point):
        if from_point != to_point:
            self[to_point] = self[from_point]
            self[from_point] = None

    def is_empty(self, location):
        return self[location] is None

    def is_of_type(self, location, type):
        return isinstance(self[location], type)

    def is_player_at(self, location):
        return self.is_of_type(location, player.Player)

    def free_location(self, location):
        self[location] = None

    def is_frozen(self, location):
        return self[location].frozen if self[location] is not None else False


class GraphicalBoard(Board):

    def __init__(self, board_width, board_height, position, surface):
        Board.__init__(self, board_width, board_height)
        self.position = position
        self.square_side = 35
        self.draw_surface = surface
        self.draw()

    def draw(self):
        for row_num in xrange(len(self.grid)):
            for col_num in xrange(len(self.grid[0])):
                self.draw_board_rect(Point(row_num, col_num))

    def get_position(self, location):
        X = 0
        Y = 1
        return (self.position[X] + location.x_coordinate * self.square_side,
                self.position[Y] + location.y_coordinate * self.square_side)

    def move(self, from_point, to_point):
        Board.move(self, from_point, to_point)
        self.draw_board_rect(from_point)

    def free_location(self, location):
        Board.free_location(self, location)
        self.draw_board_rect(location)

    def draw_board_rect(self, location):
        update_rect = pygame.Rect(self.position[0] + location.x_coordinate * self.square_side,
                                  self.position[1] + location.y_coordinate * self.square_side,
                                  self.square_side, self.square_side)
        pygame.draw.rect(self.draw_surface, colors.SNOW, update_rect)
        pygame.draw.rect(self.draw_surface, colors.BLACK, update_rect, 1)
        pygame.display.update(update_rect)

    def freeze(self, location):
        if isinstance(self[location], fruits.Fruit):
            self[location].freeze()
        else:
            self[location] = blocks.IceBlock(location, self, self.draw_surface)

    def unfreeze(self, location):
        if isinstance(self[location], fruits.Fruit):
            self[location].unfreeze()
        else:
            self[location].kill()
