# GLITCH GUY
"It's Not a Bug. It's Computer Graphics."

A B.Tech Semester 5 Computer Graphics Project demonstrating rendering algorithms, transformations, and clipping within a playable 2D/2.5D action-adventure game!

## Story
The entire Computer Graphics world has broken because the main character, Glitch Guy, accidentally corrupted the Graphics Engine. 
Now houses randomly rotate, circles become monsters, and dogs ride horses! Glitch Guy must repair the Graphics Core.

## Computer Graphics Concepts Implemented
- **Transformations (Module 1):** Translation, Rotation, Scaling, Reflection, Shearing.
- **Rasterization (Module 2):** DDA Line Drawing, Bresenham Line Drawing, Midpoint Circle, Midpoint Ellipse.
- **Polygons (Module 2):** Scan-line fill algorithm.
- **Clipping (Module 2):** Cohen-Sutherland, Liang-Barsky, Sutherland-Hodgman.

## Controls
- **WASD:** Move
- **SHIFT:** Run
- **SPACE:** Dash
- **E:** Interact / Talk
- **Mouse + Left Click:** Aim & Shoot
- **1:** Select DDA Weapon
- **2:** Select Bresenham Weapon
- **R, Q, F, T, H, 4, C:** Mission Specific Ability Buttons
- **P:** Professor Mode (Algorithm inspection)
- **V:** Viva Quiz Mode
- **F11:** Toggle Fullscreen
- **ESC:** Pause

## How to Beat All Levels (Mission Guide)
1. **Find Coordinate (500, 350):** Watch your live `POS: (X, Y)` on the HUD. Walk directly to coordinates 500, 350.
2. **Fix Rotated Horse (Rotation):** Find the Dog on the Horse near the spawn. Stand next to him and press **`R`**.
3. **Talk to Prof. Pixel:** Find the purple NPC near 600, 400. Stand next to him and press **`E`**.
4. **Shrink Giant Zombie (Scaling):** Find the massive green zombie at 1000, 800. Stand next to it and press **`Q`**.
5. **Reflect Security Door (Reflection):** Walk to the red door at 1500, 400. Press **`F`** to apply a reflection matrix and open it.
6. **Translate Broken Bridge (Translation):** Walk to 800, 200. Press **`T`** to translate the bridge pieces back together.
7. **Shear Leaning Tower (Shearing):** Walk to 200, 800. Press **`H`** to apply a shear matrix and fix the tower.
8. **Flood Fill Data Lake (Polygon Fill):** Walk to 1800, 1800. Press **`4`** to flood fill the lake with water pixels.
9. **Clip Laser Barrier (Clipping):** Walk to 1500, 1000. Press **`C`** to apply Cohen-Sutherland clipping and break the laser barrier.
10. **Defeat Glitch Lord (Final Boss):** Equip your Bresenham pixel gun (Press `2`). Find the Glitch Lord at 1200, 1200. Left Click to shoot him with pixel-perfect lines until the Graphics Core is restored!

## Installation & Running
Ensure you have Python 3 installed.
```bash
python3 -m pip install pygame-ce
python3 main.py
```
# Glitch_Guy
