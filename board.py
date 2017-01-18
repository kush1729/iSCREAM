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
    
    def __init__(self, given_grid, position, height, width):
        super(GraphicalBoard, self).__init__(given_grid)
        self.position = position
        self.height = height
        self.width = width
        self.square_side = 50 #Make this computed
    
    def get_position(self, location):
        X = 0
        Y = 1
        return (self.position[X] + location.x_coordinate * self.square_side + self.square_side / 2,
        self.position[Y] + location.y_coordinate * self.square_side + self.square_side / 2)