import pygame

import sys
sys.path.append(".\\modules\\")

import locations
import board
import monsters
import player
import blocks

import colors

pygame.init()
screen = pygame.display.set_mode((595, 595))

grid = [(["empty" for i in range(16)] + ["full"]) for j in range(17)]

my_board = board.GraphicalBoard(grid, (0, 0), 595, 595, screen)
#my_monster = monsters.PatrollingMonster(locations.Point(0, 0),
#    'images\\patrolling.png',
#    my_board,
#    [locations.Point(0, 0), locations.Point(9, 0), locations.Point(9, 9), locations.Point(0, 9)])
my_player = player.Player(locations.Point(5, 5), "images\\player.png", my_board)
my_board.start(my_player)

#my_monster_group = pygame.sprite.RenderUpdates(my_monster)
#my_monster.activate()

my_iceblocks = blocks.IceBlock(locations.Point(8, 0), my_board, screen)
my_iceblock_group = pygame.sprite.RenderUpdates(my_iceblocks)

pygame.display.set_caption('iScream')
pygame.display.set_icon(pygame.image.load('images\\icon.jpg'))
pygame.display.flip()

clock = pygame.time.Clock()
not_exited = True
try:
    while not_exited:
        deltat = clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                my_player.is_alive = False
                not_exited = False
    
        #my_monster_group.update()
        my_iceblock_group.update()
        #pygame.display.update(my_monster_group.draw(screen))
        pygame.display.update(my_iceblock_group.draw(screen))
        
except KeyboardInterrupt:
    my_player.is_alive = False

    