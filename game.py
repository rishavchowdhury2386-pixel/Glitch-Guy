import pygame
import sys
import math
import random
from settings import *
from player import Player
from enemy import Enemy
from npc import NPC
from dog_horse import DogHorse
from world import World
from camera import Camera
from ui import UI
from quiz import Quiz
from utils import draw_beveled_rect

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.state = MAIN_MENU
        self.is_fullscreen = False
        
        self.world = World()
        self.camera = Camera(MAP_WIDTH, MAP_HEIGHT)
        self.player = Player(400, 300)
        
        self.dog_horse = DogHorse(200, 200)
        self.npc1 = NPC(600, 400, "Prof. Pixel", "WHY IS MY CIRCLE SQUARE?!")
        self.npc2 = NPC(100, 500, "Mr. Polygon", "I used to have 6 sides. Now 17. Help.")
        self.boss = NPC(1200, 1200, "Glitch Lord", "I HAVE CORRUPTED THE CORE!")
        
        self.giant_zombie = Enemy(1000, 800, "zombie")
        self.giant_zombie.image = pygame.transform.scale(self.giant_zombie.image, (120, 120))
        self.giant_zombie.rect = self.giant_zombie.image.get_rect(topleft=(1000, 800))
        
        self.enemies = [Enemy(800, 600, "zombie"), Enemy(300, 700, "circle"), self.giant_zombie]
        
        self.ui = UI(self.screen)
        self.quiz = Quiz(self.screen)
        
        self.missions = [
            {"desc": "Find Coordinate (500, 350)", "type": "coord", "target": (500, 350)},
            {"desc": "Fix Rotated Horse (Press R near it)", "type": "rotate", "target": self.dog_horse},
            {"desc": "Talk to Prof. Pixel (Press E)", "type": "talk", "target": self.npc1},
            {"desc": "Shrink Giant Zombie (Press Q near it)", "type": "scale", "target": self.giant_zombie},
            {"desc": "Reflect Security Door (Press F at 1500, 400)", "type": "reflect", "target": (1500, 400)},
            {"desc": "Translate Broken Bridge (Press T at 800, 200)", "type": "translate", "target": (800, 200)},
            {"desc": "Shear Leaning Tower (Press H at 200, 800)", "type": "shear", "target": (200, 800)},
            {"desc": "Flood Fill the Data Lake (Press 4 at 1800, 1800)", "type": "fill", "target": (1800, 1800)},
            {"desc": "Clip the Laser Barrier (Press C at 1500, 1000)", "type": "clip", "target": (1500, 1000)},
            {"desc": "Defeat Glitch Lord (Shoot him!)", "type": "boss", "target": self.boss}
        ]
        self.current_mission = 0
        self.message = ""
        self.message_timer = 0
        self.dialogue = None
        self.menu_time = 0
        self.grid_offset = 0
        
        # Level states
        self.temple_door_open = False
        self.bridge_fixed = False
        self.tower_fixed = False
        self.lake_filled = False
        self.barrier_clipped = False
        self.boss_health = 100

        try:
            pygame.mixer.music.load("theme.wav")
            pygame.mixer.music.play(-1)
        except:
            pass

    def toggle_fullscreen(self):
        self.is_fullscreen = not self.is_fullscreen
        if self.is_fullscreen:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.ui = UI(self.screen)
        self.quiz = Quiz(self.screen)

    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    self.toggle_fullscreen()
                    
                if self.state == MAIN_MENU:
                    if event.key == pygame.K_RETURN:
                        self.state = EXPLORATION
                        
                elif self.state == EXPLORATION:
                    if event.key == pygame.K_1: self.player.weapon_mode = "DDA"
                    elif event.key == pygame.K_2: self.player.weapon_mode = "BRESENHAM"
                    elif event.key == pygame.K_p: self.state = PROFESSOR_MODE
                    elif event.key == pygame.K_v: self.state = QUIZ
                    elif event.key == pygame.K_ESCAPE: self.state = PAUSED
                    elif event.key == pygame.K_e: self.interact()
                    
                    # Mission specific keys
                    if self.current_mission < len(self.missions):
                        mtype = self.missions[self.current_mission]["type"]
                        tx, ty = 0, 0
                        if type(self.missions[self.current_mission]["target"]) == tuple:
                            tx, ty = self.missions[self.current_mission]["target"]
                        
                        if event.key == pygame.K_r and mtype == "rotate":
                            self.dog_horse.set_angle(0)
                            self.complete_mission()
                        elif event.key == pygame.K_q and mtype == "scale":
                            if math.hypot(self.player.x - self.giant_zombie.rect.x, self.player.y - self.giant_zombie.rect.y) < 150:
                                self.giant_zombie.image = pygame.transform.scale(self.giant_zombie.image, (40, 40))
                                self.complete_mission()
                        elif event.key == pygame.K_f and mtype == "reflect":
                            if math.hypot(self.player.x - tx, self.player.y - ty) < 150:
                                self.temple_door_open = True
                                self.complete_mission()
                        elif event.key == pygame.K_t and mtype == "translate":
                            if math.hypot(self.player.x - tx, self.player.y - ty) < 150:
                                self.bridge_fixed = True
                                self.complete_mission()
                        elif event.key == pygame.K_h and mtype == "shear":
                            if math.hypot(self.player.x - tx, self.player.y - ty) < 150:
                                self.tower_fixed = True
                                self.complete_mission()
                        elif event.key == pygame.K_4 and mtype == "fill":
                            if math.hypot(self.player.x - tx, self.player.y - ty) < 200:
                                self.lake_filled = True
                                self.complete_mission()
                        elif event.key == pygame.K_c and mtype == "clip":
                            if math.hypot(self.player.x - tx, self.player.y - ty) < 200:
                                self.barrier_clipped = True
                                self.complete_mission()
                        
                elif self.state == QUIZ:
                    if event.key == pygame.K_1:
                        if self.quiz.answer(0): self.player.score += 100
                        else: self.player.score -= 25
                    elif event.key == pygame.K_2:
                        if self.quiz.answer(1): self.player.score += 100
                        else: self.player.score -= 25
                    elif event.key == pygame.K_ESCAPE: self.state = EXPLORATION
                        
                elif self.state == PAUSED or self.state == PROFESSOR_MODE or self.state == VICTORY:
                    if event.key == pygame.K_ESCAPE:
                        if self.state == VICTORY:
                            pygame.quit()
                            sys.exit()
                        self.state = EXPLORATION
                        
            if event.type == pygame.MOUSEBUTTONDOWN and self.state == EXPLORATION:
                if event.button == 1:
                    mx, my = pygame.mouse.get_pos()
                    self.player.shoot(mx, my, self.camera)
                    
                    # Boss hit detection
                    if self.current_mission < len(self.missions) and self.missions[self.current_mission]["type"] == "boss":
                        cam_x, cam_y = self.camera.camera.x, self.camera.camera.y
                        world_mx = mx - cam_x
                        world_my = my - cam_y
                        if self.boss.rect.collidepoint(world_mx, world_my):
                            self.boss_health -= 25
                            self.boss.image.fill((255,0,0)) # Flash red
                            if self.boss_health <= 0:
                                self.state = VICTORY

    def interact(self):
        dist_dh = math.hypot(self.player.x - self.dog_horse.rect.x, self.player.y - self.dog_horse.rect.y)
        dist_npc1 = math.hypot(self.player.x - self.npc1.rect.x, self.player.y - self.npc1.rect.y)
        
        if dist_dh < 100:
            self.dialogue = ("Dog", self.dog_horse.next_dialogue())
            if self.dog_horse.angle == 0 and self.current_mission < len(self.missions) and self.missions[self.current_mission]["type"] == "rotate":
                self.dog_horse.set_angle(90)
                self.dialogue = ("Dog", "Hey! My horse has been rotated. Fix it. (Press R)")
        elif dist_npc1 < 100:
            self.dialogue = (self.npc1.name, self.npc1.dialogue)
            if self.current_mission < len(self.missions) and self.missions[self.current_mission]["type"] == "talk" and self.missions[self.current_mission]["target"] == self.npc1:
                self.complete_mission()
        else:
            self.dialogue = None

    def complete_mission(self):
        self.message = "MISSION COMPLETED!"
        self.message_timer = FPS * 2
        self.player.score += 100
        self.current_mission += 1

    def update(self):
        if self.state == MAIN_MENU:
            self.menu_time += 0.05
            self.grid_offset = (self.grid_offset + 2) % 64
            
        elif self.state == EXPLORATION:
            self.player.update()
            self.camera.update(self.player)
            
            if self.current_mission < len(self.missions) and self.missions[self.current_mission]["type"] == "coord":
                tx, ty = self.missions[self.current_mission]["target"]
                if math.hypot(self.player.x - tx, self.player.y - ty) < 50:
                    self.complete_mission()
                    
            if self.message_timer > 0:
                self.message_timer -= 1
            else:
                self.message = ""
                
            # Reset boss color if it was hit
            if self.boss_health > 0 and self.boss.image.get_at((5,5)) == (255,0,0,255):
                draw_beveled_rect(self.boss.image, PURPLE, pygame.Rect(10, 15, 20, 20), border_radius=4)

    def draw_innovative_menu(self):
        self.screen.fill((10, 10, 30))
        for i in range(-64, HEIGHT, 64):
            y = i + self.grid_offset
            pygame.draw.line(self.screen, (0, 255, 255), (0, y), (WIDTH, y), 1)
        for i in range(0, WIDTH, 64):
            pygame.draw.line(self.screen, (255, 0, 255), (i, 0), (i, HEIGHT), 1)
            
        title_scale = 1.0 + 0.05 * math.sin(self.menu_time)
        title_color = (255, max(100, int(155 + 100*math.sin(self.menu_time))), 0)
        
        font = pygame.font.SysFont(FONT_NAME, int(80 * title_scale), bold=True)
        title_surf = font.render("GLITCH GUY", True, title_color)
        shadow_surf = font.render("GLITCH GUY", True, (0, 0, 0))
        
        rect = title_surf.get_rect(center=(WIDTH//2, HEIGHT//3))
        shadow_rect = title_surf.get_rect(center=(WIDTH//2 + 5, HEIGHT//3 + 5))
        
        self.screen.blit(shadow_surf, shadow_rect)
        self.screen.blit(title_surf, rect)
        
        sub_font = pygame.font.SysFont(FONT_NAME, 30)
        sub_surf = sub_font.render("It's Not a Bug. It's Computer Graphics.", True, WHITE)
        self.screen.blit(sub_surf, sub_surf.get_rect(center=(WIDTH//2, HEIGHT//2)))
        
        if int(self.menu_time * 2) % 2 == 0:
            start_surf = sub_font.render("[ PRESS ENTER TO START ]", True, (0, 255, 0))
            self.screen.blit(start_surf, start_surf.get_rect(center=(WIDTH//2, HEIGHT - 150)))
            
        fs_surf = pygame.font.SysFont(FONT_NAME, 20).render("F11: Toggle Fullscreen", True, GRAY)
        self.screen.blit(fs_surf, (20, HEIGHT - 40))

    def draw(self):
        if self.state == MAIN_MENU:
            self.draw_innovative_menu()
            
        elif self.state == EXPLORATION:
            self.world.draw(self.screen, self.camera)
            
            # Level Objects
            if not self.temple_door_open:
                door_rect = self.camera.apply_rect(pygame.Rect(1500, 400, 100, 100))
                draw_beveled_rect(self.screen, (200, 50, 50), door_rect, border_radius=10)
                
            bridge_rect = self.camera.apply_rect(pygame.Rect(800, 200, 100, 100))
            if self.bridge_fixed:
                draw_beveled_rect(self.screen, (150, 75, 0), bridge_rect)
            else:
                draw_beveled_rect(self.screen, (150, 75, 0), self.camera.apply_rect(pygame.Rect(850, 250, 100, 100))) # Broken state
                
            tower_rect = self.camera.apply_rect(pygame.Rect(200, 800, 80, 200))
            if self.tower_fixed:
                draw_beveled_rect(self.screen, (100, 100, 100), tower_rect)
            else:
                pygame.draw.polygon(self.screen, (100, 100, 100), [
                    self.camera.apply_point((280, 800)), self.camera.apply_point((360, 800)), 
                    self.camera.apply_point((280, 1000)), self.camera.apply_point((200, 1000))
                ]) # Sheared state
                
            lake_rect = self.camera.apply_rect(pygame.Rect(1700, 1700, 200, 200))
            if self.lake_filled:
                pygame.draw.ellipse(self.screen, (0, 100, 255), lake_rect)
            else:
                pygame.draw.ellipse(self.screen, (0, 100, 255), lake_rect, 2) # Empty outline
                
            laser_rect = self.camera.apply_rect(pygame.Rect(1400, 950, 20, 200))
            if not self.barrier_clipped:
                pygame.draw.rect(self.screen, RED, laser_rect)
            
            # Entities
            self.screen.blit(self.dog_horse.image, self.camera.apply_rect(self.dog_horse.rect))
            self.screen.blit(self.npc1.image, self.camera.apply_rect(self.npc1.rect))
            self.screen.blit(self.npc2.image, self.camera.apply_rect(self.npc2.rect))
            self.screen.blit(self.boss.image, self.camera.apply_rect(self.boss.rect))
            
            for enemy in self.enemies:
                self.screen.blit(enemy.image, self.camera.apply_rect(enemy.rect))
                
            self.screen.blit(self.player.image, self.camera.apply_rect(self.player.rect))
            self.player.draw_projectiles(self.screen, self.camera)
            
            m_desc = self.missions[self.current_mission]["desc"] if self.current_mission < len(self.missions) else "All Done!"
            self.ui.draw_hud(self.player, m_desc)
            
            if self.dialogue:
                self.ui.draw_dialogue(self.dialogue[0], self.dialogue[1])
            if self.message:
                self.ui.draw_message(self.message)
                
        elif self.state == QUIZ:
            self.quiz.draw()
            
        elif self.state == PAUSED:
            self.screen.fill((0,0,0, 128))
            self.ui.draw_message("PAUSED - Press ESC to resume")
            
        elif self.state == VICTORY:
            self.screen.fill((20, 80, 20))
            self.ui.draw_message("GRAPHICS CORE RESTORED! (ESC to exit)")
            
        pygame.display.flip()
