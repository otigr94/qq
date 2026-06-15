# -*- coding: utf-8 -*-
"""
Конфигурация для GTA5 RP AutoFishing Bot
"""

class Config:
    # РЕЖИМЫ РЫБАЛКИ
    # 'auto' - полностью автоматический режим
    # 'manual' - ручной режим с вспомогательными функциями
    # 'smart' - умный режим с определением состояния
    MODE = 'auto'
    
    # РАЗМЕРЫ ЭКРАНА (подстраивается автоматически)
    SCREEN_WIDTH = 1920
    SCREEN_HEIGHT = 1080
    
    # ЗАДЕРЖКИ (в миллисекундах/секундах)
    CLICK_DELAY = 100  # Задержка между кликами (мс)
    CATCH_DELAY = 2.0  # Задержка после поимки рыбы (сек)
    READY_DELAY = 1.0  # Задержка готовности к следующей (сек)
    
    # ЧУВСТВИТЕЛЬНОСТЬ ОБНАРУЖЕНИЯ
    FISH_DETECTION_THRESHOLD = 0.6  # Порог уверенности обнаружения рыбы (0-1)
    COLOR_THRESHOLD = 30  # Порог для обнаружения по цвету
    
    # ПОДДЕРЖИВАЕМЫЕ СЕРВЕРЫ
    SUPPORTED_SERVERS = [
        'Majestic',
        'Rage',
        'RedLine',
        'Diamond',
        'Elite',
        'Fantasy'
    ]
    
    # ЦВЕТА ДЛЯ ОБНАРУЖЕНИЯ (BGR формат)
    # Зелёный цвет индикатора рыбалки
    GREEN_COLOR = (0, 255, 0)
    # Жёлтый цвет успешного клёва
    YELLOW_COLOR = (0, 255, 255)
    # Красный цвет ошибки
    RED_COLOR = (0, 0, 255)
    
    # ФАЙЛ ЛОГОВ И СТАТИСТИКИ
    LOG_FILE = 'fishing_bot.log'
    STATS_FILE = 'fishing_stats.json'
    
    # ОТЛАДКА
    DEBUG_MODE = False  # Включить отладочный режим
    SHOW_DETECTION_WINDOW = False  # Показывать окно обнаружения
    
    #安全设置 (БЕЗОПАСНОСТЬ)
    ANTI_BAN_MODE = True  # Включить антибан режим (реалистичные задержки)
    RANDOMIZE_CLICKS = True  # Случайные позиции кликов
    MIN_DELAY_BETWEEN_CLICKS = 50  # Минимальная задержка (мс)
    MAX_DELAY_BETWEEN_CLICKS = 300  # Максимальная задержка (мс)
    
    # ГОРЯЧИЕ КЛАВИШИ
    STOP_KEY = 'q'  # Клавиша для остановки
    PAUSE_KEY = 'p'  # Клавиша для паузы
    RESUME_KEY = 'r'  # Клавиша для возобновления
    
    # МАКСИМАЛЬНОЕ ВРЕМЯ РАБОТЫ (в минутах, 0 = бесконечно)
    MAX_SESSION_TIME = 0
    
    # ОТПРАВКА УВЕДОМЛЕНИЙ
    ENABLE_NOTIFICATIONS = True
    NOTIFICATION_INTERVAL = 100  # Каждые N рыб
    
    @staticmethod
    def get_server_config(server_name):
        """Получить конфигурацию для конкретного сервера"""
        configs = {
            'Majestic': {
                'CLICK_DELAY': 100,
                'CATCH_DELAY': 2.0,
                'FISH_DETECTION_THRESHOLD': 0.65
            },
            'Rage': {
                'CLICK_DELAY': 80,
                'CATCH_DELAY': 1.5,
                'FISH_DETECTION_THRESHOLD': 0.60
            },
            'RedLine': {
                'CLICK_DELAY': 120,
                'CATCH_DELAY': 2.5,
                'FISH_DETECTION_THRESHOLD': 0.70
            }
        }
        return configs.get(server_name, {})
