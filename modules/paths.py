import movable
from feeders import PointFeeder
import locations
import blocks

class FixedPathFollower(movable.Movable):

    def __init__(self, given_path):
        self.path = given_path

    def get_path(self):
        feeder = PointFeeder(self.path)
        direction = 1
        while self.board.game_not_suspended():
            new_position = feeder.next(direction)
            if self.board.is_location_clear(self.tolerated_types, new_position):
                yield new_position
            else:
                direction *= -1
                feeder.next(direction)
                yield feeder.next(direction) if self.board.is_location_clear(self.tolerated_types, new_position) else self.board_location


class ChaserAndBreaker(movable.Movable):
    def __init__(self):
        self.current_block = None
    
    def start_melt(self, location):
        self.current_block = self.board[location]
        self.current_block.melt()

    def get_path(self):
        while self.board.game_not_suspended():
            if not self.current_block or self.current_block.dead:
                self.current_block = None

                player_location = self.board.player.board_location
                x_distance = player_location.x_coordinate - self.board_location.x_coordinate
                y_distance = player_location.y_coordinate - self.board_location.y_coordinate

                new_y_location = self.board_location + (0, cmp(y_distance, 0))
                new_y_location_useful = self.board.is_location_clear(self.tolerated_types, new_y_location) and new_y_location != self.board_location

                new_x_location = self.board_location + (cmp(x_distance, 0), 0)
                new_x_location_useful = self.board.is_location_clear(self.tolerated_types, new_x_location) and new_x_location != self.board_location

                if new_y_location_useful and new_x_location_useful:
                    yield new_y_location if abs(y_distance) > abs(x_distance) else new_x_location
                elif new_y_location_useful:
                    yield new_y_location
                elif new_x_location_useful:
                    yield new_x_location
                else:
                    if isinstance(self.board[new_y_location], blocks.Block):
                        self.start_melt(new_y_location)
                    elif isinstance(self.board[new_y_location], blocks.Block):
                        self.start_melt(new_x_location)
                    yield self.board_location
            else:
                yield self.board_location
