import sqlite3
import random

def init_db():
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

def run_experiment_v2(messenger, file_size, encryption):
    """Модифицированный расчет с обработкой исключений try-except"""
    try:
        conn = sqlite3.connect('metrics.db')
        cursor = conn.cursor()
        
        # Усложненная формула: добавляется штраф за слишком большой размер файла
        overhead = 1.3 if file_size > 500 else 1.0
        base_speed = 50 if messenger == "Telegram" else 40
        
        duration = int((file_size / base_speed) * 1000 * overhead) + random.randint(5, 30)
        
        cursor.execute('''
            INSERT INTO Experiments (messenger_name, file_size_mb, encryption_type, duration_ms)
            VALUES (?, ?, ?, ?)
        ''', (messenger, file_size, encryption, duration))
        conn.commit()
        print(f"[V2] Эксперимент для {messenger} успешно сохранен.")
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")
    finally:
        if conn:
            conn.close()

def calculate_analytics():
    """Новый вычислительный эксперимент: Расчет средней скорости мессенджеров"""
    try:
        conn = sqlite3.connect('metrics.db')
        cursor = conn.cursor()
        
        # Вычисление: среднее значение (Размер / Время в секундах)
        cursor.execute('''
            SELECT messenger_name, AVG(file_size_mb / (duration_ms / 1000.0)) as avg_speed
            FROM Experiments
            GROUP BY messenger_name
        ''')
        results = cursor.fetchall()
        
        print("\n=== РЕЗУЛЬТАТЫ ВЫЧИСЛИТЕЛЬНОГО ЭКСПЕРИМЕНТА ===")
        for row in results:
            print(f"Мессенджер: {row[0]} | Средняя скорость: {round(row[1], 2)} Мб/с")
            
    except sqlite3.Error as e:
        print(f"Ошибка аналитики: {e}")
    finally:
        conn.close()

# Запуск программы
if __name__ == "__main__":
    init_db()
    # Дозапись новых данных для эксперимента
    run_experiment_v2("Telegram", 600.0, "E2EE")
    run_experiment_v2("Viber", 150.0, "E2EE")
    
    # Запуск вычислительного анализа
    calculate_analytics()
