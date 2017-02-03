import pygame
import player
import locations
import levelparser
import itertools

import colors


class Game(object):

    def __init__(self, file_name):
        self.screen = pygame.display.set_mode((525, 525))

        def fruit_kill_function():
            self.num_fruits -= 1
            try:
                if self.num_fruits == 0:
                    self.next_wave()
            except IndexError:
                self.not_suspended = False
                self.board.game_not_ended = False

        self.dataparser = levelparser.Levelparser(file_name, (0, 0), self.screen, fruit_kill_function)
        self.not_suspended = True
        self.num_fruits = 0

    def start(self):
        self.board = self.dataparser.board
        user = self.dataparser.player

        self.dataparser.initiate_monsters()
        self.dataparser.initiate_blocks()
        self.next_wave()
        self.board.start(user)

        clock = pygame.time.Clock()

        for movable in itertools.chain(self.dataparser.objects[levelparser.PATROLLING_MONSTERS],
            self.dataparser.objects[levelparser.CHASING_MONSTERS],
            self.dataparser.objects[levelparser.FRUIT_WAVES][self.dataparser.wave_number][levelparser.MOVING_FRUITS],
            self.dataparser.objects[levelparser.RANDOM_MONSTERS]):
            movable.activate()

        pygame.display.flip()
        try:
            while self.not_suspended and user.is_alive:
                clock.tick(30)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        user.kill()
                        self.not_suspended = False
                    else:
                        user.handle_event(event)
        except KeyboardInterrupt:
            user.kill()

    def next_wave(self):
        self.dataparser.next_fruit_wave()
        self.num_fruits = self.dataparser.get_current_wave_size()

    def suspend(self):
        self.not_suspended = False

    def restart(self):
        pass

    def continue_game(self):
        self.not_suspended = True
