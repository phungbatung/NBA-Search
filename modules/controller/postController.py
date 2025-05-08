from modules.dbconnect.dbconnect import get_cursor
from modules.model.postModel import Post
from modules.controller.commentController import CommentController
from datetime import datetime

class PostController:
    def __init__(self):
        pass

    @staticmethod
    def get_posts(start=0, limit=3):
        conn, cursor = get_cursor()
        try:
            query = "SELECT * FROM posts ORDER BY createdAt DESC LIMIT %s OFFSET %s"
            cursor.execute(query, (limit, start))
            posts_data = cursor.fetchall()
            post_list = [
                Post(post[0], post[1], post[2], post[3], post[4]) for post in posts_data
            ]
            return post_list
        except Exception as e:
            print(f"Error while fetching posts: {e}")
            return []
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_post_by_id(postId):
        conn, cursor = get_cursor()
        try:
            query = "SELECT * FROM posts WHERE postId = %s"
            cursor.execute(query, (postId,))
            post_data = cursor.fetchone()
            if post_data:
                comments = CommentController.get_comments_by_post(postId)
                print(comments)
                return Post(post_data[0], post_data[1], post_data[2], post_data[3], post_data[4], comments)
            else:
                print("Post not found.")
                return None
        except Exception as e:
            print(f"Error while fetching post by ID: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def create_post(userId, title, content):
        conn, cursor = get_cursor()
        try:
            query = "INSERT INTO posts (userId, title, content, createdAt) VALUES (%s, %s, %s, %s)"
            createdAt = datetime.now()
            cursor.execute(query, (userId, title, content, createdAt))
            conn.commit()
            print("Post created successfully.")
            return cursor.lastrowid
        except Exception as e:
            print(f"Error while creating post: {e}")
            return None
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def upvote_post(userId, postId):
        conn, cursor = get_cursor()
        try:
            check_query = "SELECT 1 FROM upvotes WHERE userId = %s AND postId = %s"
            cursor.execute(check_query, (userId, postId))
            already_upvoted = cursor.fetchone()

            if already_upvoted:
                print(f"User {userId} đã upvote post {postId} trước đó.")
                return False

            insert_query = "INSERT INTO upvotes (userId, postId) VALUES (%s, %s)"
            cursor.execute(insert_query, (userId, postId))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error while upvoting post {postId} by user {userId}: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
