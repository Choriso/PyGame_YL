import os

import pygame
from consts import load_image, SCREEN_SCALE, COIN_SIZE

pygame.init()
size = width, height = 500 * SCREEN_SCALE, 620 * SCREEN_SCALE
screen = pygame.display.set_mode(size)
# screen.fill('white')
all_sprites = pygame.sprite.Group()


class GoldCoin(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('gold.png'), COIN_SIZE)

    def __init__(self, group, cords):
        super().__init__(group)
        self.image = GoldCoin.image
        self.rect = self.image.get_rect()
        print(self.rect)
        self.rect.x, self.rect.y = cords
        self.golds = {1: 1, 2: 4}

    def gold_to_params(self, gold) -> tuple[tuple[float | int, float | int], int]:
        font = int(32 * SCREEN_SCALE)
        match len(str(gold)):
            case 3:
                return (self.rect.x + COIN_SIZE[0] / 2 - font / 2, (self.rect.y + COIN_SIZE[1] / 2 - font / 2)), font
            case 2:
                return (self.rect.x + COIN_SIZE[0] / 2 - font / 3, (self.rect.y + COIN_SIZE[1] / 2 - font / 2)), font
            case 1:
                return (self.rect.x + COIN_SIZE[0] / 2 - font / 6, (self.rect.y + COIN_SIZE[1] / 2 - font / 2)), font

    def update(self, color: str, surface) -> None:
        gold: int = self.golds[1 if color == 'blue' else 2]
        pos, font_size = self.gold_to_params(gold)
        fullname = os.path.join('data', "DungeonFont.ttf")
        font = pygame.font.Font(fullname, font_size)
        text = font.render(f'{gold}', True, "#895404")
        surface.blit(text, pos)

    def buy(self, price: int, player: int) -> bool:
        gold: int = self.golds[player]
        if gold >= price:
            gold -= price
            gold = max(gold, 0)
            self.golds[player] = gold
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
