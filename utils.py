import pygame

def clamp(val, min_val, max_val):
    return max(min_val, min(val, max_val))

def draw_beveled_rect(surface, color, rect, width=0, border_radius=0):
    """Draws a rectangle with a highlighted top/left and shaded bottom/right to look 3D."""
    pygame.draw.rect(surface, color, rect, width, border_radius)
    
    if width == 0:
        # Calculate highlight and shadow colors
        r, g, b = color[:3] if len(color) >= 3 else (0,0,0)
        hl_color = (min(255, r + 70), min(255, g + 70), min(255, b + 70))
        sh_color = (max(0, r - 70), max(0, g - 70), max(0, b - 70))
        
        # Highlight (top and left) - Draw thicker for more 3D pop
        pygame.draw.line(surface, hl_color, rect.topleft, rect.topright, 3)
        pygame.draw.line(surface, hl_color, rect.topleft, rect.bottomleft, 3)
        
        # Shadow (bottom and right)
        pygame.draw.line(surface, sh_color, rect.bottomleft, rect.bottomright, 3)
        pygame.draw.line(surface, sh_color, rect.topright, rect.bottomright, 3)
        
        # Inner bevel for extra depth
        hl_inner = (min(255, r + 30), min(255, g + 30), min(255, b + 30))
        pygame.draw.line(surface, hl_inner, (rect.left+3, rect.top+3), (rect.right-3, rect.top+3), 2)
        pygame.draw.line(surface, hl_inner, (rect.left+3, rect.top+3), (rect.left+3, rect.bottom-3), 2)
