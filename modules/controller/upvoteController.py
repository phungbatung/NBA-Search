from modules.dbconnect.dbconnect import get_cursor

class UpvoteController:
    def __init__(self):
        pass

@staticmethod
def upvote_comment(userId, commentId):
    conn, cursor = get_cursor()
    try:
        print("log")
        check_query = "SELECT 1 FROM upvotes WHERE userId = %s AND commentId = %s"
        cursor.execute(check_query, (userId, commentId))
        already_upvoted = cursor.fetchone()
        print("log1")
        if already_upvoted:
            print(f"User {userId} đã upvote comment {commentId} trước đó.")
            return False  
        print("log2")
        insert_query = "INSERT INTO upvotes (userId, commentId) VALUES (%s, %s)"
        cursor.execute(insert_query, (userId, commentId))
        print("log3")
        conn.commit()
        return True
    except Exception as e:
        print(f"Error while upvoting comment {commentId} by user {userId}: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

