import pygame
import colors
from locations import Point

class Board(object):

    def __init__(self, given_grid):
        self.grid = given_grid

    def start(self, player):
        self.player = player

    def is_location_clear(self, location):
        return self.grid[location.y_coordinate][location.x_coordinate] == "empty"
    
    def game_not_suspended(self):
        return self.player.is_alive
    
    def move(self, from_point, to_point):
        self.grid[to_point.y_coordinate][to_point.x_coordinate] = self.grid[from_point.y_coordinate][from_point.x_coordinate]
        self.grid[from_point.y_coordinate][from_point.y_coordinate] = "empty"
    
    def check_if_player_at(self, location):
        return self.grid[location.y_coordinate][location.x_coordinate] == "player"

class GraphicalBoard(Board):
    
    def __init__(self, given_grid, position, height, width, surface):
        super(GraphicalBoard, self).__init__(given_grid)
        self.position = position
        self.height = height
        self.width = width
        self.square_side = width / len(given_grid) #Make this computed
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
        super(GraphicalBoard, self).move(from_point, to_point)
        self.draw_board_rect(from_point)
    
    def draw_board_rect(self, location):
        pygame.draw.rect(self.draw_surface, colors.SNOW, pygame.Rect(location.x_coordinate * self.square_side, location.y_coordinate * self.square_side, self.square_side, self.square_side))
        pygame.draw.rect(self.draw_surface, colors.BLACK, pygame.Rect(location.x_coordinate * self.square_side, location.y_coordinate * self.square_side, self.square_side, self.square_side), 1)