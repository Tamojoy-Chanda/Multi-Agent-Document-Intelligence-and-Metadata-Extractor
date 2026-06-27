import os
import mysql.connector
from mysql.connector import Error
import json

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            database=os.getenv("DB_NAME", "document_intelligence"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", "")
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

def insert_document_metadata(filename: str, category: str, metadata: dict):
    connection = get_db_connection()
    if not connection:
        return None
    try:
        cursor = connection.cursor()
        sql = "INSERT INTO documents (filename, category, metadata_json) VALUES (%s, %s, %s)"
        val = (filename, category, json.dumps(metadata))
        cursor.execute(sql, val)
        connection.commit()
        return cursor.lastrowid
    except Error as e:
        print(f"Failed to insert record into MySQL table: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def get_all_documents():
    connection = get_db_connection()
    if not connection:
        return []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM documents ORDER BY created_at DESC")
        records = cursor.fetchall()
        for record in records:
            if isinstance(record['metadata_json'], str):
                record['metadata_json'] = json.loads(record['metadata_json'])
        return records
    except Error as e:
        print(f"Failed to read records from MySQL table: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
