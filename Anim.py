import pygame


class Animation:
    def __init__(self, image_path, frame_width, frame_height, frame_duration):
        self.sprite_sheet = pygame.image.load(image_path).convert_alpha()
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_duration = frame_duration

        self.frames = self.load_frames()
        self.current_frame = 0
        self.time_since_last_frame = 0

    def load_frames(self):
        frames = []
        for y in range(0, self.sprite_sheet.get_height(), self.frame_height):
            for x in range(0, self.sprite_sheet.get_width(), self.frame_width):
                rect = pygame.Rect(x, y, self.frame_width, self.frame_height)
                frame = self.sprite_sheet.subsurface(rect)
                frames.append(frame)
        return frames

    def update(self, dt):
        self.time_since_last_frame += dt
        if self.time_since_last_frame > self.frame_duration:
            self.time_since_last_frame -= self.frame_duration
            self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, surface, x, y):
        surface.blit(self.frames[self.current_frame], (x, y))
