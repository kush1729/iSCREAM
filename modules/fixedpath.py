import movable
from feeders import PointFeeder

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
                yield feeder.next(direction)