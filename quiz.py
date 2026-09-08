import pygame
from settings import *

class Quiz:
    def __init__(self, surface):
        self.surface = surface
        pygame.font.init()
        self.font = pygame.font.SysFont(FONT_NAME, 28)
        self.questions = [
            {
                "q": "What is rasterization?",
                "opts": ["Converting primitives to pixels", "A 3D modeling technique"],
                "ans": 0
            },
            {
                "q": "What are homogeneous coordinates?",
                "opts": ["A way to represent 2D points in 3D for matrix math", "A color space"],
                "ans": 0
            },
            {
                "q": "Why does transformation order matter?",
                "opts": ["Matrix multiplication is not commutative", "It doesn't matter"],
                "ans": 0
            },
            {
                "q": "What is the DDA step formula?",
                "opts": ["steps = max(|dx|, |dy|)", "steps = dx + dy"],
                "ans": 0
            },
            {
                "q": "What is Bresenham's decision parameter?",
                "opts": ["p = 2dy - dx", "p = mx + c"],
                "ans": 0
            }
        ]
        self.current = 0
        
    def get_current_question(self):
        if self.current < len(self.questions):
            return self.questions[self.current]
        return None
        
    def answer(self, idx):
        q = self.get_current_question()
        if q:
            correct = q["ans"] == idx
            self.current += 1
            return correct
        return False
        
    def draw(self):
        q = self.get_current_question()
        if q:
            self.surface.fill(DARK_GRAY)
            title = self.font.render("VIVA MODE", True, YELLOW)
            self.surface.blit(title, (WIDTH//2 - title.get_width()//2, 100))
            
            q_text = self.font.render(q["q"], True, WHITE)
            self.surface.blit(q_text, (100, 250))
            
            for i, opt in enumerate(q["opts"]):
                opt_text = self.font.render(f"{i+1}. {opt}", True, CYAN)
                self.surface.blit(opt_text, (120, 320 + i*50))
                
            hint = self.font.render("Press 1 or 2 to answer", True, GRAY)
            self.surface.blit(hint, (WIDTH//2 - hint.get_width()//2, 500))
        else:
            self.surface.fill(DARK_GRAY)
            text = self.font.render("VIVA COMPLETED!", True, GREEN)
            self.surface.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2))
