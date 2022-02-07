from settings import *
from loading import *
from level import Level
from game_data import *
from results import results

levels = {'level1': level_1, 'level2': level_2, 'level3': level_3}


def main(typ):
    class Game:
        def __init__(self, level, screenn):
            self.create_level(level, screenn)
            self.current_level = level

        def create_level(self, level, screenn):
            self.level = Level(level, screenn)

        def run(self):
            self.level.run()

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screeen_height))
    clock = pygame.time.Clock()
    font = pygame.font.Font("data/font/Bungee-Regular.ttf", 80)
    font1 = pygame.font.Font("data/font/Bungee-Regular.ttf", 27)
    text_game_over = font.render('You died', True, (255, 0, 0))
    text_loading = font1.render('Loading...', True, (0, 0, 0))
    background = pygame.image.load('data/menu/foggy.png')
    tgox = screen_width // 2 - text_game_over.get_width() // 2
    tgoy = screeen_height // 2 - text_game_over.get_height() // 2
    n = 1
    running = True
    alive = True
    screen.blit(background, (0, 0))
    screen.blit(text_loading, (screen_width - 185, screeen_height - 60))
    pygame.display.update()
    game = Game(levels[typ], screen)
    counter_death_screen = 0
    while running:
        if alive != 'False':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                if str(int(abs(alive))).isdigit() and alive is not True:
                    game.level.restart(game.current_level)
                    m = results(alive)
                    alive = True
                    if m:
                        return 'Completed'
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game.level.collide_check(event.pos):
                        screen.blit(background, (0, 0))
                        pygame.display.update()
                        game.level.restart(game.current_level)
                        return 'Home'
                    if n:
                        game.level.player.sprite.attacking1 = False
                        game.level.player.sprite.attacking2 = True
                        n = 0
                    else:
                        game.level.player.sprite.attacking1 = True
                        game.level.player.sprite.attacking2 = False
                        n = 1
            alive = game.level.run()
        else:
            screen.fill('black')
            screen.blit(text_game_over, (tgox, tgoy))
            counter_death_screen += 1
            if counter_death_screen > 200:
                alive = True
                game.level.restart(game.current_level)
                counter_death_screen = 0
        pygame.display.update()
