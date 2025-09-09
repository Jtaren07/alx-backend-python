import sqlite3
import functools

def with_db_connection(func):
    """Decorators to handle open and closing DB connection."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor=conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

# Call the function to test
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
