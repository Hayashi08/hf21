from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from shoulder import Shoulder
from image import MyImage
import numpy as np
import cv2
import os
from model import MySQL

SAVE_DIR = './static/images'

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = os.urandom(24)

## ユーザー認証

class User(UserMixin):
    def __init__(self, id, name):
        self.id = id
        self.name = name

@login_manager.user_loader
def load_user(id):
    user_id = int(id)
    db = MySQL()
    user_name = db.user_loader(user_id)
    db.close()
    if (user_name != None):
        return User(user_id, user_name)
    else:
        return None

## ページ

# インデックス
@app.route('/')
@login_required
def index():
    return render_template('index.html', title='インデックス')
    # return render_template('index.html', title='ログイン', message='ログインしてください。')

# メイン
@app.route('/main')
@login_required
def main():
    return render_template('main.html', title='メイン')

# アーカイブ
@app.route('/archive')
@login_required
def archive():
    return render_template('archive.html', title='アーカイブ')

# 設定
@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html', title='設定')

## ログイン機能

# ログイン
@app.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        user_name = request.form['user_name']
        password = request.form['password']

        db = MySQL()
        flag, user_id = db.login(user_name, password)
        db.close()

        if(flag):
            user = User(user_id, user_name)
            login_user(user)
            return render_template('index.html', title='インデックス')
        else:
            return render_template('login.html', title='ログイン', message='ログインできませんでした')

    else:
        return render_template('login.html', title='ログイン', message='ログインしてください')

# ログアウト
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('login.html', title='ログイン', message='ログインしてください。')

# ログインしていない場合
@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template('login.html', title='ログイン', message='ログインしてください。')

# 新規登録
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if(request.method == 'POST'):
        db = MySQL()
        flag = db.signup(request.form['user_name'], request.form['password'])
        db.close()
        if (flag):
            return render_template('login.html', title='ログイン', message='ログインしてください')
        else:
            return render_template('signup.html', title='新規登録', message ='IDがすでに使われています')
    else:
        return render_template('signup.html', title='新規登録', message ='新規登録')


# 画像処理

@app.route('/shoulder', methods=['POST'])
def shoulder():
    stream = request.files['image'].stream
    img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, 1)

    shoulder = Shoulder(img)
    result, save_path = shoulder.detect()

    return result + ',' + save_path

@app.route('/all_images')
def all_images():
    path = './static/images/all'
    files = os.listdir(path)
    files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
    if len(files_dir)>1:
        return render_template('all_images.html', title='処理過程', dir_name=files_dir[len(files_dir)-1])
    else: # エラー出ないようにディレクトリ用意 00000000_000000
        return render_template('all_images.html', title='処理過程', dir_name="00000000_000000")
if __name__ == '__main__':
    app.run(debug=True)