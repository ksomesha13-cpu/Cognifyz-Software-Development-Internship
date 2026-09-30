"""
Task 5: Enhanced Persistent Task Manager using File I/O
Level 3: Advanced
Internship Program: Software Development - Cognifyz Technologies

Objective:
Implement file storage for tasks to enable saving and loading from a text file,
with comprehensive error handling and persistence verification.

Features:
- Extends CRUD architecture with automatic and manual File I/O
- JSON-based persistent storage (data persistence across program runs)
- Structured plain-text export for human-readable task logs
- Robust error handling:
    * FileNotFoundError recovery with graceful initialization
    * JSONDecodeError / corrupted data handling with automatic .bak backup
    * PermissionError and OSError handling
- Complete interactive console UI with CRUD + File management
"""

import json
import os
import shutil
import sys
from datetime import datetime
from typing import List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Ensure we can import Task and display utilities if running from other directories
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
level2_dir = os.path.join(parent_dir, "Level-2")
if level2_dir not in sys.path:
    sys.path.append(level2_dir)

try:
    from task3_task_manager_crud import Task, display_tasks_table, display_single_task
except ImportError:
    # Standalone fallback definition of Task
    class Task:
        VALID_STATUSES = ["Pending", "In Progress", "Completed"]
        VALID_PRIORITIES = ["Low", "Medium", "High"]

        def __init__(self, task_id: int, title: str, description: str = "", status: str = "Pending", priority: str = "Medium", created_at: Optional[str] = None):
            self.task_id = task_id
            self.title = title.strip()
            self.description = description.strip()
            self.status = status if status in self.VALID_STATUSES else "Pending"
            self.priority = priority if priority in self.VALID_PRIORITIES else "Medium"
            self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        def to_dict(self) -> dict:
            return {
                "task_id": self.task_id,
                "title": self.title,
                "description": self.description,
                "status": self.status,
                "priority": self.priority,
                "created_at": self.created_at,
            }

        @classmethod
        def from_dict(cls, data: dict) -> "Task":
            return cls(
                task_id=data["task_id"],
                title=data["title"],
                description=data.get("description", ""),
                status=data.get("status", "Pending"),
                priority=data.get("priority", "Medium"),
                created_at=data.get("created_at"),
            )

    def display_tasks_table(tasks: List[Task]):
        if not tasks:
            print("\n📭 No tasks found.")
            return
        header = f"{'ID':<4} | {'Title':<30} | {'Priority':<8} | {'Status':<12} | {'Created At':<19}"
        print("-" * len(header))
        print(header)
        print("-" * len(header))
        for t in tasks:
            print(f"{t.task_id:<4} | {t.title[:30]:<30} | {t.priority:<8} | {t.status:<12} | {t.created_at:<19}")
        print("-" * len(header))


DEFAULT_STORAGE_FILE = os.path.join(current_dir, "tasks_storage.json")
DEFAULT_EXPORT_FILE = os.path.join(current_dir, "tasks_export.txt")


