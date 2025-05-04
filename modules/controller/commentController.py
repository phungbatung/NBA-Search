from modules.dbconnect.dbconnect import get_cursor
from modules.model.commentModel import Comment
from datetime import datetime


class CommentController:
    def __init__(self):
        pass

    @staticmethod
    def create_comment(postId, userId, content, upvote=0):
        conn, cursor = get_cursor()
        createdAt = datetime.now()
        try:
            query = """
                INSERT INTO comments (postId, userId, content, createdAt, upvote)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (postId, userId, content, createdAt, upvote))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error while creating comment: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_comments_by_post(postId):
        conn, cursor = get_cursor()
        try:
            query = "SELECT * FROM comments WHERE postId = %s ORDER BY createdAt ASC"
            cursor.execute(query, (postId,))
            data = cursor.fetchall()
            return [Comment(*row) for row in data]
        except Exception as e:
            print(f"Error while fetching comments for post {postId}: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def upvote_comment(userId, commentId):
        conn, cursor = get_cursor()
        try:
            check_query = "SELECT 1 FROM upvotes WHERE userId = %s AND commentId = %s"
            cursor.execute(check_query, (userId, commentId))
            already_upvoted = cursor.fetchone()

            if already_upvoted:
                print(f"User {userId} đã upvote comment {commentId} trước đó.")
                return False 

            insert_query = "INSERT INTO upvotes (userId, commentId, upvote) VALUES (%s, %s, 1)"
            cursor.execute(insert_query, (userId, commentId))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error while upvoting comment {commentId} by user {userId}: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
