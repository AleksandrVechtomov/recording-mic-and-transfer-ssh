from core import record_and_transmit_ssh
import schedule
import time
import signal
import sys


def schedule_tasks():
    """Настройка задач для планировщика"""
    schedule.every().day.at("03:05").do(record_and_transmit_ssh)
    schedule.every().day.at("09:05").do(record_and_transmit_ssh)
    schedule.every().day.at("15:05").do(record_and_transmit_ssh)
    schedule.every().day.at("21:05").do(record_and_transmit_ssh)


def run_scheduler():
    """Запуск планировщика"""
    schedule_tasks()
    print("ПЛАНИРОВЩИК ЗАПУЩЕН. Ожидание выполнения задач...")
    while True:
        schedule.run_pending()
        time.sleep(1)  # Проверка раз в секунду


def signal_handler(sig, frame):
    """Обработчик сигнала для корректного завершения программы"""
    print("\nПЛАНИРОВЩИК ОСТАНОВЛЕН.")
    sys.exit(0)


if __name__ == "__main__":
    # Привязываем обработчик сигнала
    signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
    run_scheduler()
