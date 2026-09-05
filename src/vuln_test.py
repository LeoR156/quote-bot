import sqlite3


def find_user_bad_practice(username: str):
    conn = sqlite3.connect("fake_database.db")
    cursor = conn.cursor()
    
    malicious_query = f"SELECT * FROM users WHERE name = '{username}'" # Vulnerability!
    
    cursor.execute(malicious_query)
    
    results = cursor.fetchall()
    conn.close()
    return results
