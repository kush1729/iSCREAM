import movable
import paths
import threading
import time
import player
import fruits

monsters_delay = 0.05

class Monster(movable.Movable):

    def __init__(self, given_board_location, given_board, screen, given_image_string):
        movable.Movable.__init__(
            self, given_board_location, given_board, screen, given_image_string)
        self.tolerated_types = (player.Player,)
        self.picked_fruit = None

    def activate(self):
        self.point_feed = self.get_path()

        def mover():
            while True:
                time.sleep(self.delay)
                try:
                    self.board.mutex.acquire()
                    try:
                        current_location = self.board_location
                        location = self.point_feed.next()
                        next_picked_fruit = None
                        if isinstance(self.board[location], fruits.Fruit):
                            next_picked_fruit = self.board[location]
                        elif self.board.is_player_at(location):
                            self.board.player.kill()
                        self.move_to(location)
                        if self.picked_fruit:
                            self.board[current_location] = self.picked_fruit
                            self.picked_fruit.draw()
                        self.picked_fruit = next_picked_fruit
                    finally:
                        self.board.mutex.release()
                except StopIteration:
                    break
        move_scheduler = threading.Timer(0, mover)
        move_scheduler.start()


class PatrollingMonster(paths.FixedPathFollower, Monster):

    def __init__(self, given_board_location, given_board, surface, given_path):
        Monster.__init__(self, given_board_location, given_board,
                         surface, ".\\images\\patrolling.png")
        paths.FixedPathFollower.__init__(self, given_path)

        self.delay = monsters_delay


class ChasingMonster(paths.ChaserAndBreaker, Monster):

    def __init__(self, given_board_location, given_board, surface):
        Monster.__init__(self, given_board_location, given_board,
                         surface, ".\\images\\chasing.png")
        paths.ChaserAndBreaker.__init__(self)

        self.delay = monsters_delay


class RandomMonster(paths.RandomWalker, Monster):

    def __init__(self, given_board_location, given_board, surface):
        Monster.__init__(self, given_board_location,
                         given_board, surface, ".\\images\\random.png")

        self.delay = monsters_delay
