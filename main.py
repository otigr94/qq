#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GTA5 RP AutoFishing Bot
Автоматический бот для рыбалки в GTA 5 RolePlay серверах
Поддерживает: Majestic, Rage, RedLine, Diamond и другие
"""

import pyautogui
import time
import cv2
import numpy as np
from datetime import datetime
import json
import os
from pathlib import Path
import logging
from config import Config
from fishing_detector import FishingDetector
from statistics import Statistics

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fishing_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AutoFishingBot:
    def __init__(self):
        self.config = Config()
        self.detector = FishingDetector()
        self.stats = Statistics()
        self.is_running = False
        self.total_fish = 0
        self.start_time = None
        
        logger.info("🎣 GTA5 RP AutoFishing Bot инициализирован")
        logger.info(f"Режим: {self.config.MODE}")
        logger.info(f"Задержка клика: {self.config.CLICK_DELAY} мс")
    
    def start_fishing(self):
        """Начать рыбалку"""
        self.is_running = True
        self.start_time = datetime.now()
        logger.info("🟢 Рыбалка началась! Нажми Q для остановки...")
        print("\n" + "="*50)
        print("🎣 АВТОБОТ ДЛЯ РЫБАЛКИ GTA5 RP ЗАПУЩЕН")
        print("="*50)
        print(f"Режим: {self.config.MODE}")
        print(f"Нажми 'Q' чтобы остановить бота")
        print("="*50 + "\n")
        
        fish_count = 0
        
        try:
            while self.is_running:
                # Снимаем скриншот
                screenshot = pyautogui.screenshot()
                frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
                
                # Проверяем есть ли рыба
                fish_detected, confidence = self.detector.detect_fish(frame)
                
                if fish_detected:
                    logger.info(f"🐟 Обнаружена рыба! Уверенность: {confidence:.2f}")
                    
                    # Клик на рыбу
                    self.click_fish()
                    fish_count += 1
                    self.total_fish += 1
                    
                    # Логируем улов
                    self.stats.add_catch()
                    logger.info(f"✅ Рыба #{fish_count} поймана! (Всего: {self.total_fish})")
                    
                    # Задержка перед следующей рыбалкой
                    time.sleep(self.config.CATCH_DELAY)
                
                # Ищем индикатор готовности к следующей рыбалке
                if self.detector.is_ready_for_next(frame):
                    logger.debug("⏳ Готовимся к следующей рыбалке...")
                    time.sleep(self.config.READY_DELAY)
                
                # Малая задержка чтобы не грузить процессор
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            logger.info("Остановка по команде пользователя...")
        except Exception as e:
            logger.error(f"❌ Ошибка: {e}")
        finally:
            self.stop_fishing(fish_count)
    
    def click_fish(self):
        """Клик по рыбе с реалистичной задержкой"""
        # Получаем текущую позицию мыши
        current_x, current_y = pyautogui.position()
        
        # Кликаем в центр экрана (где обычно индикатор рыбалки)
        center_x = self.config.SCREEN_WIDTH // 2
        center_y = self.config.SCREEN_HEIGHT // 2
        
        pyautogui.moveTo(center_x, center_y, duration=0.05)
        pyautogui.click()
        
        # Возвращаемся на исходную позицию
        pyautogui.moveTo(current_x, current_y, duration=0.05)
        
        # Задержка между кликами
        time.sleep(self.config.CLICK_DELAY / 1000.0)
    
    def stop_fishing(self, fish_count):
        """Остановить рыбалку и показать статистику"""
        self.is_running = False
        end_time = datetime.now()
        duration = (end_time - self.start_time).total_seconds()
        
        print("\n" + "="*50)
        print("🛑 РЫБАЛКА ЗАВЕРШЕНА")
        print("="*50)
        print(f"⏱️  Время работы: {duration:.0f} секунд ({duration/60:.1f} минут)")
        print(f"🐟 Всего поймано рыб: {self.total_fish}")
        print(f"📊 Рыб в минуту: {(self.total_fish / (duration/60)):.1f}")
        print("="*50 + "\n")
        
        # Сохраняем статистику
        self.stats.save_session(self.total_fish, duration)
        logger.info(f"📊 Статистика сохранена. Всего поймано: {self.total_fish}")
    
    def show_menu(self):
        """Показать меню настроек"""
        while True:
            print("\n" + "="*50)
            print("🎮 GTA5 RP AUTOFISHING BOT - МЕНЮ")
            print("="*50)
            print("1. 🎣 Начать рыбалку")
            print("2. ⚙️  Настройки")
            print("3. 📊 Статистика")
            print("4. 🚪 Выход")
            print("="*50)
            
            choice = input("\nВыбери пункт (1-4): ").strip()
            
            if choice == "1":
                self.start_fishing()
            elif choice == "2":
                self.show_settings()
            elif choice == "3":
                self.show_statistics()
            elif choice == "4":
                print("\n🚪 До свидания!\n")
                break
            else:
                print("❌ Неверный выбор!")
    
    def show_settings(self):
        """Показать и изменить настройки"""
        print("\n" + "="*50)
        print("⚙️  НАСТРОЙКИ")
        print("="*50)
        print(f"Текущий режим: {self.config.MODE}")
        print(f"Задержка клика: {self.config.CLICK_DELAY} мс")
        print(f"Задержка после поимки: {self.config.CATCH_DELAY} сек")
        print(f"Задержка готовности: {self.config.READY_DELAY} сек")
        print("="*50)
        print("Настройки хранятся в config.py")
        print("Отредактируй их там для изменения\n")
    
    def show_statistics(self):
        """Показать статистику"""
        stats_data = self.stats.get_all_sessions()
        
        if not stats_data:
            print("\n❌ Нет сохранённой статистики\n")
            return
        
        print("\n" + "="*50)
        print("📊 СТАТИСТИКА РЫБАЛКИ")
        print("="*50)
        
        total_fish = sum(s['fish_count'] for s in stats_data)
        total_time = sum(s['duration'] for s in stats_data)
        avg_fish_per_hour = (total_fish / (total_time / 3600)) if total_time > 0 else 0
        
        print(f"Всего рыб поймано: {total_fish}")
        print(f"Общее время: {total_time/3600:.1f} часов")
        print(f"Среднее рыб в час: {avg_fish_per_hour:.0f}")
        print(f"Всего сессий: {len(stats_data)}")
        print("="*50)
        
        print("\nПоследние 5 сессий:")
        for i, session in enumerate(stats_data[-5:], 1):
            print(f"  {i}. {session['timestamp']} - {session['fish_count']} рыб ({session['duration']:.0f}сек)")
        print()


def main():
    """Главная функция"""
    try:
        bot = AutoFishingBot()
        bot.show_menu()
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        print(f"\n❌ Ошибка: {e}\n")


if __name__ == "__main__":
    main()
