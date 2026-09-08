import pygame
from settings import *
from transformations import transform_polygon, rotate_about_point

class DogHorse(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = 0
        self.scale = 1.0
        self.draw_dog_horse()
        self.dialogue = ["Where are we going?", "I DON'T KNOW.", "Good. Keep going."]
        self.dialogue_idx = 0

    def draw_dog_horse(self):
        self.image.fill((0,0,0,0))
        # Base horse body
        horse_body = [(10, 30), (50, 30), (50, 50), (10, 50)]
        # Horse head
        horse_head = [(40, 10), (55, 10), (55, 35), (40, 35)]
        # Dog on top
        dog_body = [(20, 15), (35, 15), (35, 30), (20, 30)]
        
        # Apply current transformations
        center = (32, 32)
        
        def apply_transform(poly):
            # Scale
            poly = [(center[0] + (p[0]-center[0])*self.scale, center[1] + (p[1]-center[1])*self.scale) for p in poly]
            # Rotate
            poly = [rotate_about_point(p[0], p[1], self.angle, center[0], center[1]) for p in poly]
            return poly

        pygame.draw.polygon(self.image, (139, 69, 19), apply_transform(horse_body)) # Brown horse
        pygame.draw.polygon(self.image, (139, 69, 19), apply_transform(horse_head))
        pygame.draw.polygon(self.image, (255, 215, 0), apply_transform(dog_body))   # Gold dog

    def set_angle(self, angle):
        self.angle = angle
        self.draw_dog_horse()

    def set_scale(self, scale):
        self.scale = scale
        self.draw_dog_horse()
        
    def next_dialogue(self):
        msg = self.dialogue[self.dialogue_idx]
        self.dialogue_idx = (self.dialogue_idx + 1) % len(self.dialogue)
        return msg
