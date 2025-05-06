from modules.analysis import isNBA
from modules.scraper import get_playoff_bracket, get_standings
from modules.transformer import create_html_bracket
from modules.query import Query
from modules.controller.userController import UserController
from modules.controller.postController import PostController
from modules.controller.commentController import CommentController
from datetime import datetime
from data.text_data import unsure, non_nba
from flask import Flask, render_template, request, jsonify, redirect, flash, send_file
import json
from werkzeug.utils import secure_filename
import os
app = Flask(__name__)



"""
Function to handle routing to home page.

Parameters
----------
n/a

Returns
-------
HTML file
    Rendering of HTML template for home page.
"""
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/home")
def home2():
    return render_template("home.html")

"""
Function to handle routing to chatbox page.

Parameters
----------
n/a

Returns
-------
HTML file
    Rendering of HTML template for chatbox page
"""
@app.route("/chat")
def chat():
    return render_template("chat.html")

"""
Function to render blogs page.

Parameters
----------
n/a

Returns
-------
HTML file
    Rendering of HTML template for blog page
"""
@app.route("/blog")
def blog():
    return render_template("blogs.html")

"""
Function to handle routing to authors page.

Parameters
----------
n/a

Returns
-------
HTML file
    Rendering of HTML template for authors page
"""
@app.route("/authors")
def authors():
    return render_template("authors.html")

"""
Function to handle routing to predictions page.

Parameters
----------
n/a

Returns
-------
HTML file
    Rendering of HTML template for predictions page
"""
@app.route("/predictions")
def predictions():
    bracket = get_playoff_bracket()
    bracket = create_html_bracket(bracket)
    west_standings = get_standings("west")
    east_standings = get_standings("east")
    return render_template("predictions.html", bracket=bracket, west_standings=west_standings, east_standings=east_standings)

"""
Function to download requested blog for user.

Parameters
----------
n/a

Returns
-------
HTML file
    Rendering of HTML template for blog page.
"""
@app.route("/download/<string:id>", methods=['GET', 'POST'])
def download(id):
    if id is None:
        self.Error(400)
    try:
        blog_map ={
            "1" : "https://drive.google.com/uc?export=download&id=13FmzW70fMMfTwrypxzJRG-J6woty8ePz", # Dog pic
            "2" : "https://drive.google.com/uc?export=download&id=13FmzW70fMMfTwrypxzJRG-J6woty8ePz", # Dog pic
            "3" : "https://drive.google.com/uc?export=download&id=13FmzW70fMMfTwrypxzJRG-J6woty8ePz"  # Dog pic
        }
        return redirect(blog_map[id])
    except Exception as e:
        self.log.exception(e)
        self.Error(400)

"""
Function to handle POST request from user
with embedded message. The message is then 
passed to the chatbot and the response is returned 
to user.

Parameters
----------
request : json
    The POST request sent from user sending a message

Returns
-------
Bot response : json
    The chatbot response to user message
"""
@app.route("/bot-msg", methods=['POST'])
def get_bot_response():
    usr_msg = request.form['msg']
    handler = Query(usr_msg)
    response = handler.process()
    return jsonify(response)

if __name__ == "__main__":
    app.run()
    
    
    
# Tinh nang them
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        name = data.get('name')
        
        user_id = UserController.create_user(username, password, email, name)
        if user_id:
            print("Đăng ký thành công!")
            return jsonify({
                "message": "Đăng ký thành công!",
                "status": "success"
            }), 200
        else:
            print("Đã xảy ra lỗi. Vui lòng thử lại!")
            return jsonify({
                "message": "Đã xảy ra lỗi. Vui lòng thử lại!",
                "status": "danger"
            }), 400
            
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        user = UserController.get_user(username, password)
        if user:
            print("Đăng nhập thành công!")
            return jsonify({
                "message": "Đăng nhập thành công!",
                "status": "success",
                "user" : user.__dict__
            }), 200
        else:
            print("Tài khoản hoặc mật khẩu không đúng, vui lòng thử lại!")
            return jsonify({
                "message": "Tài khoản hoặc mật khẩu không đúng, vui lòng thử lại!",
                "status": "danger"
            }), 400
            
