import movable
import fixedpath
import threading
import time

class Monster(movable.Movable):
    def activate(self):
        self.point_feed = self.get_path()
        def mover():
            for location in self.point_feed:
                time.sleep(self.delay)
                self.move_to(location)
        move_scheduler = threading.Timer(0, mover)
        move_scheduler.start()

class PatrollingMonster(fixedpath.FixedPathFollower, Monster):

    def __init__(self, given_board_location, given_board, surface, given_path):
        Monster.__init__(self, given_board_location, given_board, surface, ".\\images\\chasing.png")
        fixedpath.FixedPathFollower.__init__(self, given_path)

        self.delay = 0.1

class ChasingMonster(Monster):
    pass