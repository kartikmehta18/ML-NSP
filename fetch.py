import sqlite3

def get_db_connection():
    conn = sqlite3.connect('HeartCare.db')
    conn.row_factory = sqlite3.Row
    return conn

def fetch_submissions():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM submit_form')
        submissions = cursor.fetchall()
        
        if submissions:
            print("Submissions fetched successfully:")
            for submission in submissions:
                print(f"ID: {submission['id']}")
                print(f"Name: {submission['name']}")
                print(f"Email: {submission['email']}")
                print(f"Message: {submission['message']}")
                print("----------")
        else:
            print("No submissions found.")

        conn.close()
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    fetch_submissions()
