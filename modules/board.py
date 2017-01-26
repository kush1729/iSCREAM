import pygame
import colors
import player
from locations import Point

class Board(object):

    def __init__(self, width, height):
        self.grid = [[None for i in xrange(width)] for j in xrange(width)]
        self.moving = False

    def start(self, player):
        self.player = player

    def is_location_clear(self, location):
        try:
            if location.x_coordinate >= 0 and location.y_coordinate >= 0:
                return self.grid[location.y_coordinate][location.x_coordinate] == None
            else:
                return False
        except IndexError:
            return False

    def reserve_location(self, location, boardpiece):
        self.grid[location.y_coordinate][location.x_coordinate] = boardpiece
    
    def game_not_suspended(self):
        return self.player.is_alive
    
    def move(self, from_point, to_point):
        self.grid[to_point.y_coordinate][to_point.x_coordinate] = self.grid[from_point.y_coordinate][from_point.x_coordinate]
        self.grid[from_point.y_coordinate][from_point.x_coordinate] = None
    
    def move_if_clear(self, from_point, to_point):
        self.moving = True
        if self.is_location_clear(to_point):
            self.move(from_point, to_point)
        self.moving = False
    
    def check_if_player_at(self, location):
        return isinstance(self.grid[location.y_coordinate][location.x_coordinate], player.Player)

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
    
    def draw_board_rect(self, location):
        update_rect = pygame.Rect(self.position[0] + location.x_coordinate * self.square_side,
            self.position[1] + location.y_coordinate * self.square_side,
            self.square_side, self.square_side)
        pygame.draw.rect(self.draw_surface, colors.SNOW, update_rect)
        pygame.draw.rect(self.draw_surface, colors.BLACK, update_rect, 1)
        pygame.display.update(update_rect)