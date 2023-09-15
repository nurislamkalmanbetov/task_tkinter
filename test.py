import sqlite3
import tkinter as tk
from tkinter import messagebox

class TodoApp:
    def __init__(self, root):
        # Инициализация базы данных
        self.init_db()

        # Установка фона главного окна
        root.configure(bg="black")

        # Инициализация интерфейса
        self.title_label = tk.Label(root, text="Daily Tasks", font=("Helvetica", 50), fg="white", bg="black")
        self.title_label.pack(pady=20)

        self.task_input = tk.Entry(root, width=90, bg="white", fg="black")
        self.task_input.pack(pady=20)  

        self.listbox = tk.Listbox(root, height=20, width=90, bg="white", fg="black")
        self.listbox.pack(pady=20)

        add_button = tk.Button(root, text="Add Task", command=self.add_task, bg="#1F98BB", fg="white", width=90)
        add_button.pack(pady=5)

        delete_button = tk.Button(root, text="Delete Task", command=self.delete_task, bg="#1F98BB", fg="white", width=90)
        delete_button.pack(pady=5)

        self.load_tasks()

    def init_db(self):
        self.conn = sqlite3.connect("tasks.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            task TEXT NOT NULL
        )
        """)

    def load_tasks(self):
        tasks = self.get_tasks_from_db()
        self.listbox.delete(0, tk.END)  # очищаем listbox
        for task in tasks:
            self.listbox.insert(tk.END, task[1])

    def add_task(self):
        task_name = self.task_input.get()
        if task_name:
            self.add_task_to_db(task_name)
            self.load_tasks()
            self.task_input.delete(0, tk.END)

    def delete_task(self):
        try:
            index = self.listbox.curselection()[0]
            task_name = self.listbox.get(index)
            self.delete_task_from_db(task_name)
            self.load_tasks()
        except:
            messagebox.showinfo("Warning", "Please select a task to delete")

    def add_task_to_db(self, task_name):
        self.cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task_name,))
        self.conn.commit()

    def delete_task_from_db(self, task_name):
        self.cursor.execute("DELETE FROM tasks WHERE task=?", (task_name,))
        self.conn.commit()

    def get_tasks_from_db(self):
        self.cursor.execute("SELECT * FROM tasks")
        return self.cursor.fetchall()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("To-Do List")
    root.configure(bg="#222627")  # Установка фонового цвета окна
    todo_app = TodoApp(root)
    root.mainloop()
