import pygame
from settings import *

class Snake:
    def __init__(self):
        self.reset()
        
    def reset(self):
        """Сброс змеи в начальное состояние"""
        self.length = 3
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0
        self.food_collected = 0
        self.consecutive_food = 0
        
    def get_head_position(self):
        """Получить позицию головы змеи"""
        return self.positions[0]
    
    def update_direction(self, direction):
        """Обновить направление движения"""
        # Не позволяем двигаться в противоположном направлении
        if (direction[0] * -1, direction[1] * -1) != self.direction:
            self.direction = direction
    
    def move(self):
        """Движение змеи"""
        head = self.get_head_position()
        x, y = self.direction
        new_x = head[0] + (x * GRID_SIZE)
        new_y = head[1] + (y * GRID_SIZE)
        new_position = (new_x, new_y)
        
        # Проверка выхода за границы
        if (new_x < 0 or new_x >= SCREEN_WIDTH or 
            new_y < 0 or new_y >= SCREEN_HEIGHT):
            return False
        
        # Проверка столкновения с собой
        if new_position in self.positions[1:]:
            return False
        
        self.positions.insert(0, new_position)
        
        # Управление длиной
        if len(self.positions) > self.length:
            self.positions.pop()
            
        return True
    
    def grow(self):
        """Увеличить длину змеи"""
        self.length += 1
        self.food_collected += 1
        self.consecutive_food += 1
        
        # Начисление очков
        self.score += 10
        
        # Бонус за каждые 5 еды подряд
        if self.consecutive_food % 5 == 0:
            self.score += 50
    
    def draw(self, surface):
        """Отрисовка змеи"""
        for i, p in enumerate(self.positions):
            # Голова немного отличается от тела
            if i == 0:
                color = SNAKE_COLOR
            else:
                color = (200, 200, 200)  # Немного темнее для тела
                
            rect = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BACKGROUND_COLOR, rect, 1)  # Обводка