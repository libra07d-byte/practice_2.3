import tkinter as tk
import requests
from psutil import cpu_percent, virtual_memory, disk_usage

def check_urls():
    urls_to_check = [
        ("https://github.com/", "GitHub"),
        ("https://www.binance.com/en", "Binance"),
        ("https://tomtit.tomsk.ru/", "TomTIT Томск"),
        ("https://jsonplaceholder.typicode.com/", "JSON Placeholder"),
        ("https://moodle.tomtit-tomsk.ru/", "Moodle TomTIT")
    ]
    
    result_text.delete(1.0, tk.END)
    for url, site_name in urls_to_check:
        try:
            resp = requests.head(url, timeout=5)
            code = resp.status_code
            if code == 200:
                status = "доступен"
            elif code == 404:
                status = "не найден"
            elif code == 403:
                status = "вход запрещен"
            else:
                status = "не доступен"
        except requests.exceptions.RequestException:
            code = "-"
            status = "ошибка связи"
        
        result_text.insert(tk.END, f"{site_name}: {url} — {status} ({code})\\n")

def system_monitor():
    cpu_load = cpu_percent(interval=None)
    memory_used = virtual_memory().percent
    disk_used = disk_usage('/').percent
    
    monitor_text.delete(1.0, tk.END)
    monitor_text.insert(tk.END, f"Загрузка CPU: {cpu_load}%")
    monitor_text.insert(tk.END, f"Использование памяти: {memory_used}%")
    monitor_text.insert(tk.END, f"Загруженность диска: {disk_used}%")
    
    root.after(2000, system_monitor) 


root = tk.Tk()
root.title("Мониторинг сайта и системы")

frame_left = tk.Frame(root)
frame_right = tk.Frame(root)

label_sites = tk.Label(frame_left, text="Проверка доступности сайтов:", font=("Arial", 12))
label_sites.pack(pady=(10, 5))

check_button = tk.Button(frame_left, text="Проверить доступность", command=check_urls)
check_button.pack(pady=5)

result_text = tk.Text(frame_left, height=10, width=50)
result_text.pack(padx=10, pady=5)

label_monitor = tk.Label(frame_right, text="Мониторинг системы:", font=("Arial", 12))
label_monitor.pack(pady=(10, 5))

monitor_text = tk.Text(frame_right, height=10, width=50)
monitor_text.pack(padx=10, pady=5)

system_monitor() 

frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
frame_right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

root.mainloop()
