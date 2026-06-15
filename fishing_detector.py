# -*- coding: utf-8 -*-
"""
Модуль для обнаружения рыбы и элементов интерфейса
"""

import cv2
import numpy as np
from config import Config


class FishingDetector:
    def __init__(self):
        self.config = Config()
        self.last_detection = None
        self.detection_history = []
    
    def detect_fish(self, frame):
        """
        Обнаружить рыбу на экране
        Возвращает: (detected: bool, confidence: float)
        """
        # Преобразуем в HSV для лучшего определения цветов
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Обнаружение зелёного цвета (индикатор рыбалки)
        green_mask = self.detect_color(hsv, 'green')
        
        # Обнаружение жёлтого цвета (момент клёва)
        yellow_mask = self.detect_color(hsv, 'yellow')
        
        # Комбинируем маски
        combined_mask = cv2.bitwise_or(green_mask, yellow_mask)
        
        # Находим контуры
        contours, _ = cv2.findContours(combined_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return False, 0.0
        
        # Находим самый большой контур
        largest_contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        
        # Проверяем минимальную площадь
        if area < 100:
            return False, 0.0
        
        # Вычисляем уверенность на основе площади и формы
        confidence = min(area / 1000.0, 1.0)
        
        # Проверяем форму (должна быть близка к кругу)
        circularity = self.calculate_circularity(largest_contour)
        confidence *= (0.5 + circularity * 0.5)  # Вес формы
        
        self.detection_history.append(confidence)
        if len(self.detection_history) > 10:
            self.detection_history.pop(0)
        
        return confidence >= self.config.FISH_DETECTION_THRESHOLD, confidence
    
    def detect_color(self, hsv_frame, color):
        """
        Обнаружить определённый цвет в HSV кадре
        """
        # Диапазоны HSV для разных цветов
        color_ranges = {
            'green': {
                'lower': np.array([35, 40, 40]),
                'upper': np.array([85, 255, 255])
            },
            'yellow': {
                'lower': np.array([15, 100, 100]),
                'upper': np.array([35, 255, 255])
            },
            'red': {
                'lower': np.array([0, 100, 100]),
                'upper': np.array([10, 255, 255])
            }
        }
        
        if color not in color_ranges:
            return np.zeros(hsv_frame.shape[:2], dtype=np.uint8)
        
        range_info = color_ranges[color]
        mask = cv2.inRange(hsv_frame, range_info['lower'], range_info['upper'])
        
        # Морфологические операции для очистки
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        
        return mask
    
    def calculate_circularity(self, contour):
        """
        Вычислить коэффициент круглости контура
        1.0 = идеальный круг, 0.0 = линия
        """
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        if perimeter == 0:
            return 0.0
        
        circularity = 4 * np.pi * area / (perimeter ** 2)
        return min(circularity, 1.0)
    
    def is_ready_for_next(self, frame):
        """
        Проверить готовность к следующей рыбалке
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        green_mask = self.detect_color(hsv, 'green')
        
        # Если есть хороший зелёный сигнал - готов
        if np.sum(green_mask) > 5000:
            return True
        
        return False
    
    def detect_ui_elements(self, frame):
        """
        Обнаружить элементы интерфейса рыбалки
        """
        # Центр экрана
        center_x = frame.shape[1] // 2
        center_y = frame.shape[0] // 2
        
        # Область интереса (ROI) - центр экрана
        roi = frame[center_y-100:center_y+100, center_x-100:center_x+100]
        
        # Анализируем ROI
        hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        
        # Подсчитываем пиксели разных цветов
        green_pixels = np.sum(self.detect_color(hsv_roi, 'green'))
        yellow_pixels = np.sum(self.detect_color(hsv_roi, 'yellow'))
        red_pixels = np.sum(self.detect_color(hsv_roi, 'red'))
        
        return {
            'green': green_pixels,
            'yellow': yellow_pixels,
            'red': red_pixels,
            'roi': roi
        }
    
    def get_confidence_history(self):
        """
        Получить историю уверенности обнаружения
        """
        if not self.detection_history:
            return 0.0
        
        return np.mean(self.detection_history)
