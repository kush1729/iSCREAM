import pygame

import sys
sys.path.append(".\\modules\\")

import locations
import board
import monsters
import player
import blocks
import fruits

import colors

pygame.init()
screen = pygame.display.set_mode((595, 595))

my_board = board.GraphicalBoard(17, 17,(0, 0), 595, 595, screen)
my_monster = monsters.PatrollingMonster(locations.Point(0, 0),
    my_board,
    'images\\patrolling.png',
    [locations.Point(0, 0), locations.Point(9, 0), locations.Point(9, 9), locations.Point(0, 9)])
my_player = player.Player(locations.Point(5, 5), my_board, "images\\player.png")
my_board.start(my_player)

my_monster_group = pygame.sprite.RenderUpdates(my_monster)

my_iceblocks = blocks.WallBlock(locations.Point(8, 0), my_board)
my_iceblock_group = pygame.sprite.RenderUpdates(my_iceblocks)

pygame.display.set_caption('iSCREAM')
pygame.display.set_icon(pygame.image.load('images\\icon.jpg'))
pygame.display.flip()
my_monster.activate()

fruit = fruits.Banana(locations.Point(13, 13), my_board, 100)
my_fruits = pygame.sprite.RenderUpdates(fruit)

clock = pygame.time.Clock()
not_exited = True
try:
    while not_exited:
        deltat = clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                my_player.is_alive = False
                not_exited = False
    
        my_monster_group.update()
        my_iceblock_group.update()
        my_fruits.update()
        pygame.display.update(my_monster_group.draw(screen))
        pygame.display.update(my_iceblock_group.draw(screen))
        pygame.display.update(my_fruits.draw(screen))
        
except KeyboardInterrupt:
    my_player.is_alive = False

    