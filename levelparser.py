import sys
import json
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

def get_objects(board_position, square_side, board_surface):
    return_data = {
        BOARD: None,
        ICE_BLOCKS: [],
        WALL_BLOCKS: [],
        FRUIT_WAVES: [],
        PATROLLING_MONSTERS: [],
        CHASING_MONSTERS: [],
        PLAYER: None
    }    

    with open('.\\levels\\fruitstest.level.json') as level_file:
        level_data = json.loads(level_file.read())
    
    the_board = board.GraphicalBoard(level_data[BOARD_WIDTH],
    level_data[BOARD_HEIGHT],
    board_position, board_surface)

    return_data[PLAYER] = player.Player(locations.Point(*level_data[PLAYER]), the_board, board_surface)

    return_data[PATROLLING_MONSTERS] = [
        monsters.PatrollingMonster(
            locations.Point(*monsterdata[POINTS][0]),
            the_board,
            board_surface,
            [locations.Point(x, y) for x, y in monsterdata[POINTS]]
        ) for monsterdata in level_data[PATROLLING_MONSTERS]]

    def parse_map(callback):
        for y in xrange(level_data[BOARD_HEIGHT]):
            line = map.readline().strip()
            for x, character in enumerate(line):
                if character.islower():
                    callback(x, y, character)

    with open('.\\levels\\' + level_data[MAP_FILE]) as map:
        def set_ice_blocks(x, y, character):
            return_data[character_map[character]].append(board_piece_type[character](locations.Point(x, y), the_board, board_surface))
        
        parse_map(set_ice_blocks)

        for wave in level_data[FRUIT_WAVES]:
            map.readline()
            
            wave_data = {
                STATIC_FRUITS: [],
                MOVING_FRUITS: []
            }

            def set_static_fruits(x, y, character):
                wave_data[STATIC_FRUITS].append(board_piece_type[character](locations.Point(x, y), the_board, board_surface))

            parse_map(set_static_fruits)

            return_data[FRUIT_WAVES].append(wave_data)
    
    return_data[BOARD] = the_board
    return return_data

if __name__ == '__main__':
    pass
        