"""
Task 3: Console Application for Basic CRUD Operations on a List of Tasks
Level 2: Intermediate
Internship Program: Software Development - Cognifyz Technologies

Objective:
Implement Create, Read, Update, and Delete operations using arrays or lists for data storage.

Features:
- Task class with attributes: task_id, title, description, status, priority, created_at
- In-memory TaskManager maintaining tasks in a list
- Full CRUD operations: Create, Read (all / by ID / filtered), Update, Delete
- Formatted tabular display with ANSI status badges
- Input validation and edge-case handling
"""

import sys
from datetime import datetime
from typing import List, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


class Task:
    """Represents a single task entity."""

    VALID_STATUSES = ["Pending", "In Progress", "Completed"]
    VALID_PRIORITIES = ["Low", "Medium", "High"]

    def __init__(
        self,
        task_id: int,
        title: str,
        description: str = "",
        status: str = "Pending",
        priority: str = "Medium",
        created_at: Optional[str] = None,
    ):
        self.task_id = task_id
        self.title = title.strip()
        self.description = description.strip()
        self.status = status if status in self.VALID_STATUSES else "Pending"
        self.priority = priority if priority in self.VALID_PRIORITIES else "Medium"
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        """Convert task object to dictionary representation."""
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
        """Instantiate a Task from a dictionary."""
        return cls(
            task_id=data["task_id"],
            title=data["title"],
            description=data.get("description", ""),
            status=data.get("status", "Pending"),
            priority=data.get("priority", "Medium"),
            created_at=data.get("created_at"),
        )

    def __str__(self) -> str:
        return f"[ID: {self.task_id}] {self.title} | Status: {self.status} | Priority: {self.priority}"


