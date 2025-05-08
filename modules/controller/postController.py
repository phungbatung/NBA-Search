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
            # JOIN để lấy thông tin bài viết kèm username
            query = """
                SELECT p.postId, p.title, p.content, p.createdAt, u.username
                FROM posts p
                JOIN user u ON p.userId = u.userId
                WHERE p.postId = %s
            """
            cursor.execute(query, (postId,))
            post_data = cursor.fetchone()

            if post_data:
                # Lấy comments
                comments = CommentController.get_comments_by_post(postId)
                comments_list = [c.to_dict() if hasattr(c, 'to_dict') else c for c in comments]

                # Lấy số lượng upvote
                upvote_query = "SELECT COUNT(*) FROM upvotes WHERE postId = %s"
                cursor.execute(upvote_query, (postId,))
                upvote_count = cursor.fetchone()[0]

                # Trả về JSON (dictionary)
                return {
                    "postId": post_data[0],
                    "title": post_data[1],
                    "content": post_data[2],
                    "createdAt": post_data[3],
                    "username": post_data[4],   # username thay vì userId
                    "comments": comments_list,
                    "upvote": upvote_count
                }
            else:
                print("Post not found.")
                return None

        except Exception as e:
            print(f"Error while fetching post by ID: {e}")
            return None

        finally:
            cursor.close()
            conn.close()

    # def get_post_by_id(postId):
    #     conn, cursor = get_cursor()
    #     try:
    #         # Lấy thông tin bài viết
    #         query = "SELECT * FROM posts WHERE postId = %s"
    #         cursor.execute(query, (postId,))
    #         post_data = cursor.fetchone()

    #         if post_data:
    #             # Lấy danh sách comment của post
    #             comments = CommentController.get_comments_by_post(postId)

    #             # Đếm số lượng upvotes
    #             upvote_query = "SELECT COUNT(*) FROM upvotes WHERE postId = %s"
    #             cursor.execute(upvote_query, (postId,))
    #             upvote_count = cursor.fetchone()[0]

    #             # Tạo object Post
    #             return Post(
    #                 postId=post_data[0],
    #                 userId=post_data[1],
    #                 title=post_data[2],
    #                 content=post_data[3],
    #                 createdAt=post_data[4],
    #                 comments=comments,
    #                 upvote=upvote_count
    #             )
    #         else:
    #             print("Post not found.")
    #             return None

    # except Exception as e:
    #     print(f"Error while fetching post by ID: {e}")
    #     return None

    # finally:
    #     cursor.close()
    #     conn.close()


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
