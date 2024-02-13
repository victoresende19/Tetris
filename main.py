import pygame
import random
import asyncio

# Configurações do jogo
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Definição das peças
pieces = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1], [1, 1]],  # O
    [[1, 1, 0], [0, 1, 1]]  # Z
]

piece_colors = [CYAN, PURPLE, ORANGE, BLUE, GREEN, YELLOW, RED]

# Classe do jogo
class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.fall_time = 0
        self.fall_speed = 0.5  # Tempo em segundos entre cada movimento automático para baixo

    def new_piece(self):
        piece = random.choice(pieces)
        return piece, 0, GRID_WIDTH // 2 - len(piece[0]) // 2

    def draw_grid(self):
        for y, row in enumerate(self.grid):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, piece_colors[val - 1], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                    pygame.draw.rect(self.screen, WHITE, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def draw_piece(self):
        for y, row in enumerate(self.current_piece[0]):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(self.screen, piece_colors[self.current_piece[0][y][x] - 1], ((self.current_piece[2] + x) * BLOCK_SIZE, (self.current_piece[1] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                    pygame.draw.rect(self.screen, WHITE, ((self.current_piece[2] + x) * BLOCK_SIZE, (self.current_piece[1] + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

    def valid_space(self, piece, offset):
        for y, row in enumerate(piece):
            for x, val in enumerate(row):
                if val:
                    if (offset[0] + y) < 0 or (offset[0] + y) >= GRID_HEIGHT or (offset[1] + x) < 0 or (offset[1] + x) >= GRID_WIDTH or self.grid[offset[0] + y][offset[1] + x]:
                        return False
        return True

    def place_piece(self):
        for y, row in enumerate(self.current_piece[0]):
            for x, val in enumerate(row):
                if val:
                    self.grid[self.current_piece[1] + y][self.current_piece[2] + x] = val

    def rotate_piece(self):
        rotated_piece = [list(row) for row in zip(*self.current_piece[0][::-1])]
        if self.valid_space(rotated_piece, (self.current_piece[1], self.current_piece[2])):
            self.current_piece = (rotated_piece, self.current_piece[1], self.current_piece[2])

    def clear_rows(self):
        rows_to_clear = [i for i, row in enumerate(self.grid) if 0 not in row]
        for row in rows_to_clear:
            del self.grid[row]
            self.grid.insert(0, [0] * GRID_WIDTH)

    async def run(self):
        running = True
        while running:
            self.screen.fill(BLACK)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.current_piece = (self.current_piece[0], self.current_piece[1], self.current_piece[2] - 1)
                        if not self.valid_space(self.current_piece[0], (self.current_piece[1], self.current_piece[2])):
                            self.current_piece = (self.current_piece[0], self.current_piece[1], self.current_piece[2] + 1)
                    elif event.key == pygame.K_RIGHT:
                        self.current_piece = (self.current_piece[0], self.current_piece[1], self.current_piece[2] + 1)
                        if not self.valid_space(self.current_piece[0], (self.current_piece[1], self.current_piece[2])):
                            self.current_piece = (self.current_piece[0], self.current_piece[1], self.current_piece[2] - 1)
                    elif event.key == pygame.K_DOWN:
                        self.current_piece = (self.current_piece[0], self.current_piece[1] + 1, self.current_piece[2])
                        if not self.valid_space(self.current_piece[0], (self.current_piece[1], self.current_piece[2])):
                            self.current_piece = (self.current_piece[0], self.current_piece[1] - 1, self.current_piece[2])
                            self.place_piece()
                            self.clear_rows()
                            self.current_piece = self.new_piece()
                    elif event.key == pygame.K_UP:
                        self.rotate_piece()

            self.fall_time += self.clock.get_rawtime()
            self.clock.tick()
            if self.fall_time / 1000 > self.fall_speed:
                self.current_piece = (self.current_piece[0], self.current_piece[1] + 1, self.current_piece[2])
                if not self.valid_space(self.current_piece[0], (self.current_piece[1], self.current_piece[2])):
                    self.current_piece = (self.current_piece[0], self.current_piece[1] - 1, self.current_piece[2])
                    self.place_piece()
                    self.clear_rows()
                    self.current_piece = self.new_piece()
                self.fall_time = 0

            self.draw_grid()
            self.draw_piece()

            pygame.display.update()
            await asyncio.sleep(0)
            
            if not running:
                pygame.quit()


pygame.init()
game = Tetris()
asyncio.run(game.run())
