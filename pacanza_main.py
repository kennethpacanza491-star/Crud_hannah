import sys
import database
import todo


def display_menu():
    print()
    print("****************************************")
    print("      PYTHON MYSQL TODO MANAGER         ")
    print("****************************************")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. View Task by ID")
    print("4. Update Task")
    print("5. Mark Task as Completed")
    print("6. Delete Task")
    print("0. Exit")
    print("****************************************")


def check_database_readiness():
    is_connected, message = database.test_connection()

    if is_connected is False:
        print("\n[Database Connection Alert]")
        print(f"Could not connect to MySQL database: {message}")
        print("\nPlease ensure:")
        print("1. Your MySQL server service is actively running.")
        print("2. The 'todo_db' database exists (run 'schema.sql' first).")
        print("3. Connection settings (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME) match your environment.")
        return False

    print(f"\n[Database] {message}")
    return True


def main():
    print("\nStarting Python MySQL Todo Manager...")

    if not check_database_readiness():
        print("\nExiting. Fix the connection issue and try again.")
        return 1

    try:
        database.initialize_database()
    except Exception as err:
        print(f"\nCould not prepare the database: {err}")
        return 1

    while True:
        display_menu()

        try:
            choice = input("Enter your choice: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n\nGoodbye!")
            return 0

        if choice == "1":
            todo.add_task()
        elif choice == "2":
            todo.view_all_tasks()
        elif choice == "3":
            todo.view_task_by_id()
        elif choice == "4":
            todo.update_task()
        elif choice == "5":
            todo.mark_task_completed()
        elif choice == "6":
            todo.delete_task()
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid choice. Please select a number from the menu.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
