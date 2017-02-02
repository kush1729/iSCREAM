import movable
import paths
import threading
import time
import player

mutex = threading.Lock()


class Monster(movable.Movable):

    def __init__(self, given_board_location, given_board, screen, given_image_string):
        movable.Movable.__init__(
            self, given_board_location, given_board, screen, given_image_string)
        self.tolerated_types = (player.Player,)

    def activate(self):
        self.point_feed = self.get_path()

        def mover():
            while True:
                time.sleep(self.delay)
                try:
                    mutex.acquire()
                    try:
                        location = self.point_feed.next()
                        if self.board.is_player_at(location):
                            self.board.player.kill()
                        self.move_to(location)
                    finally:
                        mutex.release()
                except StopIteration:
                    break
        move_scheduler = threading.Timer(0, mover)
        move_scheduler.start()


class PatrollingMonster(paths.FixedPathFollower, Monster):

    def __init__(self, given_board_location, given_board, surface, given_path):
        Monster.__init__(self, given_board_location, given_board,
                         surface, ".\\images\\patrolling.png")
        paths.FixedPathFollower.__init__(self, given_path)

        self.delay = 0.1


class ChasingMonster(paths.ChaserAndBreaker, Monster):

    def __init__(self, given_board_location, given_board, surface):
        Monster.__init__(self, given_board_location, given_board,
                         surface, ".\\images\\chasing.png")
        paths.ChaserAndBreaker.__init__(self)
        
        self.delay = 1

