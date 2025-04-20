from modules.dbconnect.dbconnect import get_cursor
from werkzeug.security import generate_password_hash, check_password_hash
from modules.Model.userModel import User


class UserController:
    def __init__(self):
        pass
    
    @staticmethod
    def create_user(username, password, email, name):
        conn, cursor = get_cursor()
        try:
            password = generate_password_hash(password)
            query = "INSERT INTO user (username, password, email, name) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (username, password, email, name))
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error while creating user: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    @staticmethod
    def get_user(username, password):
        conn, cursor = get_cursor()
        try:
            query = "SELECT * FROM user WHERE username = %s"
            cursor.execute(query, (username,))
            userData = cursor.fetchone()
            print(userData)
            if userData and check_password_hash(userData[2], password):  # So sánh mật khẩu đã mã hóa
                userObj = User(userData[0], userData[1], userData[2], userData[3], userData[4])
                return userObj
            else:
                print("Invalid username or password.")
                return None
        except Exception as e:
            print(f"Error while fetching user: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
