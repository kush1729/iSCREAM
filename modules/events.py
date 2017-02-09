import pygame
from collections import defaultdict
from weakref import WeakKeyDictionary

event_dict = {
    pygame.KEYDOWN: defaultdict(set),
    pygame.MOUSEBUTTONUP: dict(),
    pygame.QUIT: set(),
    'mouseenter': set(),
    'mouseleave': set()
}

loop = True


def add_keypress_listener(key, callback):
    event_dict[pygame.KEYDOWN][key].add(callback)


def remove_keypress_listener(key, callback):
    event_dict[pygame.KEYDOWN][key].remove(callback)


def add_click_listener(clickable, callback):
    event_dict[pygame.MOUSEBUTTONUP][clickable] = callback


def remove_click_listener(clickable):
    del event_dict[pygame.MOUSEBUTTONUP][clickable]


def add_exit_listener(callback):
    event_dict[pygame.QUIT].add(callback)


def remove_exit_listener(callback):
    try:
        event_dict[pygame.QUIT].remove(callback)
    except KeyError:
        pass

count_dict = {pygame.K_UP: None, pygame.K_DOWN: None,
              pygame.K_LEFT: None, pygame.K_RIGHT: None}


def handle_event(event):
    global loop
    if event.type == pygame.KEYDOWN:
        for action in event_dict[pygame.KEYDOWN][event.key].copy():
            if event.key in count_dict:
                count_dict[event.key] = 0
            action()
    elif event.type == pygame.MOUSEBUTTONUP:
        for clickable in event_dict[pygame.MOUSEBUTTONUP].copy():
            if clickable.rect.topleft[0] <= event.pos[0] <= clickable.rect.topright[0] \
                    and clickable.rect.topleft[1] <= event.pos[1] <= clickable.rect.bottomright[1]:
                event_dict[pygame.MOUSEBUTTONUP][clickable]()
    elif event.type == pygame.QUIT:
        for action in event_dict[pygame.QUIT].copy():
            action()
        loop = False
            


def start():
    c = pygame.time.Clock()
    try:
        while loop:
            c.tick(30)
            # to handle long press
            long_press_delay_time = 5
            keystate = pygame.key.get_pressed()
            for arrow_key in count_dict:
                pressed = keystate[arrow_key]
                if pressed and count_dict[arrow_key] is not None:
                    count_dict[arrow_key] += 1
                else:
                    count_dict[arrow_key] = None
                if count_dict[arrow_key] > long_press_delay_time:
                    for action in event_dict[pygame.KEYDOWN][arrow_key]:
                        action()

            for e in pygame.event.get():
                handle_event(e)
    except KeyboardInterrupt:
        for action in event_dict[pygame.QUIT]:
            action()


def stop():
    global loop
    loop = False


if __name__ == '__main__':
    pygame.init()
    a = pygame.display.set_mode((100, 100))

    class B(object):

        def __init__(self):
            self.rect = a.get_rect()

            def click():
                print 'click'
            add_click_listener(self, click)

    b = B()

    def a_p():
        print 'a clicked'

    add_keypress_listener(pygame.K_a, a_p)
