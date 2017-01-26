import pygame
import player
import locations
import levelparser

import colors

class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((595, 595))
        def update_callback(rect):
            pygame.display.update(rect)
        self.data = levelparser.get_objects((35, 35), 35, self.screen, update_callback)
        self.not_suspended = True
    
    
    def start(self):
        board = self.data[levelparser.BOARD]
        user = player.Player(locations.Point(5, 5), board, self.screen, "images\\player.png")
        wall_blocks = pygame.sprite.RenderUpdates(self.data[levelparser.WALL_BLOCKS])
        ice_blocks = pygame.sprite.RenderUpdates(self.data[levelparser.ICE_BLOCKS])
        patrolling_monsters = pygame.sprite.RenderUpdates(self.data[levelparser.PATROLLING_MONSTERS])
        movables = self.data[levelparser.PATROLLING_MONSTERS]
        board.start(user)

        clock = pygame.time.Clock()

        for movable in movables:
            movable.activate()

        pygame.display.flip()
        try:
            while self.not_suspended:
                clock.tick(30)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        user.kill()
                        self.not_suspended = False     
        except KeyboardInterrupt:
            user.kill()

    def suspend(self):
        self.not_suspended = False
    
    def restart(self):
        pass
    
    def continue_game(self):
        self.not_suspended = True