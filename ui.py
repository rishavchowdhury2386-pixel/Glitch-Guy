import pygame
from settings import *

class UI:
    def __init__(self, surface):
        self.surface = surface
        pygame.font.init()
        self.font = pygame.font.SysFont(FONT_NAME, 24, bold=True)
        self.large_font = pygame.font.SysFont(FONT_NAME, 48, bold=True)

    def draw_hud(self, player, mission_text):
        hud_rect = pygame.Rect(0, 0, WIDTH, 120)
        
        # Draw a nice gradient-like or multi-layer HUD background
        pygame.draw.rect(self.surface, (20, 20, 40), hud_rect)
        pygame.draw.rect(self.surface, (50, 50, 90), hud_rect, 4)
        pygame.draw.line(self.surface, (100, 100, 200), (4, 116), (WIDTH-4, 116), 2)
        
        health_text = self.font.render(f"HEALTH: {player.health}", True, (255, 100, 100))
        score_text = self.font.render(f"SCORE: {player.score}", True, (255, 215, 0))
        weapon_text = self.font.render(f"ABILITY: {player.weapon_mode}", True, (100, 255, 255))
        coords_text = self.font.render(f"POS: ({int(player.x)}, {int(player.y)})", True, (150, 255, 150))
        mission_lbl = self.font.render(f"MISSION: {mission_text}", True, WHITE)

        self.surface.blit(health_text, (20, 15))
        self.surface.blit(score_text, (20, 50))
        
        self.surface.blit(weapon_text, (250, 15))
        self.surface.blit(coords_text, (250, 50))
        
        # Draw mission text on a new row so it has the full screen width
        self.surface.blit(mission_lbl, (20, 85))

    def draw_dialogue(self, name, text):
        box_rect = pygame.Rect(100, HEIGHT - 150, WIDTH - 200, 100)
        pygame.draw.rect(self.surface, (30, 30, 80), box_rect, border_radius=10)
        pygame.draw.rect(self.surface, WHITE, box_rect, 3, border_radius=10)
        
        name_surf = self.font.render(name + ":", True, (255, 215, 0))
        text_surf = self.font.render(text, True, WHITE)
        
        self.surface.blit(name_surf, (120, HEIGHT - 140))
        self.surface.blit(text_surf, (120, HEIGHT - 100))
        
    def draw_message(self, text):
        # Add text shadow for better graphics
        text_surf = self.large_font.render(text, True, (255, 255, 0))
        shadow_surf = self.large_font.render(text, True, (0, 0, 0))
        
        rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
        shadow_rect = text_surf.get_rect(center=(WIDTH//2 + 4, HEIGHT//2 + 4))
        
        self.surface.blit(shadow_surf, shadow_rect)
        self.surface.blit(text_surf, rect)
