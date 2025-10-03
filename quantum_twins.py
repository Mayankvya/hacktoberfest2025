"""
Quantum Twins - PyGame prototype (single file)

Controls:
  Arrow keys / WASD - move player 1
  Player 2 automatically mirrors your moves
  R - restart
  Esc - quit

Goal:
  Get both twins (blue & red) to their exits (green & yellow) without touching walls.
"""

import pygame, sys, random

# --- Config ---
CELL = 32
COLS, ROWS = 15, 12
SCREEN_W, SCREEN_H = COLS * CELL, ROWS * CELL + 40
FPS = 30

# Colors
WALL = (40,40,40)
FLOOR = (15,15,20)
P1_COLOR = (60,180,255)   # blue twin
P2_COLOR = (255,80,80)    # red twin
EXIT1_COLOR = (120,255,120)
EXIT2_COLOR = (255,255,100)

class QuantumTwins:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Quantum Twins (PyGame prototype)")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("consolas", 20)
        self.reset()

    def reset(self):
        # Generate random maze-like walls
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        for r in range(ROWS):
            for c in range(COLS):
                if r in (0,ROWS-1) or c in (0,COLS-1):
                    self.grid[r][c] = 1
                elif random.random() < 0.15:
                    self.grid[r][c] = 1

        # Player positions
        self.p1 = [1,1]
        self.p2 = [COLS-2,ROWS-2]

        # Exit positions
        self.exit1 = [COLS-2,1]
        self.exit2 = [1,ROWS-2]

        self.win = False

    def move_player(self, dx,dy):
        # Move P1
        nr, nc = self.p1[1]+dy, self.p1[0]+dx
        if 0<=nr<ROWS and 0<=nc<COLS and self.grid[nr][nc]==0:
            self.p1=[nc,nr]

        # Mirror move for P2 (opposite direction)
        nr2, nc2 = self.p2[1]-dy, self.p2[0]-dx
        if 0<=nr2<ROWS and 0<=nc2<COLS and self.grid[nr2][nc2]==0:
            self.p2=[nc2,nr2]

        # Win check
        if self.p1==self.exit1 and self.p2==self.exit2:
            self.win=True

    def handle_events(self):
        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()
                if e.key==pygame.K_r: self.reset()
                if not self.win:
                    if e.key in (pygame.K_LEFT,pygame.K_a): self.move_player(-1,0)
                    if e.key in (pygame.K_RIGHT,pygame.K_d): self.move_player(1,0)
                    if e.key in (pygame.K_UP,pygame.K_w): self.move_player(0,-1)
                    if e.key in (pygame.K_DOWN,pygame.K_s): self.move_player(0,1)

    def draw(self):
        self.screen.fill((0,0,0))
        for r in range(ROWS):
            for c in range(COLS):
                rect = pygame.Rect(c*CELL, r*CELL, CELL, CELL)
                if self.grid[r][c]==1:
                    pygame.draw.rect(self.screen, WALL, rect)
                else:
                    pygame.draw.rect(self.screen, FLOOR, rect)

        # exits
        pygame.draw.rect(self.screen, EXIT1_COLOR, pygame.Rect(self.exit1[0]*CELL,self.exit1[1]*CELL,CELL,CELL))
        pygame.draw.rect(self.screen, EXIT2_COLOR, pygame.Rect(self.exit2[0]*CELL,self.exit2[1]*CELL,CELL,CELL))

        # players
        pygame.draw.circle(self.screen, P1_COLOR, (self.p1[0]*CELL+CELL//2,self.p1[1]*CELL+CELL//2), CELL//2-4)
        pygame.draw.circle(self.screen, P2_COLOR, (self.p2[0]*CELL+CELL//2,self.p2[1]*CELL+CELL//2), CELL//2-4)

        # HUD
        hud = "R: restart | ESC: quit"
        if self.win: hud = "YOU WIN! 🎉 Press R to restart"
        text = self.font.render(hud,True,(220,220,220))
        self.screen.blit(text,(10,SCREEN_H-30))
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.draw()
            self.clock.tick(FPS)

if __name__=="__main__":
    QuantumTwins().run()
