import pygame
from consts import load_image

pygame.init()
size = width, height = 450, 600
screen = pygame.display.set_mode(size)
# screen.fill('white')
all_sprites = pygame.sprite.Group()


class GoldCoin(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('gold.jpg', -1), (50, 50))

    def __init__(self, group):
        super().__init__(group)
        self.image = GoldCoin.image
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 550
        self.blue_gold = 5
        self.red_gold = 4
        self.gold_to_pos = {1: (419, 564), 2: (412, 564)} # change

    def update(self, color, screen):
        gold = self.blue_gold if color == 'blue' else self.red_gold
        font = pygame.font.SysFont('default', 32, italic=False, bold=False)
        text = font.render(f'{gold}', 1, "#895404")
        pos = self.gold_to_pos[len(str(gold))]
        screen.blit(text, pos)

    def buy(self, price, color):
        gold = self.blue_gold if color == 'blue' else self.red_gold
        if gold >= price:
            gold -= price
            gold = max(gold, 0)
            return True
        return False


def main():
    running = True
    coin = GoldCoin(all_sprites)
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
