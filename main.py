#!/usr/bin/env python3
"""
Главный файл игры "Змейка"
Запуск: python main.py
"""

from game import Game

if __name__ == "__main__":
    print("Запуск игры 'Змейка'...")
    print("Управление: стрелки для движения, ESC для выхода")
    print("Выберите уровень сложности в меню:")
    print("1 - Легкий, 2 - Средний, 3 - Сложный")
    
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        print("Игра завершена")