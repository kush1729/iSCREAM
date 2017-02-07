from movable import Movable
import fruits
import blocks
import pygame
import locations
import directions
import events
import threading

class Player(Movable):
    """Defines the player that the user controls.
    """

    MOVE_MAP = {
        pygame.K_UP: directions.UP,
        pygame.K_DOWN: directions.DOWN,
        pygame.K_LEFT: directions.LEFT,
        pygame.K_RIGHT: directions.RIGHT
    }

    def __init__(self, given_board_location, given_board, surface, kill_callback):
        def void(location):
            pass
        Movable.__init__(self, given_board_location,
                         given_board, surface, void, ".\\images\\player.png")
        self.is_alive = True
        self.tolerated_types = (fruits.Fruit,)
        self.kill_callback = kill_callback
        self.direction = directions.RIGHT
        self.score = 0

        def make_handler(direction):
            def handle_key():
                self.board.mutex.acquire()
                try:
                    if self.board.game_not_suspended():
                        new_location = self.board_location + direction
                        if new_location in self.board and self.board.is_of_type(new_location, fruits.Fruit) and not self.board.is_frozen(new_location):
                            self.eat(self.board[new_location])
                        self.move_to(new_location)
                        self.direction = direction
                finally:
                    self.board.mutex.release()
            return handle_key
        
        def shoot_handler():
            self.board.mutex.acquire()
            try:
                if self.board.game_not_suspended():
                    self.shoot()
            finally:
                self.board.mutex.release()
        
        events.add_keypress_listener(pygame.K_SPACE, shoot_handler)

        self.event_handlers = {}

        for key, direction in self.MOVE_MAP.items():
            self.event_handlers[key] = make_handler(direction)
            events.add_keypress_listener(key, self.event_handlers[key])
    
    def eat(self, fruit):
        self.score += fruit.score
        fruit.kill()

    def kill(self):
        self.is_alive = False
        for key, event_handler in self.event_handlers.items():
            events.remove_keypress_listener(key, event_handler)
        self.kill_callback()

    def shoot(self):
        ice_point = locations.Point.copy(self.board_location) + self.direction
        if ice_point in self.board:
            if self.board.is_frozen(ice_point):
                self.remove_ice()
            else:
                self.shoot_ice()

    def remove_ice(self):
        ice_point = locations.Point.copy(self.board_location) + self.direction
        while ice_point in self.board and self.board.is_frozen(ice_point):
            self.board.unfreeze(ice_point)
            ice_point += self.direction

    def shoot_ice(self):
        ice_point = locations.Point.copy(self.board_location) + self.direction
        while ice_point in self.board and self.board.is_location_clear(self.tolerated_types, ice_point):
            self.board.freeze(ice_point)
            ice_point += self.direction