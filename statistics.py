# -*- coding: utf-8 -*-
"""
Модуль для сбора и анализа статистики рыбалки
"""

import json
import os
from datetime import datetime
from pathlib import Path
from config import Config


class Statistics:
    def __init__(self):
        self.config = Config()
        self.stats_file = self.config.STATS_FILE
        self.current_session_fish = 0
        self.ensure_stats_file_exists()
    
    def ensure_stats_file_exists(self):
        """Убедиться что файл статистики существует"""
        if not os.path.exists(self.stats_file):
            with open(self.stats_file, 'w', encoding='utf-8') as f:
                json.dump({'sessions': []}, f, indent=2, ensure_ascii=False)
    
    def add_catch(self):
        """Добавить одну пойманную рыбу"""
        self.current_session_fish += 1
    
    def save_session(self, fish_count, duration):
        """Сохранить сессию рыбалки"""
        session_data = {
            'timestamp': datetime.now().isoformat(),
            'fish_count': fish_count,
            'duration': duration,
            'fish_per_minute': fish_count / (duration / 60) if duration > 0 else 0,
            'fish_per_hour': (fish_count / (duration / 3600)) if duration > 0 else 0
        }
        
        # Читаем текущую статистику
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except:
            data = {'sessions': []}
        
        # Добавляем новую сессию
        data['sessions'].append(session_data)
        
        # Сохраняем обновлённую статистику
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_all_sessions(self):
        """Получить все сохранённые сессии"""
        try:
            with open(self.stats_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('sessions', [])
        except:
            return []
    
    def get_total_stats(self):
        """Получить общую статистику"""
        sessions = self.get_all_sessions()
        
        if not sessions:
            return {
                'total_fish': 0,
                'total_time': 0,
                'sessions_count': 0,
                'average_fish_per_session': 0,
                'average_time_per_session': 0,
                'average_fish_per_hour': 0
            }
        
        total_fish = sum(s['fish_count'] for s in sessions)
        total_time = sum(s['duration'] for s in sessions)
        sessions_count = len(sessions)
        
        return {
            'total_fish': total_fish,
            'total_time': total_time,
            'sessions_count': sessions_count,
            'average_fish_per_session': total_fish / sessions_count if sessions_count > 0 else 0,
            'average_time_per_session': total_time / sessions_count if sessions_count > 0 else 0,
            'average_fish_per_hour': (total_fish / (total_time / 3600)) if total_time > 0 else 0
        }
    
    def get_session_by_date(self, date_str):
        """Получить сессии за конкретную дату"""
        sessions = self.get_all_sessions()
        return [s for s in sessions if s['timestamp'].startswith(date_str)]
    
    def get_best_session(self):
        """Получить лучшую сессию (по количеству рыб)"""
        sessions = self.get_all_sessions()
        if not sessions:
            return None
        return max(sessions, key=lambda x: x['fish_count'])
    
    def get_worst_session(self):
        """Получить худшую сессию (по количеству рыб)"""
        sessions = self.get_all_sessions()
        if not sessions:
            return None
        return min(sessions, key=lambda x: x['fish_count'])
    
    def export_stats(self, filename='fishing_stats_export.json'):
        """Экспортировать статистику в файл"""
        stats = {
            'total': self.get_total_stats(),
            'sessions': self.get_all_sessions(),
            'best_session': self.get_best_session(),
            'worst_session': self.get_worst_session(),
            'export_date': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def print_summary(self):
        """Вывести краткую сводку статистики"""
        total_stats = self.get_total_stats()
        
        print("\n" + "="*50)
        print("📊 ИТОГОВАЯ СТАТИСТИКА")
        print("="*50)
        print(f"Всего поймано рыб: {total_stats['total_fish']}")
        print(f"Общее время рыбалки: {total_stats['total_time']/3600:.1f} часов")
        print(f"Количество сессий: {total_stats['sessions_count']}")
        print(f"Среднее рыб за сессию: {total_stats['average_fish_per_session']:.0f}")
        print(f"Средние рыбы в час: {total_stats['average_fish_per_hour']:.0f}")
        
        best = self.get_best_session()
        if best:
            print(f"\n🏆 Лучшая сессия: {best['fish_count']} рыб")
        
        print("="*50 + "\n")
