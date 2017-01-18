import pygame

import locations
import board
import monsters
import player

pygame.init()
screen = pygame.display.set_mode((500, 500))

grid = [(["empty" for i in range(9)] + ["full"]) for j in range(10)]

my_board = board.GraphicalBoard(grid, (0, 0), 500, 500)
my_monster = monsters.PatrollingMonster(locations.Point(0, 0),
    'images\\patrolling.png',
    my_board,
    [locations.Point(0, 0), locations.Point(9, 0), locations.Point(9, 9), locations.Point(0, 9)])
my_player = player.Player(locations.Point(5, 5), "images\\player.png", my_board)
my_board.start(my_player)

my_monster_group = pygame.sprite.RenderUpdates(my_monster)
my_monster.activate()

clock = pygame.time.Clock()
not_exited = True
try:
    while not_exited:
        deltat = clock.tick(24)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                my_player.is_alive = False
                not_exited = False
    
        my_monster_group.update()
        screen.fill((255, 0, 0))
        pygame.display.update(my_monster_group.draw(screen))
        
except KeyboardInterrupt:
    my_player.is_alive = False

    