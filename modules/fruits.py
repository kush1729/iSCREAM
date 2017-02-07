import boardpiece
import pygame
import paths
import colors
import threading
import time
import player
import monsters
import board
import blocks

class Fruit(boardpiece.BoardPiece):

    def __init__(self, given_board_location, given_board, surface, given_score, given_image_string, frozen, fruit_kill_callback):
        self.should_draw_on_init = True
        self.score = given_score

        self.frozen = frozen
        self.alive = True

        self.kill_callback = fruit_kill_callback

        self.picked = False

        def collide_resolver(location):
            if self.board.is_of_type(location, monsters.Monster):
                self.should_draw_on_init = False
                self.board[location].pick(self)
            elif self.board.is_of_type(location, blocks.Block):
                self.should_draw_on_init = True
                self.board[location].kill()
                self.freeze()
                self.board.reserve_location(location, self)
            elif self.board.is_of_type(location, player.Player):
                self.should_draw_on_init = False
                self.board[location].eat(self)
        
        boardpiece.BoardPiece.__init__(
            self, given_board_location, given_board, surface, collide_resolver)

        self.original_image = pygame.image.load(
            given_image_string).convert_alpha()
        self.image = pygame.Surface(
            [self.board.square_side, self.board.square_side], pygame.SRCALPHA)
        self.rect = self.image.get_rect()

        self.rect.topleft = self.board.get_position(self.board_location)

        if self.frozen:
            self.freeze()

        if self.should_draw_on_init:
            self.draw()

    def freeze(self):
        self.frozen = True
        self.draw(colors.LIGHT_BLUE)

    def unfreeze(self):
        self.frozen = False
        self.draw(colors.SNOW)

    def draw(self, background_color=colors.SNOW):
        if not self.board.is_of_type(self.board_location, Fruit):
            return
        update_rect = pygame.Rect(
            (0, 0), (self.board.square_side, self.board.square_side))

        pygame.draw.rect(self.image, background_color, update_rect)
        self.image.blit(self.original_image, (1, 1))
        pygame.draw.rect(self.image, colors.BLACK, update_rect, 1)

        target_rect = pygame.Rect(update_rect)
        self.screen.blit(self.image, self.position)
        pygame.display.update(pygame.Rect(
            self.position, (self.board.square_side, self.board.square_side)))

    def kill(self):
        self.alive = False
        self.kill_callback(self)


class Strawberry(Fruit, paths.FixedPathFollower):

    def __init__(self, given_board_location, given_board, surface, fruit_kill_callback, given_path):
        Fruit.__init__(self, given_board_location, given_board, surface,
                       200, ".\\images\\strawberry.png", False, fruit_kill_callback)
        paths.FixedPathFollower.__init__(self, given_path)
        
        self.tolerated_types = (player.Player, monsters.Monster)

        self.delay = 0.1

        self.point_feed = self.get_path()
    
    def activate(self):

        def mover():
            while self.alive:
                time.sleep(self.delay)
                self.board.mutex.acquire()
                try:
                    if not self.frozen and self.alive and not self.picked and self.board.game_not_suspended():
                        try:
                            location = self.point_feed.next()
                            if self.board.is_of_type(location, monsters.Monster):
                                self.board[location].pick(self)
                                self.board[self.board_location] = None
                                self.board_location = location
                                self.board.draw_board_rect(self.board_location)
                            else:
                                if self.board.is_of_type(location, player.Player):
                                    self.board.free_location(self.board_location)
                                    self.board.player.eat(self)
                                    break
                                self.move_to(location)
                        except StopIteration:
                            break
                finally:
                    self.board.mutex.release()
        move_scheduler = threading.Timer(0, mover)
        move_scheduler.start()


class Apple(Fruit):

    def __init__(self, given_board_location, given_board, surface, frozen, fruit_kill_callback):
        Fruit.__init__(self, given_board_location, given_board, surface,
                       25, ".\\images\\apple.png", frozen, fruit_kill_callback)


class Banana(Fruit):

    def __init__(self, given_board_location, given_board, surface, frozen, fruit_kill_callback):
        Fruit.__init__(self, given_board_location, given_board, surface,
                       50, ".\\images\\banana.png", frozen, fruit_kill_callback)


class Grapes(Fruit):

    def __init__(self, given_board_location, given_board, surface, frozen, fruit_kill_callback,):
        Fruit.__init__(self, given_board_location, given_board, surface,
                       100, ".\\images\\grapes.png", frozen, fruit_kill_callback)
