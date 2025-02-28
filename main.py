import time
import pygetwindow as gw
import json
import os
from datetime import datetime

def get_active_window():
    """Получает название активного окна, убирая лишние суффиксы."""
    try:
        active_window = gw.getActiveWindow()
        return active_window.title.split(" - ")[-1] if active_window else "No active window"
    except Exception as e:
        return f"Error: {e}"

def save_stats(window_times, filename="window_times.json"):
    """Сохраняет статистику времени работы в файл JSON."""
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(window_times, f, indent=4)

def load_stats(filename="window_times.json"):
    """Загружает статистику времени работы из JSON-файла.⌀"""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def clear_console():
    """Очищает консоль в зависимости от ОС."""
    os.system("cls" if os.name == "nt" else "clear")

def format_time(seconds):
    """Форматирует время в часы, минуты и секунды."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    if (hours < 10):
      hours = "0" + str(hours)
      
    if (minutes < 10):
      minutes = "0" + str(minutes)
      
    if (seconds < 10):
      seconds = "0" + str(seconds)
    return f"{hours}:{minutes}:{seconds}"


def get_today_date():
    """Возвращает текущую дату в формате YYYY-MM-DD."""
    return datetime.today().strftime("%Y-%m-%d")

def out_console(last_window, total_time, elapsed_time, today_stats):
    """Выводит статистику в консоль."""
    clear_console()
    print("name                 | total       | current    |")
    print("---------------------|-------------|------------|")
    print(f"{last_window[:20]:<20} | {format_time(total_time):<11} | {format_time(elapsed_time):<10} |")
    print("\nТоп 5 приложений за сегодня:")
    sorted_today_stats = sorted(today_stats.items(), key=lambda x: x[1], reverse=True)[:5]
    for app, time_spent in sorted_today_stats:
        print(f"{app:<20} | {format_time(time_spent)}")

def main():
    window_times = load_stats()
    last_window = None
    start_time = time.time()
    today_date = get_today_date()
    if today_date not in window_times:
        window_times[today_date] = {}
    
    while True:
        current_window = get_active_window()
        
        if current_window != last_window:
            if last_window:
                elapsed_time = time.time() - start_time
                window_times[last_window] = window_times.get(last_window, 0) + elapsed_time
                window_times[today_date][last_window] = window_times[today_date].get(last_window, 0) + elapsed_time
                save_stats(window_times)
            
            last_window = current_window
            start_time = time.time()
        
        total_time = window_times.get(last_window, 0) + (time.time() - start_time)
        today_stats = window_times.get(today_date, {})
        out_console(last_window, total_time, time.time() - start_time, today_stats)
        time.sleep(1)

if __name__ == "__main__":
    main()
