import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('arial.ttf', 25)
# font = pygame.font.SysFont('arial', 25)  # Alternative font

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')

class Obstacle:
    def __init__(self, point, lifetime):
        self.point = point
        self.lifetime = lifetime

# RGB colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)  # Color for obstacles

BLOCK_SIZE = 20
SPEED = 40

class SnakeGameAI:

    def __init__(self, w=640, h=480, num_obstacles=5):
        self.w = w
        self.h = h
        self.num_obstacles = num_obstacles  # Number of obstacles
        # Initialize display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        # Obstacle parameters
        self.min_obstacle_lifetime = 50   # Minimum lifespan in frames
        self.max_obstacle_lifetime = 200  # Maximum lifespan in frames
        self.obstacle_frequency = 100     # Frames between new obstacles
        self.reset()

    def reset(self):
        # Initialize game state
        self.direction = Direction.RIGHT
        self.head = Point(self.w / 2, self.h / 2)
        self.snake = [
            self.head,
            Point(self.head.x - BLOCK_SIZE, self.head.y),
            Point(self.head.x - (2 * BLOCK_SIZE), self.head.y)
        ]
        self.score = 0
        self.food = None
        self.obstacles = []
        self.frame_since_last_obstacle = 0
        self._place_food()
        # self._place_obstacles()  # Obstacles will be placed during the game
        self.frame_iteration = 0

    def _place_food(self):
        """Place food at a random location."""
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)
        # Ensure food doesn't spawn on snake or obstacles
        if self.food in self.snake or self.food in [obs.point for obs in self.obstacles]:
            self._place_food()

    def _place_obstacles(self):
        """Place obstacles with random lifetimes."""
        while len(self.obstacles) < self.num_obstacles:
            x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            point = Point(x, y)
            # Ensure obstacles don't overlap with snake, food, or existing obstacles
            if point not in self.snake and point != self.food and point not in [obs.point for obs in self.obstacles]:
                lifetime = random.randint(self.min_obstacle_lifetime, self.max_obstacle_lifetime)
                self.obstacles.append(Obstacle(point, lifetime))

    def play_step(self, action):
        """Execute one game step."""
        self.frame_iteration += 1
        # 1. Collect user input (handle quit event)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # 2. Move the snake
        distance_to_food_before = self._distance(self.head, self.food)
        self._move(action)  # Update the head position
        self.snake.insert(0, self.head)

        # 3. Check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # 4. Place new food or move snake
        distance_to_food_after = self._distance(self.head, self.food)
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
            # Reward for moving closer to the food
            if distance_to_food_after < distance_to_food_before:
                reward += 0.1
            else:
                reward -= 0.1

        # Update obstacle lifespans and manage obstacles
        for obstacle in self.obstacles:
            obstacle.lifetime -= 1
        # Remove obstacles that have expired
        self.obstacles = [obstacle for obstacle in self.obstacles if obstacle.lifetime > 0]

        # Add new obstacles periodically
        self.frame_since_last_obstacle += 1
        if self.frame_since_last_obstacle >= self.obstacle_frequency:
            self._place_obstacles()
            self.frame_since_last_obstacle = 0

        # 5. Update UI and clock
        self._update_ui()
        self.clock.tick(SPEED)

        # 6. Return reward, game over status, and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        """Check if the snake collides with the wall, itself, or obstacles."""
        if pt is None:
            pt = self.head
        # Hits boundary
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # Hits itself
        if pt in self.snake[1:]:
            return True
        # Hits an obstacle
        if pt in [obstacle.point for obstacle in self.obstacles]:
            return True
        return False

    def _update_ui(self):
        """Update the game's user interface."""
        self.display.fill(BLACK)

        # Draw Snake
        for pt in self.snake:
            pygame.draw.rect(self.display, BLUE1, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLUE2, pygame.Rect(pt.x + 4, pt.y + 4, 12, 12))

        # Draw Food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # Draw Obstacles
        for obstacle in self.obstacles:
            pygame.draw.rect(self.display, GRAY, pygame.Rect(obstacle.point.x, obstacle.point.y, BLOCK_SIZE, BLOCK_SIZE))

        # Draw Score
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        """Move the snake based on the action."""
        # [straight, right, left]
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        # Action mapping
        if np.array_equal(action, [1, 0, 0]):
            # Move straight
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            # Turn right
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:  # [0, 0, 1]
            # Turn left
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

    def _distance(self, point1, point2):
        """Calculate the Manhattan distance between two points."""
        return abs(point1.x - point2.x) + abs(point1.y - point2.y)