class PersistentTaskManager:
    """Task Manager with persistent file storage and robust error handling."""

    def __init__(self, storage_path: str = DEFAULT_STORAGE_FILE, auto_load: bool = True):
        self.storage_path = storage_path
        self.tasks: List[Task] = []
        self._next_id = 1
        if auto_load:
            self.load_from_file()

    def create_task(self, title: str, description: str = "", priority: str = "Medium", status: str = "Pending", auto_save: bool = True) -> Task:
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty.")

        task = Task(
            task_id=self._next_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
        )
        self.tasks.append(task)
        self._next_id += 1
        if auto_save:
            self.save_to_file()
        return task

    def read_all_tasks(self) -> List[Task]:
        return list(self.tasks)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        for t in self.tasks:
            if t.task_id == task_id:
                return t
        return None

    def search_tasks(self, keyword: str) -> List[Task]:
        kw = keyword.lower()
        return [t for t in self.tasks if kw in t.title.lower() or kw in t.description.lower()]

    def filter_tasks(self, status: Optional[str] = None, priority: Optional[str] = None) -> List[Task]:
        res = self.tasks
        if status:
            res = [t for t in res if t.status.lower() == status.lower()]
        if priority:
            res = [t for t in res if t.priority.lower() == priority.lower()]
        return res

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None, status: Optional[str] = None, priority: Optional[str] = None, auto_save: bool = True) -> Optional[Task]:
        task = self.get_task_by_id(task_id)
        if not task:
            return None
        if title is not None and title.strip():
            task.title = title.strip()
        if description is not None:
            task.description = description.strip()
        if status is not None and status in Task.VALID_STATUSES:
            task.status = status
        if priority is not None and priority in Task.VALID_PRIORITIES:
            task.priority = priority
        if auto_save:
            self.save_to_file()
        return task

    def delete_task(self, task_id: int, auto_save: bool = True) -> bool:
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            if auto_save:
                self.save_to_file()
            return True
        return False

    def save_to_file(self, target_path: Optional[str] = None) -> bool:
        """
        Save all tasks to a JSON file with error handling.
        Returns True on success, False on error.
        """
        path = target_path or self.storage_path
        try:
            # Ensure target directory exists
            parent = os.path.dirname(os.path.abspath(path))
            if parent and not os.path.exists(parent):
                os.makedirs(parent, exist_ok=True)

            payload = {
                "version": "1.0",
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "tasks": [t.to_dict() for t in self.tasks],
            }
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, indent=4)
            return True
        except PermissionError:
            print(f"❌ Error: Permission denied when writing to '{path}'.")
            return False
        except OSError as e:
            print(f"❌ OS Error saving tasks to '{path}': {e}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error saving tasks: {e}")
            return False

    def load_from_file(self, target_path: Optional[str] = None) -> bool:
        """
        Load tasks from a persistent JSON file with comprehensive error handling.
        """
        path = target_path or self.storage_path
        if not os.path.exists(path):
            # File doesn't exist yet, start with empty list
            self.tasks = []
            self._next_id = 1
            return False

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            raw_tasks = data.get("tasks", []) if isinstance(data, dict) else data
            loaded_tasks = []
            max_id = 0
            for item in raw_tasks:
                task = Task.from_dict(item)
                loaded_tasks.append(task)
                if task.task_id > max_id:
                    max_id = task.task_id

            self.tasks = loaded_tasks
            self._next_id = max_id + 1
            return True

        except FileNotFoundError:
            print(f"ℹ️ Storage file '{path}' not found. Starting with a fresh list.")
            self.tasks = []
            self._next_id = 1
            return False
        except json.JSONDecodeError as e:
            print(f"⚠️ Warning: File '{path}' is corrupted or contains invalid JSON.")
            # Create a backup
            backup_path = f"{path}.corrupted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
            try:
                shutil.copyfile(path, backup_path)
                print(f"📦 Backup of corrupted file saved to '{backup_path}'.")
            except Exception:
                pass
            self.tasks = []
            self._next_id = 1
            return False
        except PermissionError:
            print(f"❌ Error: Permission denied when reading '{path}'.")
            return False
        except Exception as e:
            print(f"❌ Error loading tasks from '{path}': {e}")
            return False

    def export_to_text_file(self, export_path: str = DEFAULT_EXPORT_FILE) -> bool:
        """Export tasks into a human-readable text file summary."""
        try:
            with open(export_path, "w", encoding="utf-8") as f:
                f.write("=" * 60 + "\n")
                f.write("  COGNIFYZ INTERNSHIP - PERSISTENT TASK MANAGER EXPORT\n")
                f.write(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"  Total Tasks: {len(self.tasks)}\n")
                f.write("=" * 60 + "\n\n")

                if not self.tasks:
                    f.write("No tasks recorded.\n")
                else:
                    for t in self.tasks:
                        f.write(f"Task ID:     {t.task_id}\n")
                        f.write(f"Title:       {t.title}\n")
                        f.write(f"Description: {t.description or 'N/A'}\n")
                        f.write(f"Priority:    {t.priority}\n")
                        f.write(f"Status:      {t.status}\n")
                        f.write(f"Created:     {t.created_at}\n")
                        f.write("-" * 40 + "\n")
            return True
        except Exception as e:
            print(f"❌ Error exporting tasks to '{export_path}': {e}")
            return False