class TaskManager:
    """Manages an in-memory list of tasks performing CRUD operations."""

    def __init__(self):
        self.tasks: List[Task] = []
        self._next_id = 1

    def create_task(
        self,
        title: str,
        description: str = "",
        priority: str = "Medium",
        status: str = "Pending",
    ) -> Task:
        """Create and append a new task to the list."""
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
        return task

    def read_all_tasks(self) -> List[Task]:
        """Return all tasks."""
        return list(self.tasks)

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Retrieve a task by its unique ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def search_tasks(self, keyword: str) -> List[Task]:
        """Search tasks by title or description keyword."""
        kw = keyword.lower()
        return [
            t
            for t in self.tasks
            if kw in t.title.lower() or kw in t.description.lower()
        ]

    def filter_tasks(
        self,
        status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> List[Task]:
        """Filter tasks by status and/or priority."""
        filtered = self.tasks
        if status:
            filtered = [t for t in filtered if t.status.lower() == status.lower()]
        if priority:
            filtered = [t for t in filtered if t.priority.lower() == priority.lower()]
        return filtered

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
    ) -> Optional[Task]:
        """Update fields of an existing task."""
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

        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if deleted, False otherwise."""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def seed_sample_tasks(self):
        """Populate initial tasks for quick evaluation."""
        samples = [
            ("Set up development workspace", "Install Python, Git, and clone repository", "High", "Completed"),
            ("Implement Level 1 tasks", "Complete number game and number patterns", "High", "Completed"),
            ("Design CRUD application", "Implement Task class and in-memory list operations", "Medium", "In Progress"),
            ("Add temperature converter", "Formula conversions between Celsius and Fahrenheit", "Medium", "Pending"),
            ("Prepare LinkedIn presentation", "Record short showcase video and prepare hashtags", "Low", "Pending"),
        ]
        for title, desc, prio, stat in samples:
            self.create_task(title, desc, prio, stat)


def display_tasks_table(tasks: List[Task]):
    """Pretty-print tasks in a structured tabular format."""
    if not tasks:
        print("\n📭 No tasks found.")
        return

    header = f"{'ID':<4} | {'Title':<30} | {'Priority':<8} | {'Status':<12} | {'Created At':<19}"
    divider = "-" * len(header)
    print("\n" + divider)
    print(header)
    print(divider)
    for t in tasks:
        title_disp = t.title[:27] + "..." if len(t.title) > 30 else t.title
        print(f"{t.task_id:<4} | {title_disp:<30} | {t.priority:<8} | {t.status:<12} | {t.created_at:<19}")
    print(divider)
    print(f"Total tasks displayed: {len(tasks)}\n")


def display_single_task(task: Task):
    """Detailed view for a single task."""
    print("\n" + "=" * 45)
    print(f"📌 Task Details [ID: {task.task_id}]")
    print("=" * 45)
    print(f"Title:       {task.title}")
    print(f"Description: {task.description or '(No description)'}")
    print(f"Priority:    {task.priority}")
    print(f"Status:      {task.status}")
    print(f"Created At:  {task.created_at}")
    print("=" * 45)


def run_crud_interactive(manager: TaskManager):
    """Interactive console UI for CRUD Task Manager."""
    while True:
        print("\n" + "=" * 55)
        print("   COGNIFYZ INTERNSHIP - TASK 3: TASK MANAGER (CRUD)")
        print("=" * 55)
        print("1. ➕ Create a New Task")
        print("2. 📋 View All Tasks")
        print("3. 🔍 View Task by ID")
        print("4. 🔎 Search / Filter Tasks")
        print("5. ✏️  Update Task Details")
        print("6. 🗑️  Delete a Task")
        print("7. ⚡ Seed Sample Tasks")
        print("8. 🚪 Return / Exit")

        choice = input("\nEnter your choice (1-8): ").strip()

        if choice == "1":
            print("\n--- Create New Task ---")
            title = input("Enter task title: ").strip()
            if not title:
                print("❌ Title cannot be empty!")
                continue
            desc = input("Enter task description (optional): ").strip()
            print("Select Priority: 1. Low  2. Medium  3. High")
            p_map = {"1": "Low", "2": "Medium", "3": "High"}
            priority = p_map.get(input("Choice (1-3, default Medium): ").strip(), "Medium")

            print("Select Status: 1. Pending  2. In Progress  3. Completed")
            s_map = {"1": "Pending", "2": "In Progress", "3": "Completed"}
            status = s_map.get(input("Choice (1-3, default Pending): ").strip(), "Pending")

            new_task = manager.create_task(title, desc, priority, status)
            print(f"✅ Task created successfully with ID: {new_task.task_id}!")

        elif choice == "2":
            display_tasks_table(manager.read_all_tasks())

        elif choice == "3":
            try:
                tid = int(input("Enter Task ID: ").strip())
                task = manager.get_task_by_id(tid)
                if task:
                    display_single_task(task)
                else:
                    print(f"❌ No task found with ID {tid}.")
            except ValueError:
                print("❌ Invalid Task ID! Please enter a number.")

        elif choice == "4":
            print("\n1. Search by Keyword")
            print("2. Filter by Status")
            print("3. Filter by Priority")
            sub = input("Select option (1-3): ").strip()
            if sub == "1":
                kw = input("Enter keyword: ").strip()
                res = manager.search_tasks(kw)
                display_tasks_table(res)
            elif sub == "2":
                print("Options: Pending / In Progress / Completed")
                st = input("Enter status: ").strip()
                res = manager.filter_tasks(status=st)
                display_tasks_table(res)
            elif sub == "3":
                print("Options: Low / Medium / High")
                pr = input("Enter priority: ").strip()
                res = manager.filter_tasks(priority=pr)
                display_tasks_table(res)

        elif choice == "5":
            try:
                tid = int(input("Enter Task ID to update: ").strip())
                task = manager.get_task_by_id(tid)
                if not task:
                    print(f"❌ Task ID {tid} not found.")
                    continue
                display_single_task(task)
                print("\nLeave blank to keep existing value:")
                new_title = input(f"New Title [{task.title}]: ").strip() or None
                new_desc = input(f"New Description [{task.description}]: ").strip()
                new_desc = new_desc if new_desc != "" else None

                print(f"Current Status: {task.status} (1. Pending / 2. In Progress / 3. Completed)")
                s_choice = input("Change status? (1-3, or Enter to skip): ").strip()
                s_map = {"1": "Pending", "2": "In Progress", "3": "Completed"}
                new_status = s_map.get(s_choice, None)

                print(f"Current Priority: {task.priority} (1. Low / 2. Medium / 3. High)")
                p_choice = input("Change priority? (1-3, or Enter to skip): ").strip()
                p_map = {"1": "Low", "2": "Medium", "3": "High"}
                new_priority = p_map.get(p_choice, None)

                manager.update_task(tid, new_title, new_desc, new_status, new_priority)
                print(f"✅ Task {tid} updated successfully!")
            except ValueError:
                print("❌ Invalid Task ID!")

        elif choice == "6":
            try:
                tid = int(input("Enter Task ID to delete: ").strip())
                task = manager.get_task_by_id(tid)
                if not task:
                    print(f"❌ Task ID {tid} not found.")
                    continue
                confirm = input(f"⚠️ Are you sure you want to delete task '{task.title}'? (y/n): ").strip().lower()
                if confirm == "y":
                    if manager.delete_task(tid):
                        print(f"🗑️ Task {tid} deleted successfully.")
                    else:
                        print("❌ Failed to delete task.")
                else:
                    print("Deletion cancelled.")
            except ValueError:
                print("❌ Invalid Task ID!")

        elif choice == "7":
            manager.seed_sample_tasks()
            print("🌱 Sample tasks loaded!")
            display_tasks_table(manager.read_all_tasks())

        elif choice == "8":
            print("Exiting Task Manager.")
            break
        else:
            print("❌ Invalid option! Choose 1-8.")


def main():
    manager = TaskManager()
    run_crud_interactive(manager)


if __name__ == "__main__":
    main()
