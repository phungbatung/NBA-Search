from modules.dbconnect.dbconnect import get_cursor
from modules.Model.commentModel import Comment
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
    def upvote_comment(commentId):
        conn, cursor = get_cursor()
        try:
            query = "UPDATE comments SET upvote = upvote + 1 WHERE commentId = %s"
            cursor.execute(query, (commentId,))
            conn.commit()
            return cursor.rowcount > 0  # Trả về True nếu có dòng nào được cập nhật
        except Exception as e:
            print(f"Error while upvoting comment {commentId}: {e}")
            return False
        finally:
            cursor.close()
            conn.close()