@app.route('/createpost', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        data = request.get_json()
        userId = data.get('userId')
        title = data.get('title')
        content = data.get('content')
        
        newPost = PostController.create_post(userId, title, content)
        if newPost:
            print("Tạo bài viết thành công!")
            return jsonify({
                "message": "Tạo bài viết thành công!",
                "status": "success"
            }), 200
        else:
            print("Đã xảy ra lỗi. Vui lòng thử lại!")
            return jsonify({
                "message": "Đã xảy ra lỗi khi tạo bài viết. Vui lòng thử lại!",
                "status": "danger"
            }), 400

@app.route('/getpost', methods=['GET'])
def get_post():
    data = request.get_json()
    postId = data.get('postId')

    post = PostController.get_post_by_id(postId)
    if post:
        print("Lấy bài viết thành công!")
        return jsonify({
            "message": "Lấy bài viết thành công!",
            "status": "success",
            "post" : post.to_dict()
        }), 200
    else:
        print("Đã xảy ra lỗi. Vui lòng thử lại!")
        return jsonify({
            "message": "Đã xảy ra lỗi khi lấy bài viết. Vui lòng thử lại!",
            "status": "danger"
        }), 400
@app.route('/getposts', methods=['GET'])
def get_posts():
    data = request.get_json()
    start = data.get('start')
    limit = data.get('limit')
    post = PostController.get_posts(start, limit)
    if post:
        print("Lấy bài viết thành công!")
        return jsonify({
            "message": "Lấy bài viết thành công!",
            "status": "success",
            "post" : post.__dict__
        }), 200
    else:
        print("Đã xảy ra lỗi. Vui lòng thử lại!")
        return jsonify({
            "message": "Đã xảy ra lỗi khi lấy bài viết. Vui lòng thử lại!",
            "status": "danger"
        }), 400
        
@app.route('/comment/create', methods=['POST'])
def create_comment():
    data = request.get_json()
    postId = data.get('postId')
    userId = data.get('userId')
    content = data.get('content')

    comment_id = CommentController.create_comment(postId, userId, content)
    if comment_id:
        return jsonify({
            "message": "Bình luận đã được tạo!",
            "status": "success",
            "commentId": comment_id
        }), 201
    else:
        return jsonify({
            "message": "Tạo bình luận thất bại!",
            "status": "danger"
        }), 500

@app.route('/upvote', methods=['POST'])
def upvote_comment():
    data = request.get_json()
    comment_id = data.get('commentId')
    user_id = data.get('userId')
    success = CommentController.upvote_comment(user_id,comment_id)
    if success:
        return jsonify({
            "message": "Upvote thành công!",
            "status": "success"
        }), 200
    else:
        return jsonify({
            "message": "Không thể upvote bình luận!",
            "status": "danger"
        }), 400


# Thư mục lưu trữ ảnh
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Giới hạn kích thước tệp (16 MB)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"message": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"message": "No selected file"}), 400
    
    # Kiểm tra loại tệp (nếu cần)
    if file and allowed_file(file.filename):
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Lấy postId từ form
        # post_id = request.form.get('postId') #post id được gửi từ frontend
        post_id = 1 # đây là fake
        if not post_id:
            return jsonify({"message": "Missing postId"}), 400

        # Lưu đường dẫn vào DB thông qua CommentController
        uploaded_at = datetime.now()
        success = CommentController.save_image_path(post_id, filename, uploaded_at)
        if success:
            return jsonify({"message": "File uploaded successfully!"}), 200
        else: 
            return jsonify({"message": "File saved but DB insert failed"}), 500
    else:
        return jsonify({"message": "Invalid file type"}), 400

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

# API trả ảnh từ đường dẫn
@app.route('/image/<int:image_id>', methods=['GET'])
def get_image(image_id):
    # Lấy thông tin ảnh từ cơ sở dữ liệu
    image = CommentController.get_image_path(image_id)
    
    if image and os.path.exists(image):
        # Lấy tên tệp từ đường dẫn
        filename = os.path.basename(image)
        
        # Kiểm tra phần mở rộng, nếu không có thì thêm vào
        if not filename.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            filename += '.jpg'  # Hoặc thêm loại phần mở rộng phù hợp
        
        # Trả về ảnh từ đường dẫn với đúng tên tệp và phần mở rộng
        return send_file(image, mimetype='image/jpeg', as_attachment=True, download_name=filename)
    else:
        return jsonify({"error": "Image not found or path invalid"}), 404