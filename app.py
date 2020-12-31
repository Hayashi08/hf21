from flask import Flask, render_template, request
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin,current_user
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

# メイン
@app.route('/main', methods=['POST'])
@login_required
def main():
    if request.method == 'POST':
        company_name = request.form['company_name']
        company_stage = request.form['company_stage']
        db = MySQL()
        session_id, session_timestamp = db.insert_session(int(current_user.id), company_name, company_stage)
        db.close()
        return render_template('main.html', title='メイン', session_id=str(session_id), session_timestamp=session_timestamp, company_name=company_name, company_stage=company_stage)
    else:
        return render_template('index.html', title='インデックス')

# 保存
@app.route('/save', methods=['POST'])
@login_required
def save():
    if request.method == 'POST':
        result = request.form['result']
        sentence = request.form['sentence']
        image = request.form['image']

        db = MySQL()

        result_list = result.split(',')
        result_id = db.insert_result(int(result_list[0]), str(result_list[1]), str(result_list[2]))

        sentence_list = sentence.split('|')
        for sentence_row in sentence_list:
            sentence_ele = sentence_row.split(',')
            if len(sentence_ele) != 1 and sentence_ele[2] != 'Infinity':
                db.insert_sentence(result_id, str(sentence_ele[0]), str(sentence_ele[1]), int(sentence_ele[2]))


        image_list = image.split('|')
        for image_row in image_list:
            image_ele = image_row.split(',')
            if len(image_ele) != 1:
                db.insert_image(result_id, str(image_ele[0]), str(image_ele[1]), str(image_ele[2]))

        db.close()

        return render_template('index.html', title='インデックス')
    else:
        return render_template('index.html', title='インデックス')

# アーカイブ
@app.route('/archive')
@login_required
def archive():

    db = MySQL()
    rows = db.archive(int(current_user.id))
    db.close()

    return render_template('archive.html', title='アーカイブ',rows=rows)

# アーカイブ詳細
@app.route('/archive/<id>')
@login_required
def archive_detail(id):
    session_id = id
    db = MySQL()
    row_session, row_result, log_list = db.archive_detail(session_id)
    db.close()
    return render_template('archive_detail.html', title='アーカイブ詳細', row_session=row_session, row_result=row_result, log_list=log_list)

# 設定
@app.route('/settings')
@login_required
def settings():
    return render_template('settings.html', title='設定')

# 設定編集
@app.route('/settings_edit')
@login_required
def settings_edit():
    return render_template('settings_edit.html', title='設定')


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


# 検出
@app.route('/shoulder', methods=['POST'])
def shoulder():
    stream = request.files['image'].stream
    img_array = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    img = cv2.imdecode(img_array, 1)

    shoulder = Shoulder(img)
    result, save_path = shoulder.detect()

    return result + ',' + save_path

# 画像処理デモ
@app.route('/all_images')
def all_images():
    path = './static/images/all'
    files = os.listdir(path)
    files_dir = [f for f in files if os.path.isdir(os.path.join(path, f))]
    if len(files_dir)>1:
        return render_template('all_images.html', title='処理過程', dir_name=files_dir[len(files_dir)-1])
    else: # エラー出ないようにディレクトリ用意 00000000_000000
        return render_template('all_images.html', title='処理過程', dir_name="00000000_000000")


# 起動時の設定
if __name__ == '__main__':
    app.run(debug=True)