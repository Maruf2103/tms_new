import sqlite3


def check_database():
    try:
        conn = sqlite3.connect('tms_database.db')
        cursor = conn.cursor()

        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print("📊 Database Tables:")
        for table in tables:
            print(f" - {table[0]}")

        # Check users table if it exists
        if any('users' in table for table in tables):
            cursor.execute("SELECT * FROM users;")
            users = cursor.fetchall()
            print(f"\n👥 Users ({len(users)} records):")
            for user in users:
                print(f" - {user}")

        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    check_database()