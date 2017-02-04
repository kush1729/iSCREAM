import pygame
import fonts
import colors
import button
import json
import game
import threading

class Page(object):
    def __init__(self, screen):
        self.screen = screen
        self.buttons = []
        self.texts = []
        self.screen_horizontal_center = self.screen.get_rect().center[0]

    def display(self, caption="iSCREAM"):
        pygame.display.set_caption(caption)
        self.screen.fill(colors.WHITE)
        for text, text_rect in self.texts:
            self.screen.blit(text, text_rect)
        for button in self.buttons:
            button.display()
        pygame.display.flip()
    
    def clean(self):
        for button in self.buttons:
            button.clean()

class IntroducePage(Page):
    def __init__(self, screen):
        Page.__init__(self, screen)
        welcome_to = fonts.MEDIUM.render('WELCOME TO', True, colors.LIGHT_RED)
        welcome_to_rect = welcome_to.get_rect()
        welcome_to_rect.center = (self.screen_horizontal_center, 100)

        self.texts.append((welcome_to, welcome_to_rect))

        iscream = fonts.X_LARGE.render('iSCREAM', True, colors.CHOCOLATE)
        iscream_rect = iscream.get_rect()
        iscream_rect.center = (self.screen_horizontal_center, 275)

        self.texts.append((iscream, iscream_rect))

        def dummy_func():
            print 'click'
        
        play = button.Button(
            'PLAY',
            pygame.Rect(50, 450, 125, 125),
            colors.GREEN,
            colors.BLACK,
            dummy_func,
            self.screen
        )

        self.buttons.append(play)

        instructions = button.Button(
            'INSTRUCTIONS',
            pygame.Rect((self.screen.get_rect().width - 175) / 2, 450, 175, 125),
            colors.ORANGE,
            colors.BLACK,
            dummy_func,
            self.screen
        )

        self.buttons.append(instructions)

        quit = button.Button(
            'QUIT',
            pygame.Rect((self.screen.get_rect().width - 175), 450, 125, 125),
            colors.RED,
            colors.BLACK,
            dummy_func,
            self.screen
        )

        self.buttons.append(quit)
    
    def display(self):
        Page.display(self, "Welcome to iSCREAM")

class LevelPage(Page):
    def __init__(self, screen):
        Page.__init__(self, screen)

        heading = fonts.MED_LARGE.render("CHOOSE LEVEL", True, colors.CHOCOLATE)
        heading_rect = heading.get_rect()
        heading_rect.center = (self.screen_horizontal_center, 65)

        self.texts.append((heading, heading_rect))

        with open('..\\levels\\gamelevels.json') as game_file:
            level_files = json.loads(game_file.read())['gameLevels']

        level_button_margin_top = 150
        level_button_margin_left = 25
        num_level_buttons_in_row = 5
        level_button_width = 94
        level_button_height = 80
        gap = 25

        def dummy_func():
            print 'click!'
        
        for level_number in xrange(1, len(level_files) + 1):
            level_button = button.Button(
                'LEVEL {level_number}'.format(level_number=level_number),
                pygame.Rect(
                    level_button_margin_left + ((level_number - 1) % num_level_buttons_in_row) * (gap + level_button_width),
                    level_button_margin_top + ((level_number - 1) / 5) * (level_button_height + gap),
                    level_button_width,
                    level_button_height
                ),
                colors.GREEN,
                colors.BLACK,
                dummy_func,
                self.screen
            )
            self.buttons.append(level_button)
    
    def display(self):
        Page.display(self, "Select Level")

