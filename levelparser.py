import json

import sys
sys.path.append('.\\modules')

import board
import blocks
import locations
import fruits
import monsters
import player

MAP_FILE = 'mapFile'
BOARD = 'board'
BOARD_HEIGHT = 'boardHeight'
BOARD_WIDTH = 'boardWidth'
FRUIT_WAVES = 'fruitWaves'
STATIC_FRUITS = 'staticFruits'
MOVING_FRUITS = 'movingFruits'
PATROLLING_MONSTERS = 'patrollingMonsters'
CHASING_MONSTERS = 'chasingMonsters'
ICE_BLOCKS = 'iceBlocks'
WALL_BLOCKS = 'wallBlocks'
POINTS = 'points'
PLAYER  = 'player'

board_piece_type = {
    'i': blocks.IceBlock,
    'w': blocks.WallBlock,
    'a': fruits.Apple,
    'b': fruits.Banana,
    'g': fruits.Grapes
}

character_map = {
    "i": ICE_BLOCKS,
    "w": WALL_BLOCKS
}

class Levelparser(object):
    def __init__(filename, board_position, surface, fruit_kill_callback):
        self.screen = surface
        self.wave_number = 0
        self.fruit_kill_callback = fruit_kill_callback

        with open('.\\levels\\' + filename) as data_file:
            self.data = json.loads(data_file.read())
        
        with open('.\\levels\\' + self.data[MAP_FILE]) as map_file:
            all_maps = map_file.read().split('\n\n')
            self.block_map = all_maps[0]

            self.wave_maps = all_maps[1:] 

        self.objects = {
            ICE_BLOCKS: [],
            WALL_BLOCKS: [],
            FRUIT_WAVES: [],
            PATROLLING_MONSTERS: [],
            CHASING_MONSTERS: [],
        }

        self.board = board.GraphicalBoard(
            self.data[BOARD_WIDTH],
            self.data[BOARD_HEIGHT],
            board_position,
            self.screen
        )

        self.objects[BOARD] = self.board
        self.objects[PLAYER] = player.Player(
            locations.Point(*self.data[PLAYER]),
            the_board,
            board_surface
        )

    def parse_map(map, callback):
        for y in xrange(self.data[BOARD_HEIGHT]):
            line = map.readline().strip()
            for x, character in enumerate(line):
                if character.lower() in board_piece_type:
                    callback(x, y, character
    
    def set_ice_blocks(x, y, character):
        self.objects[character_map[character]].append(
            board_piece_type[character](
                locations.Point(x, y),
                self.board,
                self.surface
            )
        )
    
    def initiate_blocks(self):
        parse_map(self.block_map, set_ice_blocks)
    
    def set_static_fruits(x, y, character):
        self.objects[FRUIT_WAVES][self.wave_number][STATIC_FRUITS].append(
            board_piece_type[character](
                locations.Point(x, y),
                self.board,
                self.surface,
                character.isupper(),
                self.fruit_kill_callback
            )
        )

    def next_fruit_wave(self):
        self.wave_number += 1
        parse_map(self.wave_maps[self.wave_number], set_static_fruits)