import movables
import threading
import time
from feeders import PointFeeder

class Monster(movables.Movable):
    pass

class PatrollingMonster(Monster):

    def __init__(self, given_board_location, given_image_string, given_board, given_path):
        Monster.__init__(self, given_board_location, given_image_string, given_board)

        self.path = given_path

    def activate(self):
        self.point_feed = self.get_path()
        def mover():
            for location in self.point_feed:
                time.sleep(0.1)
                self.move_to(location)
        move_scheduler = threading.Timer(0, mover)
        move_scheduler.start()
    
    def get_path(self):
        feeder = PointFeeder(self.path)
        direction = 1
        while self.board.game_not_suspended():
            new_position = feeder.next(direction)
            if self.board.is_location_clear(new_position):
                yield new_position
            else:
                direction *= -1
                feeder.next(direction)
                yield feeder.next(direction)

class ChasingMonster(Monster):
    
    def activate(self):
        raise NotImplementedError

if __name__ == '__main__':
    from board import GraphicalBoard
    from locations import Point
    import pygame
    pygame.init()
    pygame.display.set_mode((250, 250))
    monster = PatrollingMonster(Point(0, 0),
    '.\\images\\apple.jpg',
    GraphicalBoard([], (0, 0), 250, 250),
    [Point(0, 0), Point(1, 0), Point(1, 1), Point(0, 1)])
    monster.activate()