class GamePage(Page):
    def __init__(self, screen):
        Page.__init__(self, screen)
        self.image = pygame.Surface((self.screen.get_rect().width, self.screen.get_rect().height), pygame.SRCALPHA)

        for i in xrange(17):
            update_rect_1 = pygame.Rect(35 * i, 0, 35, 35)
            update_rect_2 = pygame.Rect(35 * i, 560, 35, 35)
            self.draw_border_rect(update_rect_1)
            self.draw_border_rect(update_rect_2)

        for i in xrange(1, 16):
            update_rect_1 = pygame.Rect(0, 35 * i, 35, 35)
            update_rect_2 = pygame.Rect(560, 35 * i, 35, 35)
            self.draw_border_rect(update_rect_1)
            self.draw_border_rect(update_rect_2)
    
    def draw_border_rect(self, update_rect):
        pygame.draw.rect(self.image, colors.MED_BLUE, update_rect)
        pygame.draw.rect(self.image, colors.BLACK, update_rect, 1)

    def display(self, level_file):
        def score_cb(score):
            text = fonts.SMALL.render(str(score), True, colors.BLACK)
            textRect = text.get_rect()
            textRect.bottomleft = (0, 665)
            
            self.screen.fill(colors.WHITE, pygame.Rect(0, 595 + 40, 150, 40))
            self.screen.blit(text, textRect)
            
            pygame.display.update(pygame.Rect(0, 595 + 40, 150, 40))
        
        def end_callback(user_won, score):
            def clear_screen():
                self.screen.fill(colors.WHITE)
            
            clear_scheduler = threading.Timer(1, clear_screen)
            clear_scheduler.start()
        
        Page.display(self)
        self.screen.blit(self.image, (0, 0))
        pygame.display.flip()

        current_game = game.Game(self.screen, (35, 35), level_file, score_cb, end_callback)
        current_game.start()

class ResultsPage(Page):
    def __init__(self, screen):
        Page.__init__(self, screen)
        def dummy_func():
            print 'click'
        
        play = button.Button(
            'PLAY',
            pygame.Rect(50, 450, 125, 125),
            colors.GREEN,
            colors.BLACK,
            dummy_func,
            self.screen
        )

        self.buttons.append(play)

        main_menu = button.Button(
            'MAIN MENU',
            pygame.Rect((self.screen.get_rect().width - 175) / 2, 450, 175, 125),
            colors.ORANGE,
            colors.BLACK,
            dummy_func,
            self.screen
        )

        self.buttons.append(main_menu)

        quit = button.Button(
            'QUIT',
            pygame.Rect((self.screen.get_rect().width - 175), 450, 125, 125),
            colors.RED,
            colors.BLACK,
            dummy_func,
            self.screen
        )

        self.buttons.append(quit)
    


class InstructionPage(Page):
    def __init__(self, screen):
        Page.__init__(self, screen)
        instructions = '''
        AVOID THE MONSTERS AND EAT ALL THE FRUITS
        TO COMPLETE THE LEVEL!

        USE THE ARROW KEYS TO NAVIGATE
        USE THE SPACEBAR TO SHOOT AND BREAK ICE
        PRESS 'P' TO PAUSE
        '''

        heading = fonts.MED_LARGE.render('INSTRUCTIONS', True, colors.CHOCOLATE)
        heading_rect = heading.get_rect()
        heading_rect.center = (self.screen_horizontal_center, 65)

        self.texts.append((heading, heading_rect))

        instructions_height = 190

        for line_index, line in enumerate(instructions.strip().split('\n')):
            line_surface = fonts.SMALL.render(line.strip(), True, colors.MED_BLUE)
            line_rect = line_surface.get_rect()
            line_rect.center = (self.screen_horizontal_center, instructions_height + line_index * 40)
            self.texts.append((line_surface, line_rect))
        
        def dummy_func():
            print 'click!'
        
        play = button.Button(
            'PLAY',
            pygame.Rect(50, 500, 175, 75),
            colors.GREEN,
            colors.BLACK,
            dummy_func,
            self.screen
        )

        self.buttons.append(play)

        quit = button.Button(
            'QUIT',
            pygame.Rect(self.screen.get_rect().width - 225, 500, 175, 75),
            colors.RED,
            colors.BLACK,
            dummy_func,
            self.screen
        )

        self.buttons.append(quit)
    
    def display(self):
        Page.display(self, "Instructions")


if __name__ == '__main__':
    import events
    pygame.init()
    a = pygame.display.set_mode((595, 665))
    b = ResultsPage(a)
    #b.display('level1.level.json')
    b.display()
    events.start()
