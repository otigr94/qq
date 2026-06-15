# 📥 Подробная инструкция установки

## Windows 10/11

### Шаг 1: Установи Python

1. Скачай Python 3.9+ с https://www.python.org/downloads/
2. **ВАЖНО:** При установке отметь "Add Python to PATH"
3. Установи

### Шаг 2: Клонируй репозиторий

```bash
git clone https://github.com/otigr94/qq.git
cd qq
```

Или просто скачай ZIP и распакуй папку

### Шаг 3: Установи зависимости

Отворе командную строку (cmd) в папке проекта и выполни:

```bash
pip install -r requirements.txt
```

Это может занять 2-3 минуты

### Шаг 4: Запусти бота

```bash
python main.py
```

Если видишь меню - всё установлено правильно!

---

## macOS

### Шаг 1: Установи Homebrew

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Шаг 2: Установи Python

```bash
brew install python3
```

### Шаг 3: Клонируй репо

```bash
git clone https://github.com/otigr94/qq.git
cd qq
```

### Шаг 4: Установи зависимости

```bash
pip3 install -r requirements.txt
```

### Шаг 5: Запусти

```bash
python3 main.py
```

---

## Linux

### Ubuntu/Debian

```bash
# Установи Python и необходимые библиотеки
sudo apt-get update
sudo apt-get install python3 python3-pip python3-dev
sudo apt-get install libopencv-dev python3-opencv

# Клонируй репо
git clone https://github.com/otigr94/qq.git
cd qq

# Установи зависимости
pip3 install -r requirements.txt

# Запусти
python3 main.py
```

### Fedora

```bash
sudo dnf install python3 python3-pip opencv-devel
git clone https://github.com/otigr94/qq.git
cd qq
pip3 install -r requirements.txt
python3 main.py
```

---

## ⚠️ Решение проблем при установке

### Ошибка: "python is not recognized"

**Решение:** Python не добавлен в PATH
1. Переустанови Python
2. При установке отметь "Add Python to PATH"
3. Перезагрузи компьютер

### Ошибка: "pip is not recognized"

**Решение:** Используй `python -m pip`
```bash
python -m pip install -r requirements.txt
```

### Ошибка при установке OpenCV

**Решение для Windows:**
```bash
pip install opencv-python-headless
```

**Решение для Mac:**
```bash
brew install opencv
pip3 install opencv-python
```

### Ошибка: "No module named 'pyautogui'"

**Решение:**
```bash
pip install --upgrade pyautogui
```

### Медленная установка

Попробуй использовать другой индекс PyPI:
```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

---

## ✅ Проверка установки

Чтобы проверить что всё установлено правильно:

```bash
python -c "import cv2; print('OpenCV OK')"
python -c "import pyautogui; print('PyAutoGUI OK')"
python -c "import numpy; print('NumPy OK')"
```

Если видишь "OK" - готово!

---

## 🚀 Первый запуск

1. Запусти бота: `python main.py`
2. Выбери пункт 1 (Начать рыбалку)
3. Нажми Q чтобы остановить
4. Смотри статистику

**Готово! Бот работает! 🎣**
