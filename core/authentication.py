from core.database import connect_to_db

def get_current_user(token):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE token=%s", (token,))
    user = cursor.fetchone()
    conn.close()
    return user
