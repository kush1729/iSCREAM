import movable
import paths
import threading
import time
import player
import fruits
import blocks

class Monster(movable.Movable):

    def __init__(self, given_board_location, given_board, screen, given_image_string):
        self.picked_fruit = None
        def collide_resolver(location):
            if self.board.is_of_type(location, blocks.Block):
                self.board[location].kill()
                self.board.reserve_location(location, self)
            elif self.board.is_of_type(location, player.Player):
                self.board[location].kill()
                self.board.reserve_location(location, self)
            elif self.board.is_of_type(location, fruits.Fruit):
                self.pick(self.board[location])
                self.board.reserve_location(location, self)
        
        movable.Movable.__init__(
            self, given_board_location, given_board, screen, collide_resolver, given_image_string)
        self.tolerated_types = (player.Player, fruits.Fruit)
        self.delay = 0.07
        self.is_alive = True
        self.point_feed = self.get_path()

    def activate(self):
        def mover():
            while self.is_alive and self.board.game_not_suspended():
                time.sleep(self.delay)
                try:
                    self.board.mutex.acquire()
                    try:
                        # current_location = self.board_location
                        # location = self.point_feed.next()
                        # next_picked_fruit = self.board[location] if location != current_location and isinstance(self.board_location, fruits.Fruit) else None
                        # update = True

                        # if self.board.is_player_at(location):
                        #     self.board.player.kill()
                        # if self.picked_fruit and location != current_location:
                        #     if isinstance(self.board[location], fruits.Fruit):
                        #         next_picked_fruit = self.board[location]
                        # elif self.picked_fruit:
                        #     update = False
                        #     next_picked_fruit = self.picked_fruit
                        # self.move_to(location)
                        # self.unpick(self.picked_fruit, current_location, update)

                        # self.pick(next_picked_fruit)

                        ###

                        current_location = self.board_location
                        location = self.point_feed.next()
                        next_picked_fruit = None
                        should_pick = False

                        if self.board.is_player_at(location):
                            self.board[location].kill()

                        if self.picked_fruit:
                            if location != current_location:
                                if self.board.is_of_type(location, fruits.Fruit):
                                    next_picked_fruit = self.board[location]
                                    should_pick = True
                                self.move_to(location)
                                self.unpick(self.picked_fruit, current_location)
                                if should_pick:
                                    self.pick(next_picked_fruit)
                        else:
                            if location != current_location:
                                if self.board.is_of_type(location, fruits.Fruit):
                                    should_pick = True
                                    next_picked_fruit = self.board[location]
                                self.move_to(location)
                                if should_pick:
                                    self.pick(next_picked_fruit)

                        if not self.is_alive:
                            self.board.draw_board_rect(self.board_location)
                            self.board.free_location(self.board_location)
                    finally:
                        self.board.mutex.release()
                except StopIteration:
                    break
        move_scheduler = threading.Timer(0, mover)
        move_scheduler.start()
        
    def pick(self, fruit):
        # print 'picked', fruit
        self.picked_fruit = fruit
        if fruit:
            fruit.picked = True

    def unpick(self, fruit, location):
        # print 'dropped', fruit, location
        self.picked_fruit = None
        self.board[location] = fruit
        if fruit:
            fruit.board_location = location
            fruit.picked = False
            if not isinstance(fruit, fruits.Strawberry):
                fruit.draw()
    
    def kill(self):
        self.is_alive = False
        self.board.draw_board_rect(self.board_location)
        self.board.free_location(self.board_location)

class PatrollingMonster(paths.FixedPathFollower, Monster):

    def __init__(self, given_board_location, given_board, surface, given_path):
        Monster.__init__(self, given_board_location, given_board,
                         surface, ".\\images\\patrolling.png")
        paths.FixedPathFollower.__init__(self, given_path)


class ChasingMonster(paths.ChaserAndBreaker, Monster):

    def __init__(self, given_board_location, given_board, surface):
        Monster.__init__(self, given_board_location, given_board,
                         surface, ".\\images\\chasing.png")
        paths.ChaserAndBreaker.__init__(self)


class RandomMonster(paths.RandomWalker, Monster):

    def __init__(self, given_board_location, given_board, surface):
        Monster.__init__(self, given_board_location,
                         given_board, surface, ".\\images\\random.png")

