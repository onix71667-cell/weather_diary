import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

FILENAME = "data.json"

def load_data():
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_data(data):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def add_record():
    date = entry_date.get()
    temp = entry_temp.get()
    desc = entry_desc.get()
    precip = var_precip.get()

    if not date or not temp or not desc:
        messagebox.showerror("Ошибка", "Заполните все поля!")
        return

    try:
        datetime.strptime(date, "%Y-%m-%d")
        temp = float(temp)
    except ValueError:
        messagebox.showerror("Ошибка", "Неверный формат даты или температуры!")
        return

    record = {
        "date": date,
        "temp": temp,
        "description": desc,
        "precipitation": precip
    }

    data.append(record)
    save_data(data)
    update_table()
    clear_inputs()

def update_table(filter_date=None, filter_temp=None):
    for i in treeview.get_children():
        treeview.delete(i)

    for rec in data:
        if filter_date and rec["date"] != filter_date:
            continue
        if filter_temp is not None and rec["temp"] <= filter_temp:
            continue
        treeview.insert("", "end", values=(
            rec["date"],
            rec["temp"],
            rec["description"],
            "Да" if rec["precipitation"] else "Нет"
        ))

def filter_records():
    date = entry_filter_date.get() or None
    temp = entry_filter_temp.get()
    try:
        temp = float(temp) if temp else None
    except ValueError:
        messagebox.showerror("Ошибка", "Температура должна быть числом!")
        return
    update_table(filter_date=date, filter_temp=temp)

def clear_inputs():
    entry_date.delete(0, tk.END)
    entry_temp.delete(0, tk.END)
    entry_desc.delete(0, tk.END)
    var_precip.set(0)

# Загрузка данных
data = load_data()

# Окно приложения
root = tk.Tk()
root.title("Дневник погоды")
root.geometry("700x500")

# Вкладки: Добавление и Просмотр/Фильтр
tab_control = ttk.Notebook(root)
tab_add = ttk.Frame(tab_control)
tab_view = ttk.Frame(tab_control)
tab_control.add(tab_add, text="Добавить запись")
tab_control.add(tab_view, text="Просмотр и фильтр")
tab_control.pack(expand=1, fill="both")

# Вкладка "Добавить запись"
tk.Label(tab_add, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_date = tk.Entry(tab_add, width=15)
entry_date.grid(row=0, column=1, padx=10, pady=5)

tk.Label(tab_add, text="Температура:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_temp = tk.Entry(tab_add, width=15)
entry_temp.grid(row=1, column=1, padx=10, pady=5)

tk.Label(tab_add, text="Описание:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_desc = tk.Entry(tab_add, width=30)
entry_desc.grid(row=2, column=1, padx=10, pady=5, columnspan=2)

tk.Label(tab_add, text="Осадки:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
var_precip = tk.IntVar()
tk.Radiobutton(tab_add, text="Да", variable=var_precip, value=1).grid(row=3, column=1)
tk.Radiobutton(tab_add, text="Нет", variable=var_precip, value=0).grid(row=3, column=2)

btn_add = tk.Button(tab_add, text="Добавить запись", command=add_record)
btn_add.grid(row=4, column=0, columnspan=3, pady=15)


# Вкладка "Просмотр и фильтр"
tk.Label(tab_view, text="Фильтр по дате:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_filter_date = tk.Entry(tab_view, width=15)
entry_filter_date.grid(row=0, column=1, padx=10, pady=5)

tk.Label(tab_view, text="Фильтр по температуре (>):").grid(row=0, column=2, padx=10, pady=5, sticky="e")
entry_filter_temp = tk.Entry(tab_view, width=10)
entry_filter_temp.grid(row=0, column=3, padx=10, pady=5)

btn_filter = tk.Button(tab_view, text="Применить фильтр", command=filter_records)
btn_filter.grid(row=0, column=4, padx=10)

# Таблица записей
treeview = ttk.Treeview(tab_view, columns=("Дата", "Температура", "Описание", "Осадки"), show="headings")
treeview.heading("Дата", text="Дата")
treeview.heading("Температура", text="Температура")
treeview.heading("Описание", text="Описание")
treeview.heading("Осадки", text="Осадки")
treeview.column("Дата", width=120)
treeview.column("Температура", width=100)
treeview.column("Описание", width=250)
treeview.column("Осадки", width=80)
treeview.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

# Заполнение таблицы при запуске
update_table()

root.mainloop()
