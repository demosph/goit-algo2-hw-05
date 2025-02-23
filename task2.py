import time
import re
from datasketch import HyperLogLog
import pandas as pd

def load_ip_addresses(file_path):
    """Завантажує IP-адреси з лог-файлу, ігноруючи некоректні рядки."""
    ip_pattern = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
    ip_addresses = []
    try:
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            for line in file:
                match = ip_pattern.search(line)
                if match:
                    ip_addresses.append(match.group(0))
    except Exception as e:
        print(f"Помилка при зчитуванні файлу: {e}")
    return ip_addresses

def count_unique_exact(ip_addresses):
    """Підраховує точну кількість унікальних IP-адрес за допомогою множини."""
    start_time = time.time()
    unique_ips = set(ip_addresses)
    end_time = time.time()
    return len(unique_ips), end_time - start_time

def count_unique_hyperloglog(ip_addresses):
    """Оцінює кількість унікальних IP-адрес за допомогою HyperLogLog."""
    hll = HyperLogLog()
    start_time = time.time()
    for ip in ip_addresses:
        hll.update(ip.encode('utf8'))
    end_time = time.time()
    return hll.count(), end_time - start_time

if __name__ == "__main__":
    file_path = "lms-stage-access.log"  # Шлях до лог-файлу

    # Завантаження даних
    ip_addresses = load_ip_addresses(file_path)

    if ip_addresses:
        # Точний підрахунок
        exact_count, exact_time = count_unique_exact(ip_addresses)

        # Підрахунок за допомогою HyperLogLog
        hll_count, hll_time = count_unique_hyperloglog(ip_addresses)

        # Формування та вивід результатів
        print("Результати порівняння:")
        print(f"{'':>25} {'Точний підрахунок':>20} {'HyperLogLog':>15}")
        print(f"{'Унікальні елементи':>25} {exact_count:>20.1f} {hll_count:>15.1f}")
        print(f"{'Час виконання (сек.)':>25} {exact_time:>20.2f} {hll_time:>15.2f}")
    else:
        print("Не вдалося отримати жодної IP-адреси з файлу.")