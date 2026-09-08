import pygame
import sys
import traceback
from settings import WIDTH, HEIGHT
from game import Game

def main():
    try:
        pygame.init()
        # Initialize mixer for music
        pygame.mixer.init()
        # Use SCALED and RESIZABLE for native Mac fullscreen support
        flags = pygame.SCALED | pygame.RESIZABLE
        screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
        pygame.display.set_caption("GLITCH GUY: It's Not a Bug. It's Computer Graphics.")
        
        game = Game(screen)
        game.run()
    except Exception as e:
        with open("crash_log.txt", "w") as f:
            f.write(traceback.format_exc())
        print("Game crashed! Check crash_log.txt")
        raise e
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
