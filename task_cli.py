import sys
import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"

def print_header():
    print("\n🚀 Task Tracker CLI — Powered by NanoCoders\n")

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as file:
        return json.load(file)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as file:
        json.dump(tasks, file, indent=4)

def generate_id(tasks):
    return max([task["id"] for task in tasks], default=0) + 1

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def colored_status(status):
    colors = {
        "todo": "\033[94m",          # Blue
        "in-progress": "\033[93m",   # Yellow
        "done": "\033[92m"           # Green
    }
    reset = "\033[0m"
    return f"{colors.get(status, '')}{status}{reset}"

def add_task(description):
    tasks = load_tasks()
    task_id = generate_id(tasks)
    now = current_time()
    new_task = {
        "id": task_id,
        "description": description,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"✅ Task added successfully (ID: {task_id})")
    print("🔷 Status: todo")
    print("✅ Powered by NanoCoders\n")

def update_task(task_id, new_description):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["description"] = new_description
            task["updatedAt"] = current_time()
            save_tasks(tasks)
            print(f"✏️ Task {task_id} updated successfully")
            print("✅ Powered by NanoCoders\n")
            return
    print(f"❌ Task with ID {task_id} not found.\n")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [task for task in tasks if task["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"❌ Task with ID {task_id} not found.\n")
        return
    save_tasks(new_tasks)
    print(f"🗑️ Task {task_id} deleted successfully")
    print("✅ Powered by NanoCoders\n")

def mark_status(task_id, status):
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == task_id:
            task["status"] = status
            task["updatedAt"] = current_time()
            save_tasks(tasks)
            print(f"🔄 Task {task_id} marked as {status}")
            print("✅ Powered by NanoCoders\n")
            return
    print(f"❌ Task with ID {task_id} not found.\n")

def list_tasks(filter_status=None):
    tasks = load_tasks()
    tasks = sorted(tasks, key=lambda t: t['createdAt'])
    if filter_status:
        tasks = [t for t in tasks if t["status"] == filter_status]

    if not tasks:
        print("📭 No tasks found.")
    else:
        for task in tasks:
            print(f"[{task['id']}] {task['description']} - {colored_status(task['status'])}")
    print("\n✅ Powered by NanoCoders\n")

def clear_tasks():
    save_tasks([])
    print("🧹 All tasks cleared.")
    print("✅ Powered by NanoCoders\n")

# CLI handling
if __name__ == "__main__":
    print_header()

    if len(sys.argv) < 2:
        print("⚠️ Please provide a command (add/update/delete/mark-done/mark-in-progress/list/clear).")
        sys.exit(1)

    cmd = sys.argv[1]

    try:
        if cmd == "add":
            desc = sys.argv[2]
            add_task(desc)

        elif cmd == "update":
            task_id = int(sys.argv[2])
            desc = sys.argv[3]
            update_task(task_id, desc)

        elif cmd == "delete":
            task_id = int(sys.argv[2])
            delete_task(task_id)

        elif cmd == "mark-done":
            task_id = int(sys.argv[2])
            mark_status(task_id, "done")

        elif cmd == "mark-in-progress":
            task_id = int(sys.argv[2])
            mark_status(task_id, "in-progress")

        elif cmd == "list":
            if len(sys.argv) == 3:
                list_tasks(sys.argv[2])
            else:
                list_tasks()

        elif cmd == "clear":
            clear_tasks()

        else:
            print("❓ Unknown command.")
    except IndexError:
        print("⚠️ Missing required arguments.")
    except ValueError:
        print("⚠️ Invalid input. Task ID must be a number.")
