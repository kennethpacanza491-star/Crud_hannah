import database


def _read_task_id(prompt="Task ID: "):
    raw = input(prompt).strip()
    try:
        return int(raw)
    except ValueError:
        print("Please enter a valid numeric task ID.")
        return None


def _get_existing_task(task_id):
    task = database.get_task_by_id(task_id)
    if task is None:
        print(f"No task found with ID {task_id}.")
    return task


def _format_date(value):
    return str(value)[:19] if value else "-"


def _print_task(task):
    status = "Completed" if task["is_completed"] else "Pending"
    print("\n----------------------------------------")
    print(f"ID:          {task['id']}")
    print(f"Title:       {task['title']}")
    print(f"Description: {task['description'] or '-'}")
    print(f"Status:      {status}")
    print(f"Created:     {_format_date(task['created_at'])}")
    print("----------------------------------------")


def add_task():
    title = input("Task title: ").strip()
    if not title:
        print("Task title cannot be empty.")
        return

    description = input("Description (optional): ").strip()
    task_id = database.create_task(title, description)
    print(f"Task added successfully with ID {task_id}.")


def view_all_tasks():
    tasks = database.get_all_tasks()

    if not tasks:
        print("\nNo tasks found. Add a task to get started.")
        return

    print("\n" + "-" * 72)
    print(f"{'ID':<5}{'Status':<11}{'Title':<36}{'Created'}")
    print("-" * 72)
    for task in tasks:
        status = "Completed" if task["is_completed"] else "Pending"
        title = task["title"]
        if len(title) > 33:
            title = title[:30] + "..."
        print(f"{task['id']:<5}{status:<11}{title:<36}{_format_date(task['created_at'])}")
    print("-" * 72)
    print(f"Total tasks: {len(tasks)}")


def view_task_by_id():
    task_id = _read_task_id()
    if task_id is None:
        return

    task = _get_existing_task(task_id)
    if task is not None:
        _print_task(task)


def update_task():
    task_id = _read_task_id()
    if task_id is None:
        return

    task = _get_existing_task(task_id)
    if task is None:
        return

    _print_task(task)

    title = input(f"New title [{task['title']}]: ").strip()
    if not title:
        title = task["title"]

    current_description = task["description"] or ""
    description = input(f"New description [{current_description or 'none'}]: ").strip()
    if not description:
        description = current_description

    if database.update_task(task_id, title, description):
        print(f"Task {task_id} updated successfully.")
    else:
        print(f"Could not update task {task_id}; it may have been deleted.")


def mark_task_completed():
    task_id = _read_task_id()
    if task_id is None:
        return

    task = _get_existing_task(task_id)
    if task is None:
        return

    if task["is_completed"]:
        print(f"Task {task_id} is already completed.")
        return

    if database.mark_task_completed(task_id):
        print(f"Task {task_id} marked as completed.")
    else:
        print(f"Could not update task {task_id}; it may have been deleted.")


def delete_task():
    task_id = _read_task_id()
    if task_id is None:
        return

    task = _get_existing_task(task_id)
    if task is None:
        return

    _print_task(task)
    confirm = input("Are you sure you want to delete this task? (y/N): ").strip().lower()
    if confirm != "y":
        print("Delete cancelled.")
        return

    if database.delete_task(task_id):
        print(f"Task {task_id} deleted successfully.")
    else:
        print(f"Could not delete task {task_id}; it may have already been deleted.")
