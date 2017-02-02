import json

import sys

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
STRAWBERRIES = 'strawberries'
PATROLLING_MONSTERS = 'patrollingMonsters'
CHASING_MONSTERS = 'chasingMonsters'
ICE_BLOCKS = 'iceBlocks'
WALL_BLOCKS = 'wallBlocks'
POINTS = 'points'
PLAYER = 'player'

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

    def __init__(self, filename, board_position, surface, fruit_kill_callback):
        self.screen = surface
        self.wave_number = -1
        self.fruit_kill_callback = fruit_kill_callback

        with open('.\\levels\\' + filename) as data_file:
            self.data = json.loads(data_file.read())

        with open('.\\levels\\' + self.data[MAP_FILE]) as map_file:
            all_maps = map_file.read().strip().split('\n\n')
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

        self.player = player.Player(
            locations.Point(*self.data[PLAYER]),
            self.board,
            self.screen
        )
    
    def initiate_monsters(self):
        self.objects[PATROLLING_MONSTERS] = [
        monsters.PatrollingMonster(
            locations.Point(*monsterdata[POINTS][0]),
            self.board,
            self.screen,
            [locations.Point(*point) for point in monsterdata[POINTS]]
        ) for monsterdata in self.data[PATROLLING_MONSTERS]]

        self.objects[CHASING_MONSTERS] = [
            monsters.ChasingMonster(
                locations.Point(*location),
                self.board,
                self.screen
            ) for location in self.data[CHASING_MONSTERS]
        ]

    def parse_map(self, map, callback):
        for y, line in enumerate(map.split()):
            for x, character in enumerate(line):
                if character.lower() in board_piece_type:
                    callback(x, y, character)

    def set_ice_blocks(self, x, y, character):
        self.objects[character_map[character]].append(
            board_piece_type[character](
                locations.Point(x, y),
                self.board,
                self.screen
            )
        )

    def initiate_blocks(self):
        self.parse_map(self.block_map, self.set_ice_blocks)

    def set_static_fruits(self, x, y, character):
        self.objects[FRUIT_WAVES][self.wave_number][STATIC_FRUITS].append(
            board_piece_type[character.lower()](
                locations.Point(x, y),
                self.board,
                self.screen,
                character.isupper(),
                self.fruit_kill_callback
            )
        )

    def next_fruit_wave(self):
        self.wave_number += 1
        self.objects[FRUIT_WAVES].append(
            {STATIC_FRUITS: [], MOVING_FRUITS: []})
        self.parse_map(
            self.wave_maps[self.wave_number], self.set_static_fruits)
        
        self.objects[FRUIT_WAVES][self.wave_number][MOVING_FRUITS] = [
            fruits.Strawberry(
                locations.Point(*strawberry_data[0]),
                self.board,
                self.screen,
                self.fruit_kill_callback,
                [locations.Point(*point) for point in strawberry_data]
            ) for strawberry_data in self.data[FRUIT_WAVES][self.wave_number][STRAWBERRIES]
        ]

    def get_current_wave_size(self):
        return len(self.objects[FRUIT_WAVES][self.wave_number][STATIC_FRUITS]) \
            + len(self.objects[FRUIT_WAVES][self.wave_number][MOVING_FRUITS])
