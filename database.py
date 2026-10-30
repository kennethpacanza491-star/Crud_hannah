import os

import mysql.connector
from mysql.connector import Error

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "pacanza")

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
)
"""


def _server_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def test_connection():
    try:
        connection = _server_connection()
        if connection.is_connected():
            connection.close()
            return True, "Connected to MySQL successfully."
        return False, "MySQL server did not accept the connection."
    except Error as err:
        return False, str(err)


def initialize_database():
    connection = _server_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
        cursor.execute(f"USE `{DB_NAME}`")
        cursor.execute(CREATE_TABLE_SQL)
        connection.commit()
        cursor.close()
    finally:
        connection.close()


def _get_connection():
    initialize_database()
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
    )


def create_task(title, description=""):
    connection = _get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description) VALUES (%s, %s)",
            (title, description),
        )
        connection.commit()
        return cursor.lastrowid
    finally:
        connection.close()


def get_all_tasks():
    connection = _get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, title, description, is_completed, created_at "
            "FROM tasks ORDER BY id"
        )
        return cursor.fetchall()
    finally:
        connection.close()


def get_task_by_id(task_id):
    connection = _get_connection()
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, title, description, is_completed, created_at "
            "FROM tasks WHERE id = %s",
            (task_id,),
        )
        return cursor.fetchone()
    finally:
        connection.close()


def update_task(task_id, title, description):
    connection = _get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE tasks SET title = %s, description = %s WHERE id = %s",
            (title, description, task_id),
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def mark_task_completed(task_id):
    connection = _get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE tasks SET is_completed = TRUE WHERE id = %s",
            (task_id,),
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def delete_task(task_id):
    connection = _get_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()
