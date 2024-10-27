import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
# font = pygame.font.SysFont('arial', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

# RGB colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GRAY = (169, 169, 169)  # Color for obstacles

BLOCK_SIZE = 20
SPEED = 20

class SnakeGame:
    
    def _init_(self, w=640, h=480, num_obstacles=5):
        self.w = w
        self.h = h
        self.num_obstacles = num_obstacles  # Number of obstacles
        # Init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
        
    def reset(self):
        # Init game state
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self.obstacles = []  # Initialize obstacles list
        self._place_food()
        self._place_obstacles()
        
    def _place_obstacles(self):
        self.obstacles = []
        while len(self.obstacles) < self.num_obstacles:
            x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
            y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
            point = Point(x, y)
            # Ensure obstacles don't overlap with snake or food
            if point not in self.snake and point != self.food and point not in self.obstacles:
                self.obstacles.append(point)

    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        # Ensure food doesn't spawn on snake or obstacles
        if self.food in self.snake or self.food in self.obstacles:
            self._place_food()
        
    def play_step(self):
        # 1. Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN
        
        # 2. Move
        self._move(self.direction)  # Update the head
        self.snake.insert(0, self.head)
        
        # 3. Check if game over
        game_over = False
        # Modified condition to include obstacle collision
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. Place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. Return game over and score
        return game_over, self.score
    
    def _is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # Hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # Hits itself
        if pt in self.snake[1:]:
            return True
        # Hits obstacle
        if pt in self.obstacles:
            return True
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)
        
        # Draw Snake
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x+4, pt.y+4, 12, 12))
            
        # Draw Food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw Obstacles
        for pt in self.obstacles:
            pygame.draw.rect(self.display, GRAY, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
        
        # Draw Score
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            

if __name__ == '_main_':
    game = SnakeGame()

    # Game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score', score)
        
    pygame.quit()