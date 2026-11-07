import sqlite3
import random


def init_db():
    """Создание базы данных и таблицы для результатов"""
    conn = sqlite3.connect('metrics.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            messenger_name TEXT,
            file_size_mb REAL,
            encryption_type TEXT,
            duration_ms INTEGER
        )
    ''')
    conn.commit()
    conn.close()


def run_experiment_v1(messenger, file_size, encryption):
    """Базовый расчет времени передачи данных и запись в БД"""
    base_speed = 50 if messenger == "Telegram" else 40
    encryption_penalty = 1.5 if encryption == "E2EE" else 1.0

    # Линейный расчет времени с небольшим случайным отклонением
    duration = int((file_size / base_speed) * 1000 * encryption_penalty) + random.randint(10, 50)

    conn = sqlite3.connect('metrics.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Experiments (messenger_name, file_size_mb, encryption_type, duration_ms)
        VALUES (?, ?, ?, ?)
    ''', (messenger, file_size, encryption, duration))
    conn.commit()
    conn.close()
    print(f"[V1] Эксперимент сохранен. Рассчитанное время: {duration} мс")


# Запуск программы
if __name__ == "__main__":
    init_db()
    run_experiment_v1("Telegram", 100.0, "E2EE")
    run_experiment_v1("WhatsApp", 100.0, "E2EE")
