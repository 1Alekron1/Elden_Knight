import pygame
from settings import *
from loading import *
from level import Level
from game_data import level_0


class Game:
    def __init__(self, level, screen):
        self.create_level(level, screen)

    def create_level(self, level, screen):
        self.level = Level(level, screen)

    def run(self):
        self.level.run()





def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screeen_height))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 100)
    text_game_over = font.render('You died', True, (255, 0, 0))
    tgox = screen_width // 2 - text_game_over.get_width() // 2
    tgoy = screeen_height // 2 - text_game_over.get_height() // 2
    # Группы спрайтов
    player_group = pygame.sprite.Group()
    n = 1
    running = True
    alive = True
    game = Game(level_0, screen)
    counter_death_screen = 0
    while running:
        if alive:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
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
                game.level.restart(level_0, screen)
                counter_death_screen = 0
        pygame.display.update()
        clock.tick(fps)
    pygame.quit()

if __name__ == '__main__':
    main()
