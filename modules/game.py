import pygame
import player
import locations
import levelparser

import colors


class Game(object):

    def __init__(self):
        self.screen = pygame.display.set_mode((525, 525))

        def fruit_kill_function():
            self.num_fruits -= 1
            print self.num_fruits
            if self.num_fruits == 0:
                self.next_wave()

        self.data = levelparser.get_objects(
            (0, 0), 35, self.screen, fruit_kill_function)
        self.not_suspended = True
        self.num_fruits = 0

    def start(self):
        board = self.data[levelparser.BOARD]
        user = self.data[levelparser.PLAYER]
        wall_blocks = pygame.sprite.RenderUpdates(
            self.data[levelparser.WALL_BLOCKS])
        ice_blocks = pygame.sprite.RenderUpdates(
            self.data[levelparser.ICE_BLOCKS])
        self.next_wave()
        patrolling_monsters = pygame.sprite.RenderUpdates(
            self.data[levelparser.PATROLLING_MONSTERS])
        movables = self.data[levelparser.PATROLLING_MONSTERS]
        board.start(user)

        clock = pygame.time.Clock()

        for movable in movables:
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
        self.current_wave = levelparser.get_fruits()
        self.num_fruits = len(
            self.current_wave[levelparser.STATIC_FRUITS]) + len(self.current_wave)

    def suspend(self):
        self.not_suspended = False

    def restart(self):
        pass

    def continue_game(self):
        self.not_suspended = True
