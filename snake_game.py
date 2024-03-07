import pygame
import random
from enum import Enum
from collections import namedtuple

pygame.init()
font = pygame.font.SysFont('arial', 25)

Point = namedtuple('Point', 'x, y')

# rgb colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 30
SPEED = 10


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


class SnakeGame:
    
    def __init__(self, w=640, h=480):
        self.w = w
        self.h = h
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        # Load images
        self.food_img = pygame.image.load('Resources/apple.png').convert_alpha()
        self.food_img = pygame.transform.scale(self.food_img, (BLOCK_SIZE, BLOCK_SIZE))

        self.snake_head_img = pygame.image.load('Resources/snake_head.png').convert_alpha()
        self.snake_head_img = pygame.transform.scale(self.snake_head_img, (BLOCK_SIZE, BLOCK_SIZE))

        self.snake_body_img = pygame.image.load('Resources/snake_body.png').convert_alpha()
        self.snake_body_img = pygame.transform.scale(self.snake_body_img, (BLOCK_SIZE, BLOCK_SIZE))

        self.snake_curve_img = pygame.image.load('Resources/snake_curve.png').convert_alpha()
        self.snake_curve_img = pygame.transform.scale(self.snake_curve_img, (BLOCK_SIZE, BLOCK_SIZE))

        self.snake_tail_img = pygame.image.load('Resources/snake_tail.png').convert_alpha()
        self.snake_tail_img = pygame.transform.scale(self.snake_tail_img, (BLOCK_SIZE, BLOCK_SIZE))
        
        # init game state
        self.direction = random.choice([Direction.RIGHT, Direction.UP, Direction.DOWN])
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        y = random.randint(0, (self.h-BLOCK_SIZE)//BLOCK_SIZE)*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def play_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN
        
        # 2. move
        self._move(self.direction)  # update the head
        self.snake.insert(0, self.head)
        
        # 3. check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
            
        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            self._place_food()
        else:
            self.snake.pop()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return game_over, self.score
    
    def _is_collision(self):
        # hits boundary
        # if self.head.x > self.w-BLOCK_SIZE or self.head.x < 0 or self.head.y > self.h-BLOCK_SIZE or self.head.y < 0:
        #     return True
        # hits itself
        if self.head in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.display.fill(BLACK)

        # Draw snake head
        snake_head_rect = pygame.Rect(self.snake[0].x, self.snake[0].y, BLOCK_SIZE, BLOCK_SIZE)
        match self.direction:
            case Direction.RIGHT:
                self.display.blit(self.snake_head_img, snake_head_rect)
            case Direction.UP:
                self.display.blit(pygame.transform.rotate(self.snake_head_img, 90), snake_head_rect)
            case Direction.LEFT:
                self.display.blit(pygame.transform.rotate(self.snake_head_img, 180), snake_head_rect)
            case Direction.DOWN:
                self.display.blit(pygame.transform.rotate(self.snake_head_img, 270), snake_head_rect)

        # Draw snake body
        for b in range(1, len(self.snake)-1):
            x_avg = (self.snake[b-1].x + self.snake[b+1].x) / 2
            y_avg = (self.snake[b-1].y + self.snake[b+1].y) / 2
            snake_body_rect = pygame.Rect(self.snake[b].x, self.snake[b].y, BLOCK_SIZE, BLOCK_SIZE)
            if (self.snake[b-1].y == self.snake[b].y) and (self.snake[b].y == self.snake[b+1].y):
                self.display.blit(self.snake_body_img, snake_body_rect)
            elif (self.snake[b-1].x == self.snake[b].x) and (self.snake[b].x == self.snake[b+1].x):
                self.display.blit(pygame.transform.rotate(self.snake_body_img, 90), snake_body_rect)
            elif (x_avg < self.snake[b].x) and (y_avg < self.snake[b].y):
                self.display.blit(self.snake_curve_img, snake_body_rect)
            elif (self.snake[b-1].x == self.snake[b].x) and (self.snake[b].x == self.snake[b+1].x):
                self.display.blit(pygame.transform.rotate(self.snake_body_img, 90), snake_body_rect)
            elif (x_avg < self.snake[b].x) and (y_avg > self.snake[b].y):
                self.display.blit(pygame.transform.rotate(self.snake_curve_img, 90), snake_body_rect)
            elif (x_avg > self.snake[b].x) and (y_avg > self.snake[b].y):
                self.display.blit(pygame.transform.rotate(self.snake_curve_img, 180), snake_body_rect)
            elif (x_avg > self.snake[b].x) and (y_avg < self.snake[b].y):
                self.display.blit(pygame.transform.rotate(self.snake_curve_img, 270), snake_body_rect)

        # Draw snake tail
        snake_tail_rect = pygame.Rect(self.snake[-1].x, self.snake[-1].y, BLOCK_SIZE, BLOCK_SIZE)
        if (self.snake[-1].x < self.snake[-2].x) and (self.snake[-1].y == self.snake[-2].y):
            self.display.blit(self.snake_tail_img, snake_tail_rect)
        elif (self.snake[-1].x == self.snake[-2].x) and (self.snake[-1].y > self.snake[-2].y):
            self.display.blit(pygame.transform.rotate(self.snake_tail_img, 90), snake_tail_rect)
        elif (self.snake[-1].x > self.snake[-2].x) and (self.snake[-1].y == self.snake[-2].y):
            self.display.blit(pygame.transform.rotate(self.snake_tail_img, 180), snake_tail_rect)
        elif (self.snake[-1].x == self.snake[-2].x) and (self.snake[-1].y < self.snake[-2].y):
            self.display.blit(pygame.transform.rotate(self.snake_tail_img, 270), snake_tail_rect)

        # Draw food
        food_rect = pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE)
        self.display.blit(self.food_img, food_rect)

        # Draw score
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])

        # Update the full display surface
        pygame.display.flip()
        
    def _move(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
            if x >= self.w:
                x = 0
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
            if x < 0:
                x = self.w - BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
            if y >= self.h:
                y = 0
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
            if y < 0:
                y = self.h - BLOCK_SIZE
            
        self.head = Point(x, y)
            

if __name__ == '__main__':
    game = SnakeGame(w=900, h=600)
    # game loop
    while True:
        is_game_over, score = game.play_step()
        if is_game_over:
            break
        
    print('Final Score', score)
    pygame.quit()
