from modules.dbconnect.dbconnect import get_cursor
from modules.model.commentModel import Comment
from datetime import datetime


class CommentController:
    def __init__(self):
        pass

    @staticmethod
    def create_comment(postId, userId, content):
        conn, cursor = get_cursor()
        createdAt = datetime.now()
        try:
            query = """
                INSERT INTO comments (postId, userId, content, createdAt)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (postId, userId, content, createdAt))
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
            query = """
                SELECT c.commentId, c.content, c.createdAt, c.postId, u.username
                FROM comments c
                JOIN user u ON c.userId = u.userId
                WHERE c.postId = %s
                ORDER BY c.createdAt ASC
            """
            cursor.execute(query, (postId,))
            comment_rows = cursor.fetchall()

            comments = []
            for row in comment_rows:
                comment = {
                    "commentId": row[0],
                    "content": row[1],
                    "createdAt": row[2],
                    "postId": row[3],
                    "username": row[4]
                }
                comments.append(comment)

            return comments

        except Exception as e:
            print(f"Error while fetching comments: {e}")
            return []

        finally:
            cursor.close()
            conn.close()

    # @staticmethod
    # def upvote_comment(userId, commentId):
    #     conn, cursor = get_cursor()
    #     try:
    #         check_query = "SELECT 1 FROM upvotes WHERE userId = %s AND commentId = %s"
    #         cursor.execute(check_query, (userId, commentId))
    #         already_upvoted = cursor.fetchone()

    #         if already_upvoted:
    #             print(f"User {userId} đã upvote comment {commentId} trước đó.")
    #             return False 

    #         insert_query = "INSERT INTO upvotes (userId, commentId) VALUES (%s, %s)"
    #         cursor.execute(insert_query, (userId, commentId))
    #         conn.commit()
    #         return True
    #     except Exception as e:
    #         print(f"Error while upvoting comment {commentId} by user {userId}: {e}")
    #         return False
    #     finally:
    #         cursor.close()
    #         conn.close()
