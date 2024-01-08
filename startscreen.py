import pygame
import sys
from load_image import load_image

class InputBox:
    def __init__(self, position, size, font, border_color=(0, 0, 0)):
        self.position = position
        self.size = size
        self.font = font
        self.border_color = border_color
        self.text = ''

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += pygame.key.name(event.key)
        return False

    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), (self.position[0], self.position[1], self.size[0], self.size[1]))
        pygame.draw.rect(screen, self.border_color, (self.position[0], self.position[1], self.size[0], self.size[1]), 2)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, (self.position[0] + 22, self.position[1]))

class InfoButton:
    def __init__(self, position, size, image_path):
        self.position = position
        self.size = size
        self.image = pygame.transform.scale(load_image(image_path), size)
        self.clicked = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.clicked = not self.clicked

    def render(self, screen):
        screen.blit(self.image, self.position)
        self.rect = pygame.Rect(self.position, self.size)

class StartScreen:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Stratego")

        self.background_color = (200, 200, 200)
        self.font = pygame.font.Font(None, 36)
        self.font_input = pygame.font.Font(None, 32)
        self.clock = pygame.time.Clock()

        self.player1_name = ""
        self.player2_name = ""

        self.load_images()
        self.dialog_active = False
        self.input_active = 0  # 0: Player 1, 1: Player 2

        self.input_box_player1 = InputBox((width // 4 + 18, height // 4 + height // 2 - 32), (204, 36), self.font_input)
        self.input_box_player2 = InputBox((width // 4 + 18, height // 4 + height // 2 + 28), (204, 36), self.font_input)

        self.info_rules_button = InfoButton((10, 10), (100, 40), "gold.jpg")
        self.rules_text = [
            "Game Rules:",
            "1. Enter names for Player 1 and Player 2.",
            "2. Press 'Start' to begin the game."
        ]

    def load_images(self):
        self.background_image = pygame.transform.scale(load_image("Background.png"), (self.width, self.height))
        self.start_button_image = load_image("start.png")

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.info_rules_button.handle_event(event)
                    if not self.dialog_active:
                        if self.start_button_image.get_rect(center=(self.width // 2, self.height * 3 // 4)).collidepoint(event.pos):
                            self.dialog_active = True
                            self.input_active = 0

                elif event.type == pygame.KEYDOWN:
                    if self.dialog_active:
                        if self.input_active == 0:
                            if self.input_box_player1.handle_event(event):
                                self.input_active = 1
                        elif self.input_active == 1:
                            if self.input_box_player2.handle_event(event):
                                self.dialog_active = False

            self.screen.fill(self.background_color)

            if not self.dialog_active:
                self.screen.blit(self.background_image, (0, 0))
                self.display_text("Stratego", self.width // 2, self.height // 4)
                self.display_start_button()
                self.info_rules_button.render(self.screen)
            else:
                self.display_dialog()

            pygame.display.flip()
            self.clock.tick(30)

    def handle_dialog_keydown(self, key):
        pass

    def display_text(self, text, x, y, color=(0, 0, 0)):
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

    def display_start_button(self):
        start_button_rect = self.start_button_image.get_rect(center=(self.width // 2, self.height * 3 // 4))
        self.screen.blit(self.start_button_image, start_button_rect)

    def display_dialog(self):
        dialog_rect = pygame.Rect(self.width // 4, self.height // 4, self.width // 2, self.height // 2)
        pygame.draw.rect(self.screen, (255, 255, 255), dialog_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), dialog_rect, 2)

        self.display_text("Enter names:", self.width // 2, self.height // 3)

        if self.info_rules_button.clicked:
            self.show_rules_dialog()
        else:
            self.display_text("Click 'Info Rules' for Rules", self.width // 2, self.height // 3 + 100, (0, 0, 0))

        self.input_box_player1.render(self.screen)
        self.input_box_player2.render(self.screen)

        if self.input_active == 0:
            pygame.draw.line(self.screen, (0, 0, 0), (dialog_rect.x + 22 + self.font_input.size(self.input_box_player1.text)[0], dialog_rect.y + dialog_rect.height // 2 - 30),
                             (dialog_rect.x + 22 + self.font_input.size(self.input_box_player1.text)[0], dialog_rect.y + dialog_rect.height // 2 - 30 + 32), 2)
        elif self.input_active == 1:
            pygame.draw.line(self.screen, (0, 0, 0), (dialog_rect.x + 22 + self.font_input.size(self.input_box_player2.text)[0], dialog_rect.y + dialog_rect.height // 2 + 30),
                             (dialog_rect.x + 22 + self.font_input.size(self.input_box_player2.text)[0], dialog_rect.y + dialog_rect.height // 2 + 30 + 32), 2)

    def show_rules_dialog(self):
        self.display_text("Game Rules", self.width // 2, self.height // 8, (0, 0, 0))
        for i, line in enumerate(self.rules_text):
            self.display_text(line, self.width // 2, self.height // 3 + i * 40, (0, 0, 0))

if __name__ == "__main__":
    screen = StartScreen(800, 600)
    screen.run()
