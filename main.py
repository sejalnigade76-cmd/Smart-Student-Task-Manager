import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

FILE_NAME = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")

tasks = []


# Load saved tasks
def load_tasks():
    global tasks

    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as file:
                tasks = json.load(file)
        except (json.JSONDecodeError, OSError):
            tasks = []


# Save tasks
def save_tasks():
    with open(FILE_NAME, "w") as file:
        json.dump(tasks, file, indent=4)


# Add a new task
def add_task():
    name = task_entry.get().strip()
    subject = subject_entry.get().strip()
    deadline = deadline_entry.get().strip()
    priority = priority_box.get()

    if not name or not subject or not deadline:
        messagebox.showwarning(
            "Missing Details",
            "Please fill in all the fields."
        )
        return

    try:
        datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror(
            "Invalid Date",
            "Enter date in YYYY-MM-DD format."
        )
        return

    task = {
        "name": name,
        "subject": subject,
        "deadline": deadline,
        "priority": priority,
        "completed": False
    }

    tasks.append(task)
    save_tasks()
    refresh_tasks()

    task_entry.delete(0, tk.END)
    subject_entry.delete(0, tk.END)
    deadline_entry.delete(0, tk.END)

    messagebox.showinfo("Success", "Task added successfully!")


# Display tasks
def refresh_tasks():
    for item in task_table.get_children():
        task_table.delete(item)

    today = datetime.today().date()

    pending = 0
    completed = 0
    overdue = 0

    for index, task in enumerate(tasks):
        deadline = datetime.strptime(
            task["deadline"], "%Y-%m-%d"
        ).date()

        if task["completed"]:
            status = "Completed"
            completed += 1
        elif deadline < today:
            status = "Overdue"
            overdue += 1
            pending += 1
        elif deadline == today:
            status = "Due Today"
            pending += 1
        else:
            status = "Pending"
            pending += 1

        task_table.insert(
            "",
            tk.END,
            iid=str(index),
            values=(
                task["name"],
                task["subject"],
                task["deadline"],
                task["priority"],
                status
            )
        )

    summary_label.config(
        text=f"Total Tasks: {len(tasks)}   |   "
             f"Pending: {pending}   |   "
             f"Completed: {completed}   |   "
             f"Overdue: {overdue}"
    )


# Mark selected task as completed
def complete_task():
    selected = task_table.selection()

    if not selected:
        messagebox.showwarning(
            "Selection Required",
            "Please select a task first."
        )
        return

    index = int(selected[0])

    tasks[index]["completed"] = True

    save_tasks()
    refresh_tasks()

    messagebox.showinfo(
        "Updated",
        "Task marked as completed!"
    )


# Delete selected task
def delete_task():
    selected = task_table.selection()

    if not selected:
        messagebox.showwarning(
            "Selection Required",
            "Please select a task first."
        )
        return

    index = int(selected[0])

    if messagebox.askyesno(
        "Confirm",
        "Are you sure you want to delete this task?"
    ):
        tasks.pop(index)
        save_tasks()
        refresh_tasks()


# Main window
root = tk.Tk()
root.title("Smart Student Task Manager")
root.geometry("900x600")
root.configure(bg="#F3F0FA")

# Heading
heading = tk.Label(
    root,
    text="SMART STUDENT TASK MANAGER",
    font=("Arial", 21, "bold"),
    bg="#F3F0FA",
    fg="#49366B"
)
heading.pack(pady=15)

subtitle = tk.Label(
    root,
    text="Organize your assignments. Never miss a deadline!",
    font=("Arial", 11),
    bg="#F3F0FA"
)
subtitle.pack(pady=3)

# Input section
input_frame = tk.LabelFrame(
    root,
    text=" Add New Task ",
    font=("Arial", 12, "bold"),
    bg="white",
    padx=15,
    pady=15
)
input_frame.pack(fill="x", padx=25, pady=15)

tk.Label(input_frame, text="Task Name:", bg="white").grid(
    row=0, column=0, padx=8, pady=8
)
task_entry = tk.Entry(input_frame, width=22)
task_entry.grid(row=0, column=1, padx=8, pady=8)

tk.Label(input_frame, text="Subject:", bg="white").grid(
    row=0, column=2, padx=8, pady=8
)
subject_entry = tk.Entry(input_frame, width=18)
subject_entry.grid(row=0, column=3, padx=8, pady=8)

tk.Label(input_frame, text="Deadline:", bg="white").grid(
    row=1, column=0, padx=8, pady=8
)
deadline_entry = tk.Entry(input_frame, width=22)
deadline_entry.grid(row=1, column=1, padx=8, pady=8)

tk.Label(input_frame, text="Priority:", bg="white").grid(
    row=1, column=2, padx=8, pady=8
)

priority_box = ttk.Combobox(
    input_frame,
    values=["High", "Medium", "Low"],
    width=15,
    state="readonly"
)
priority_box.set("Medium")
priority_box.grid(row=1, column=3, padx=8, pady=8)

add_button = tk.Button(
    input_frame,
    text="Add Task",
    command=add_task,
    bg="#634B91",
    fg="white",
    width=15
)
add_button.grid(row=2, column=1, pady=12)

# Task table
table_frame = tk.Frame(root, bg="#F3F0FA")
table_frame.pack(fill="both", expand=True, padx=25, pady=10)

columns = (
    "Task",
    "Subject",
    "Deadline",
    "Priority",
    "Status"
)

task_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=10
)

for column in columns:
    task_table.heading(column, text=column)
    task_table.column(column, width=145, anchor="center")

task_table.pack(fill="both", expand=True)

# Action buttons
button_frame = tk.Frame(root, bg="#F3F0FA")
button_frame.pack(pady=10)

tk.Button(
    button_frame,
    text="Mark Completed",
    command=complete_task,
    bg="#39845C",
    fg="white",
    width=18
).grid(row=0, column=0, padx=10)

tk.Button(
    button_frame,
    text="Delete Task",
    command=delete_task,
    bg="#B64A4A",
    fg="white",
    width=18
).grid(row=0, column=1, padx=10)

# Summary
summary_label = tk.Label(
    root,
    text="",
    font=("Arial", 11, "bold"),
    bg="#F3F0FA",
    fg="#49366B"
)
summary_label.pack(pady=12)

# Start application
load_tasks()
refresh_tasks()

root.mainloop()