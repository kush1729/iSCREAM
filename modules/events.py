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
    try:
        event_dict[pygame.KEYDOWN][key].remove(callback)
    except KeyError:
        pass

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

def handle_event(event):
    global loop
    if event.type == pygame.KEYDOWN:
        for action in event_dict[pygame.KEYDOWN][event.key]:
            action()
    elif event.type == pygame.MOUSEBUTTONUP:
        for clickable in event_dict[pygame.MOUSEBUTTONUP]:
            if clickable.rect.topleft[0] <= event.pos[0] <= clickable.rect.topright[0] \
                and clickable.rect.topleft[1] <= event.pos[1] <= clickable.rect.bottomright[1]:
                event_dict[pygame.MOUSEBUTTONUP][clickable]()
    elif event.type == pygame.QUIT:
        for action in event_dict[pygame.QUIT]:
            action()
        loop = False

def start():
    c = pygame.time.Clock()
    while loop:
        c.tick(30)
        for e in pygame.event.get():
            handle_event(e)

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
    
    
