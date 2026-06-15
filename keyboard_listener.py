# -*- coding: utf-8 -*-
"""
Модуль для отслеживания горячих клавиш
"""

from pynput import keyboard
import threading
from config import Config


class KeyboardListener:
    def __init__(self, on_stop=None, on_pause=None, on_resume=None):
        self.config = Config()
        self.on_stop = on_stop
        self.on_pause = on_pause
        self.on_resume = on_resume
        self.is_paused = False
        self.listener = None
    
    def on_press(self, key):
        """Обработка нажатия клавиши"""
        try:
            # Получаем символ клавиши
            if hasattr(key, 'char'):
                char = key.char.lower()
            else:
                return
            
            # Проверяем горячие клавиши
            if char == self.config.STOP_KEY:
                if self.on_stop:
                    self.on_stop()
            
            elif char == self.config.PAUSE_KEY:
                if self.on_pause:
                    self.on_pause()
                    self.is_paused = True
            
            elif char == self.config.RESUME_KEY:
                if self.on_resume:
                    self.on_resume()
                    self.is_paused = False
        
        except AttributeError:
            pass
    
    def start(self):
        """Начать отслеживание клавиш"""
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
    
    def stop(self):
        """Остановить отслеживание клавиш"""
        if self.listener:
            self.listener.stop()
