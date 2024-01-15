import os

import pygame
from consts import load_image, SCREEN_SCALE

pygame.init()
size = width, height = 500, 700
screen = pygame.display.set_mode(size)
# screen.fill('white')
all_sprites = pygame.sprite.Group()

class GoldCoin(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('gold.png'), (50 * SCREEN_SCALE, 50 * SCREEN_SCALE))

    def __init__(self, group):
        super().__init__(group)
        self.image = GoldCoin.image
        self.rect = self.image.get_rect()
        self.rect.x = int(408 * SCREEN_SCALE)
        self.rect.y = int(300 * SCREEN_SCALE)
        self.golds = {'blue': 5, 'red': 4}
        # self.blue_gold = 5
        # self.red_gold = 4
        self.gold_to_pos = {1: (int(self.rect.x + 23), int(self.rect.y + 13)), 2: (int(self.rect.x + 20), int(self.rect.y + 20))}  # change

    def update(self, color, surface):
        gold = self.golds[color]
        fullname = os.path.join('data', "DungeonFont.ttf")
        font = pygame.font.Font(fullname, int(32 * SCREEN_SCALE))
        text = font.render(f'{gold}', 1, "#895404")
        pos = self.gold_to_pos[len(str(gold))]
        surface.blit(text, pos)

    def buy(self, price, color):
        gold = self.golds[color]
        if gold >= price:
            gold -= price
            gold = max(gold, 0)
            self.golds[color] = gold
            return True
        return False


def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
