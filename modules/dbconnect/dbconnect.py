import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3308,
        user="root",
        password="admin",
        database="nba_search"
    )

def get_cursor():
    conn = get_connection()
    return conn, conn.cursor()