def run_persistent_interactive(manager: PersistentTaskManager):
    """Interactive loop for Task 5."""
    while True:
        print("\n" + "=" * 60)
        print("  COGNIFYZ INTERNSHIP - TASK 5: PERSISTENT TASK MANAGER")
        print(f"  Storage: {os.path.basename(manager.storage_path)} ({len(manager.tasks)} tasks loaded)")
        print("=" * 60)
        print("1. ➕ Create New Task (Auto-saved)")
        print("2. 📋 View All Tasks")
        print("3. 🔍 Search / Filter Tasks")
        print("4. ✏️  Update Task (Auto-saved)")
        print("5. 🗑️  Delete Task (Auto-saved)")
        print("6. 💾 Force Manual Save to File")
        print("7. 📂 Reload Tasks from Storage File")
        print("8. 📄 Export to Human-Readable Text File (.txt)")
        print("9. ⚡ Seed Sample Tasks")
        print("10. 🚪 Return / Exit")

        choice = input("\nEnter choice (1-10): ").strip()

        if choice == "1":
            title = input("Enter task title: ").strip()
            if not title:
                print("❌ Title cannot be empty!")
                continue
            desc = input("Enter description (optional): ").strip()
            print("Select Priority: 1. Low  2. Medium  3. High")
            p_map = {"1": "Low", "2": "Medium", "3": "High"}
            priority = p_map.get(input("Choice (1-3, default Medium): ").strip(), "Medium")

            print("Select Status: 1. Pending  2. In Progress  3. Completed")
            s_map = {"1": "Pending", "2": "In Progress", "3": "Completed"}
            status = s_map.get(input("Choice (1-3, default Pending): ").strip(), "Pending")

            task = manager.create_task(title, desc, priority, status)
            print(f"✅ Task created with ID {task.task_id} and saved persistently!")

        elif choice == "2":
            display_tasks_table(manager.read_all_tasks())

        elif choice == "3":
            kw = input("Enter search keyword or status/priority filter: ").strip()
            matched = manager.search_tasks(kw) + manager.filter_tasks(status=kw, priority=kw)
            # Remove duplicates preserving order
            unique_tasks = list({t.task_id: t for t in matched}.values())
            display_tasks_table(unique_tasks)

        elif choice == "4":
            try:
                tid = int(input("Enter Task ID to update: ").strip())
                task = manager.get_task_by_id(tid)
                if not task:
                    print(f"❌ Task ID {tid} not found.")
                    continue
                new_title = input(f"New Title [{task.title}]: ").strip() or None
                new_desc = input(f"New Description [{task.description}]: ").strip()
                new_desc = new_desc if new_desc != "" else None

                print(f"Current Status: {task.status} (1. Pending / 2. In Progress / 3. Completed)")
                s_choice = input("Change status? (1-3, or Enter to keep): ").strip()
                s_map = {"1": "Pending", "2": "In Progress", "3": "Completed"}
                new_status = s_map.get(s_choice, None)

                print(f"Current Priority: {task.priority} (1. Low / 2. Medium / 3. High)")
                p_choice = input("Change priority? (1-3, or Enter to keep): ").strip()
                p_map = {"1": "Low", "2": "Medium", "3": "High"}
                new_priority = p_map.get(p_choice, None)

                manager.update_task(tid, new_title, new_desc, new_status, new_priority)
                print(f"✅ Task {tid} updated and persisted to storage file!")
            except ValueError:
                print("❌ Invalid Task ID!")

        elif choice == "5":
            try:
                tid = int(input("Enter Task ID to delete: ").strip())
                task = manager.get_task_by_id(tid)
                if not task:
                    print(f"❌ Task ID {tid} not found.")
                    continue
                confirm = input(f"⚠️ Delete task '{task.title}'? (y/n): ").strip().lower()
                if confirm == "y":
                    manager.delete_task(tid)
                    print(f"🗑️ Task {tid} deleted and changes persisted!")
            except ValueError:
                print("❌ Invalid Task ID!")

        elif choice == "6":
            if manager.save_to_file():
                print(f"💾 Tasks successfully saved to '{manager.storage_path}'.")

        elif choice == "7":
            if manager.load_from_file():
                print(f"📂 Tasks successfully reloaded from '{manager.storage_path}'.")
                display_tasks_table(manager.read_all_tasks())
            else:
                print(f"⚠️ Could not load tasks or file was empty.")

        elif choice == "8":
            target = input(f"Export text file path [default: {DEFAULT_EXPORT_FILE}]: ").strip()
            path = target if target else DEFAULT_EXPORT_FILE
            if manager.export_to_text_file(path):
                print(f"📄 Successfully exported tasks to text file: '{path}'")

        elif choice == "9":
            samples = [
                ("Implement Level 1 tasks", "Finish basic game and patterns", "High", "Completed"),
                ("Implement Level 2 tasks", "Finish CRUD and temperature converter", "High", "Completed"),
                ("Implement Level 3 tasks", "Implement file persistence and web scraper", "High", "Completed"),
                ("Review Git commits", "Ensure clean commit history and git push", "Medium", "In Progress"),
                ("LinkedIn Video Demo", "Record 2-3 minute project demonstration", "Medium", "Pending"),
            ]
            for t, d, p, s in samples:
                manager.create_task(t, d, p, s)
            print("🌱 Sample persistent tasks added!")
            display_tasks_table(manager.read_all_tasks())

        elif choice == "10":
            print("Exiting Persistent Task Manager.")
            break
        else:
            print("❌ Invalid option! Choose 1-10.")


def main():
    manager = PersistentTaskManager()
    run_persistent_interactive(manager)


if __name__ == "__main__":
    main()
