## 環境構築

1. Python

    1.1. Pythonのインストール
        ※ バージョンは3.8をおすすめ

    1.2. コマンドプロンプトで以下のコマンドを実行
        pip install flask
        pip install flask-login
        pip mysql-connector-python
        pip install numpy
        pip install opencv-python
        
        ※ この際、ちゃんとこの場所にPATH通しておけよ！みたいな文章がで出てきたら。その場所をPATHに通しておく。


## アプリ起動方法

    2.1. コマンドプロンプトで本アプリのルートディレクトリに移動

    2.2. ルートディレクトリで以下のコマンドを実行してサーバーを立ち上げる
        python app.py

    3.3. 以下のURLに"Chrome"でアクセス
        http://127.0.0.1:5000/

    3.4. サーバーの停止方法はCtrl+C

以上
