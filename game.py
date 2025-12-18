import pygame
import sys
from snake import Snake
from food import Food
from sounds import SoundManager
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        self.snake = Snake()
        self.food = Food()
        self.sound_manager = SoundManager()
        self.difficulty = "medium"
        self.game_state = "menu"  # menu, playing, game_over
        self.running = True
        self.high_score = 0
        
    def handle_events(self):
        """Обработка событий"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "playing":
                    if event.key == pygame.K_UP:
                        self.snake.update_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        self.snake.update_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        self.snake.update_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        self.snake.update_direction(RIGHT)
                    elif event.key == pygame.K_ESCAPE:
                        self.show_menu()
                        
                elif self.game_state == "menu":
                    if event.key == pygame.K_1:
                        self.difficulty = "easy"
                        self.sound_manager.play_menu()
                        self.start_game()
                    elif event.key == pygame.K_2:
                        self.difficulty = "medium"
                        self.sound_manager.play_menu()
                        self.start_game()
                    elif event.key == pygame.K_3:
                        self.difficulty = "hard"
                        self.sound_manager.play_menu()
                        self.start_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                        
                elif self.game_state == "game_over":
                    if event.key == pygame.K_SPACE:
                        self.sound_manager.play_menu()
                        self.show_menu()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
    
    def start_game(self):
        """Начало новой игры"""
        self.snake.reset()
        self.food.randomize_position()
        self.game_state = "playing"
        
    def show_menu(self):
        """Показать меню"""
        self.game_state = "menu"
        self.sound_manager.stop_music()
        
    def update(self):
        """Обновление состояния игры"""
        if self.game_state != "playing":
            return
            
        # Движение змеи
        if not self.snake.move():
            self.game_over()
            return
            
        # Проверка столкновения с едой
        if self.snake.get_head_position() == self.food.position:
            self.snake.grow()
            self.sound_manager.play_eat()
            self.food.randomize_position()
            
            # Проверка, что еда не появилась на змее
            while self.food.position in self.snake.positions:
                self.food.randomize_position()
        
    def game_over(self):
        """Завершение игры"""
        self.game_state = "game_over"
        self.high_score = max(self.high_score, self.snake.score)
        self.sound_manager.play_crash()
        self.sound_manager.stop_music()
        
    def get_game_speed(self):
        """Получить скорость игры"""
        return DIFFICULTY[self.difficulty]
        
    def draw_menu(self):
        """Отрисовка меню"""
        self.screen.fill(BACKGROUND_COLOR)
        
        title = self.big_font.render('SNAKE GAME', True, SNAKE_COLOR)
        easy = self.font.render('1 - Easy', True, TEXT_COLOR)
        medium = self.font.render('2 - Medium', True, TEXT_COLOR)
        hard = self.font.render('3 - Hard', True, TEXT_COLOR)
        instruction = self.font.render('Press ESC to quit', True, TEXT_COLOR)
        
        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))
        self.screen.blit(easy, (SCREEN_WIDTH // 2 - easy.get_width() // 2, 250))
        self.screen.blit(medium, (SCREEN_WIDTH // 2 - medium.get_width() // 2, 300))
        self.screen.blit(hard, (SCREEN_WIDTH // 2 - hard.get_width() // 2, 350))
        self.screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 450))
        
    def draw_playing(self):
        """Отрисовка игрового процесса"""
        self.screen.fill(BACKGROUND_COLOR)
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Отображение счета
        score_text = self.font.render(f'Score: {self.snake.score}', True, TEXT_COLOR)
        self.screen.blit(score_text, (10, 10))
        
        # Отображение уровня сложности
        diff_text = self.font.render(f'Difficulty: {self.difficulty}', True, TEXT_COLOR)
        self.screen.blit(diff_text, (10, 50))
        
    def draw_game_over(self):
        """Отрисовка экрана завершения игры"""
        self.screen.fill(BACKGROUND_COLOR)
        
        game_over = self.big_font.render('GAME OVER', True, GAME_OVER_COLOR)
        score = self.font.render(f'Score: {self.snake.score}', True, TEXT_COLOR)
        high_score = self.font.render(f'High Score: {self.high_score}', True, TEXT_COLOR)
        restart = self.font.render('Press SPACE to restart or ESC to quit', True, TEXT_COLOR)
        
        self.screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, 150))
        self.screen.blit(score, (SCREEN_WIDTH // 2 - score.get_width() // 2, 250))
        self.screen.blit(high_score, (SCREEN_WIDTH // 2 - high_score.get_width() // 2, 300))
        self.screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, 350))
        
    def draw(self):
        """Отрисовка игры"""
        if self.game_state == "menu":
            self.draw_menu()
        elif self.game_state == "playing":
            self.draw_playing()
        elif self.game_state == "game_over":
            self.draw_game_over()
            
        pygame.display.update()
        
    def run(self):
        """Главный игровой цикл"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.get_game_speed())